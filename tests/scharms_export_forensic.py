from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import urlencode

import httpx
import requests
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer"
BBOX = "102.18383789062501,2.28455066023697,102.19482421875,2.2955282141879016"
EXACT = BASE + "/export?" + urlencode({
    "bbox": BBOX,
    "bboxSR": "4326",
    "imageSR": "4326",
    "size": "256,256",
    "dpi": "96",
    "format": "png32",
    "transparent": "true",
    "layers": "show:0",
    "f": "image",
})
OUT = Path(os.environ.get("URBION_SCHARMS_FORENSIC_DIR", "/tmp/urbion-scharms-forensic"))
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw_response_png32.bin"
HEADERS_FILE = OUT / "response_headers.txt"
REPORT_JSON = OUT / "scharms_forensic.json"
REPORT_TXT = OUT / "scharms_forensic.txt"
ORIGIN = "https://urbion-horizon-championship.onrender.com"
HTTP_TIMEOUT = 45
BROWSER_TEST_TIMEOUT_MS = 10_000
BROWSER_WATCHDOG_SEC = 60


def classify(body: bytes, ctype: str = "") -> str:
    if not body:
        return "empty"
    sig = body[:16]
    low = body[:1024].lstrip().lower()
    if sig.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if sig.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    if sig.startswith((b"GIF87a", b"GIF89a")):
        return "GIF"
    if low.startswith(b"<!doctype html") or low.startswith(b"<html") or b"<html" in low[:256]:
        return "HTML"
    if low.startswith((b"{", b"[")):
        try:
            json.loads(body.decode("utf-8", "replace"))
            return "JSON"
        except Exception:
            pass
    if low.startswith((b"<?xml", b"<error", b"<arcgis")) or b"<error" in low[:256]:
        return "XML"
    try:
        text = body[:1024].decode("utf-8")
        if sum(ch.isprintable() or ch in "\r\n\t" for ch in text) / max(1, len(text)) > 0.9:
            return "text"
    except Exception:
        pass
    return "binary/unknown"


def image_validity(body: bytes, kind: str) -> dict:
    if kind == "PNG":
        if len(body) < 24 or body[:8] != b"\x89PNG\r\n\x1a\n":
            return {"valid": False, "detail": "bad PNG signature"}
        pos = 8
        chunks = []
        try:
            while pos + 12 <= len(body):
                n = int.from_bytes(body[pos : pos + 4], "big")
                typ = body[pos + 4 : pos + 8]
                end = pos + 12 + n
                if end > len(body):
                    return {"valid": False, "detail": "truncated PNG chunk"}
                chunks.append(typ.decode("ascii", "replace"))
                pos = end
                if typ == b"IEND":
                    return {"valid": True, "detail": f"PNG chunks parsed; IEND at byte {pos}; chunks={chunks[:12]}"}
            return {"valid": False, "detail": "PNG has no complete IEND"}
        except Exception as e:
            return {"valid": False, "detail": f"PNG parse error: {e}"}
    if kind == "JPEG":
        return {
            "valid": len(body) >= 4 and body[:3] == b"\xff\xd8\xff" and body[-2:] == b"\xff\xd9",
            "detail": "JPEG SOI/EOI check",
        }
    if kind == "GIF":
        return {"valid": len(body) >= 10 and body[-1:] == b";", "detail": "GIF header/trailer check"}
    return {"valid": None, "detail": None}


def headers_dict(headers) -> dict:
    wanted = {
        "content-type",
        "content-length",
        "content-encoding",
        "cache-control",
        "etag",
        "server",
        "date",
        "location",
        "x-content-type-options",
        "access-control-allow-origin",
        "access-control-allow-credentials",
        "vary",
    }
    result = {}
    for k, v in headers.items():
        lk = k.lower()
        if lk in wanted or "arcgis" in lk or lk.startswith(("x-", "cf-", "akamai-", "server-timing")):
            result[lk] = v
    return result


def response_record(r) -> dict:
    body = r.content
    kind = classify(body, r.headers.get("content-type", ""))
    return {
        "status": r.status_code,
        "url": str(r.url),
        "redirects": [
            {
                "status": h.status_code,
                "url": str(h.url),
                "headers": headers_dict(h.headers),
                "location": h.headers.get("location"),
            }
            for h in r.history
        ],
        "headers": headers_dict(r.headers),
        "body_length": len(body),
        "first64_hex": body[:64].hex(" "),
        "first64_text": body[:64].decode("utf-8", "replace"),
        "classification": kind,
        "image_validity": image_validity(body, kind),
        "body_prefix_500": body[:500].decode("utf-8", "replace") if kind not in ("PNG", "JPEG", "GIF", "binary/unknown") else None,
        "content_type": r.headers.get("content-type", ""),
        "body": body,
    }


def request_one(url: str, headers=None, client_name: str = "requests") -> dict:
    headers = headers or {}
    if client_name == "requests":
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=HTTP_TIMEOUT)
    else:
        timeout = httpx.Timeout(HTTP_TIMEOUT)
        with httpx.Client(follow_redirects=True, timeout=timeout) as c:
            r = c.get(url, headers=headers)
    return response_record(r)


def safe_request_one(evidence_section: dict, label: str, url: str, headers=None, client_name: str = "requests") -> dict | None:
    started = time.monotonic()
    try:
        result = request_one(url, headers=headers, client_name=client_name)
        body = result.pop("body")
        evidence_section[label] = result
        return body
    except Exception as e:
        evidence_section[label] = {
            "event": "error",
            "failed": True,
            "exception_type": type(e).__name__,
            "exception_text": str(e),
            "elapsed_sec": round(time.monotonic() - started, 3),
        }
        return None


def curl_get(url: str, headers=None, out_name: str = "curl_body.bin") -> dict:
    headers = headers or {}
    body_path = OUT / out_name
    headers_path = OUT / (out_name + ".headers")
    verbose_path = OUT / (out_name + ".verbose.txt")
    cmd = [
        "curl",
        "-sS",
        "-L",
        "--connect-timeout",
        "15",
        "--max-time",
        str(HTTP_TIMEOUT),
        "-D",
        str(headers_path),
        "-o",
        str(body_path),
        "-w",
        "\\nCURL_FINAL_URL=%{url_effective}\\nCURL_STATUS=%{http_code}\\n",
        url,
    ]
    if headers:
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
    result = {"command": cmd, "body_file": str(body_path), "headers_file": str(headers_path), "verbose_file": str(verbose_path)}
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=HTTP_TIMEOUT + 5)
        result.update({"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr})
    except Exception as e:
        result.update({"event": "error", "failed": True, "exception_type": type(e).__name__, "exception_text": str(e)})
    verbose_cmd = [
        "curl",
        "-v",
        "-L",
        "--connect-timeout",
        "15",
        "--max-time",
        str(HTTP_TIMEOUT),
        "-o",
        "/dev/null",
        url,
    ]
    if headers:
        for k, v in headers.items():
            verbose_cmd += ["-H", f"{k}: {v}"]
    try:
        v = subprocess.run(verbose_cmd, capture_output=True, text=True, timeout=HTTP_TIMEOUT + 5)
        verbose_path.write_text(v.stderr + "\n" + v.stdout, encoding="utf-8")
        result["verbose_returncode"] = v.returncode
    except Exception as e:
        result["verbose_error"] = {"exception_type": type(e).__name__, "exception_text": str(e)}
        try:
            verbose_path.write_text(json.dumps(result["verbose_error"], indent=2), encoding="utf-8")
        except Exception:
            pass
    return result


def variant_url(fmt=None, f="image") -> str:
    q = {
        "bbox": BBOX,
        "bboxSR": "4326",
        "imageSR": "4326",
        "size": "256,256",
        "dpi": "96",
        "transparent": "true",
        "layers": "show:0",
        "f": f,
    }
    if fmt:
        q["format"] = fmt
    return BASE + "/export?" + urlencode(q)


def timeout_result(label: str, ms: int) -> dict:
    return {"event": "timeout", "timed_out": True, "timeout_ms": ms, "label": label}


def browser_eval(page, script: str, arg, label: str, evidence: dict, timeout_ms: int = BROWSER_TEST_TIMEOUT_MS):
    started = time.monotonic()
    try:
        value = page.evaluate(script, arg, timeout=timeout_ms)
        evidence[label] = {"completed": True, "elapsed_sec": round(time.monotonic() - started, 3), "result": value}
        return value
    except PlaywrightTimeoutError:
        evidence[label] = timeout_result(label, timeout_ms)
    except Exception as e:
        evidence[label] = {
            "event": "error",
            "failed": True,
            "exception_type": type(e).__name__,
            "exception_text": str(e),
            "elapsed_sec": round(time.monotonic() - started, 3),
        }
    return None


def browser_section() -> dict:
    evidence = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sections": {}, "trace": [], "timed_out": False}
    started = time.monotonic()
    browser = context = page = cdp = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            cdp = context.new_cdp_session(page)
            cdp.send("Network.enable")

            def record(kind, payload):
                try:
                    haystack = str(payload.get("request", payload.get("response", payload))) if isinstance(payload, dict) else str(payload)
                    if "GTsemasa_04" in haystack or "scharms.planmalaysia.gov.my" in haystack:
                        evidence["trace"].append({"kind": kind, "payload": payload})
                except Exception as e:
                    evidence.setdefault("diagnostic_errors", []).append({"section": "trace", "exception_type": type(e).__name__, "exception_text": str(e)})

            for event in ["Network.requestWillBeSent", "Network.responseReceived", "Network.loadingFailed", "Network.loadingFinished"]:
                cdp.on(event, lambda p, e=event: record(e, p))
            page.on("request", lambda r: record("playwright.request", {"url": r.url, "headers": r.all_headers(), "resource_type": r.resource_type, "frame_url": r.frame.url if r.frame else None}) if "GTsemasa_04/MapServer/export" in r.url else None)
            page.on("response", lambda r: record("playwright.response", {"url": r.url, "status": r.status, "headers": r.all_headers()}) if "GTsemasa_04/MapServer/export" in r.url else None)
            page.on("requestfinished", lambda r: record("playwright.requestfinished", {"url": r.url}) if "GTsemasa_04/MapServer/export" in r.url else None)
            page.on("requestfailed", lambda r: record("playwright.requestfailed", {"url": r.url, "failure": r.failure, "headers": r.all_headers(), "resource_type": r.resource_type}) if "GTsemasa_04/MapServer/export" in r.url else None)

            try:
                page.goto("data:text/html,<html><body></body></html>", timeout=BROWSER_TEST_TIMEOUT_MS, wait_until="domcontentloaded")
                evidence["sections"]["page_setup"] = {"completed": True}
            except Exception as e:
                evidence["sections"]["page_setup"] = {"event": "error", "failed": True, "exception_type": type(e).__name__, "exception_text": str(e)}

            if time.monotonic() - started < BROWSER_WATCHDOG_SEC:
                browser_eval(
                    page,
                    """async ({url}) => {
                      const a={img:null,newImage:null,fetch:null,fetchError:null};
                      const withTimeout=(promise,ms)=>Promise.race([
                        promise,
                        new Promise(resolve=>setTimeout(()=>resolve({event:'timeout',timed_out:true,timeout_ms:ms}),ms))
                      ]);
                      const done = withTimeout(new Promise(resolve=>{
                        let n=0;
                        const finish=()=>{n+=1;if(n===2)resolve({event:'done',completions:n});};
                        const i=document.createElement('img');
                        i.onload=()=>{a.img='load';finish()};
                        i.onerror=()=>{a.img='error';finish()};
                        i.src=url; document.body.appendChild(i);
                        const j=new Image();
                        j.onload=()=>{a.newImage='load';finish()};
                        j.onerror=()=>{a.newImage='error';finish()};
                        j.src=url;
                      }),10000);
                      try {
                        const r=await withTimeout(fetch(url),10000);
                        if(r && r.timed_out) a.fetchError=r;
                        else { a.fetch={ok:r.ok,status:r.status,type:r.type,contentType:r.headers.get('content-type')}; await withTimeout(r.arrayBuffer(),10000); }
                      } catch(e) { a.fetchError=String(e); }
                      const result=done && done.timed_out ? {...a,...done} : {...a,done};
                      return result;
                    }""",
                    {"url": EXACT},
                    "scharms_control_images",
                )
            else:
                evidence["sections"]["scharms_control_images"] = timeout_result("scharms_control_images", 0)

            if time.monotonic() - started < BROWSER_WATCHDOG_SEC:
                browser_eval(
                    page,
                    """async (url) => {
                      const out={};
                      const finish = async () => new Promise(resolve=>{
                        const i=new Image(); const timer=setTimeout(()=>resolve({event:'timeout',timed_out:true,timeout_ms:10000}),10000);
                        i.onload=()=>{clearTimeout(timer);resolve({event:'load',complete:i.complete,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight});};
                        i.onerror=()=>{clearTimeout(timer);resolve({event:'error',complete:i.complete,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight});};
                        i.src=url; document.body.appendChild(i);
                      });
                      out.img=await finish();
                      try { const f=await Promise.race([fetch(url),new Promise(resolve=>setTimeout(()=>resolve(null),10000))]); out.fetch=f?{success:true,status:f.status,type:f.type,url:f.url,headers:Object.fromEntries(f.headers.entries())}:{event:'timeout',timed_out:true,timeout_ms:10000}; }
                      catch(e){out.fetch={success:false,error:String(e)}}
                      return out;
                    }""",
                    EXACT,
                    "scharms_img_fetch",
                )

            if time.monotonic() - started < BROWSER_WATCHDOG_SEC:
                browser_eval(
                    page,
                    """async (url) => Promise.race([
                      new Promise(resolve=>{
                        const d=document.createElement('div'); d.style.width='1px'; d.style.height='1px'; d.style.backgroundImage=`url(${url})`; document.body.appendChild(d);
                        setTimeout(()=>resolve({event:'done',timed_out:false,backgroundImage:getComputedStyle(d).backgroundImage}),1000);
                      }),
                      new Promise(resolve=>setTimeout(()=>resolve({event:'timeout',timed_out:true,timeout_ms:10000}),10000))
                    ])""",
                    EXACT,
                    "scharms_css_background",
                )

            if time.monotonic() - started < BROWSER_WATCHDOG_SEC:
                browser_eval(
                    page,
                    """async (url) => Promise.race([
                      new Promise(resolve=>{
                        const i=new Image(); i.onload=()=>resolve({event:'load',complete:i.complete,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight}); i.onerror=()=>resolve({event:'error',complete:i.complete,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight}); i.src=url;
                      }),
                      new Promise(resolve=>setTimeout(()=>resolve({event:'timeout',timed_out:true,timeout_ms:10000}),10000))
                    ])""",
                    EXACT,
                    "scharms_isolated_img",
                )

            if time.monotonic() - started < BROWSER_WATCHDOG_SEC:
                browser_eval(
                    page,
                    """async (url) => Promise.race([
                      (async()=>{try{const r=await fetch(url);return {success:true,status:r.status,type:r.type,url:r.url,headers:Object.fromEntries(r.headers.entries())}}catch(e){return {success:false,error:String(e)}}})(),
                      new Promise(resolve=>setTimeout(()=>resolve({event:'timeout',timed_out:true,timeout_ms:10000}),10000))
                    ])""",
                    EXACT,
                    "scharms_isolated_fetch",
                )

            if time.monotonic() - started >= BROWSER_WATCHDOG_SEC:
                evidence["timed_out"] = True
                evidence["watchdog"] = timeout_result("browser_diagnostics_overall", BROWSER_WATCHDOG_SEC * 1000)
    except Exception as e:
        evidence.setdefault("diagnostic_errors", []).append({"section": "browser", "exception_type": type(e).__name__, "exception_text": str(e)})
    finally:
        for obj, name in [(page, "page"), (context, "context"), (browser, "browser")]:
            if obj is not None:
                try:
                    obj.close()
                except Exception as e:
                    evidence.setdefault("diagnostic_errors", []).append({"section": f"cleanup.{name}", "exception_type": type(e).__name__, "exception_text": str(e)})
    evidence["elapsed_sec"] = round(time.monotonic() - started, 3)
    evidence["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return evidence


def main() -> int:
    evidence = {
        "exact_url": EXACT,
        "bbox": BBOX,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "curl": {},
        "clients": {},
        "variants": {},
        "origin_tests": {},
        "metadata": {},
        "browser": {},
        "classification": {},
        "diagnostic_errors": [],
        "completed_sections": [],
        "failed_sections": [],
        "timed_out_sections": [],
    }
    exact_req = None
    raw_body = None

    try:
        evidence["curl"]["exact"] = curl_get(EXACT, out_name="raw_response_png32.bin")
        evidence["completed_sections"].append("exact_curl")

        raw_body = safe_request_one(evidence["clients"], "requests_exact", EXACT, client_name="requests")
        if raw_body is not None:
            exact_req = evidence["clients"]["requests_exact"]
            RAW.write_bytes(raw_body)
            HEADERS_FILE.write_text(json.dumps(exact_req["headers"], indent=2, sort_keys=True), encoding="utf-8")
            evidence["completed_sections"].append("requests_exact")
        else:
            evidence["failed_sections"].append("requests_exact")

        httpx_result_body = safe_request_one(evidence["clients"], "httpx_exact", EXACT, client_name="httpx")
        (evidence["completed_sections"] if httpx_result_body is not None else evidence["failed_sections"]).append("httpx_exact")

        for label, fmt, f in [("png32", "png32", "image"), ("png", "png", "image"), ("jpg", "jpg", "image"), ("json", None, "json")]:
            r = safe_request_one(evidence["variants"], label, variant_url(fmt, f), client_name="requests")
            (evidence["completed_sections"] if r is not None else evidence["failed_sections"]).append(f"variant_{label}")

        for label, headers in [
            ("no_origin", {}),
            ("origin", {"Origin": ORIGIN}),
            ("origin_referer", {"Origin": ORIGIN, "Referer": ORIGIN + "/"}),
        ]:
            r = safe_request_one(evidence["origin_tests"], label, EXACT, headers=headers, client_name="requests")
            (evidence["completed_sections"] if r is not None else evidence["failed_sections"]).append(f"origin_{label}")

        for path in ["?f=json", "/0?f=json"]:
            label = "service_json" if path == "?f=json" else "layer0_json"
            rbody = safe_request_one(evidence["metadata"], label, BASE + path, client_name="requests")
            if rbody is not None:
                evidence["metadata"][label]["body_prefix_500"] = rbody[:500].decode("utf-8", "replace")
                try:
                    evidence["metadata"][label]["json"] = json.loads(rbody.decode("utf-8"))
                except Exception as e:
                    evidence["metadata"][label]["json_parse_error"] = str(e)
                evidence["completed_sections"].append(label)
            else:
                evidence["failed_sections"].append(label)
        rbody = safe_request_one(evidence["metadata"], "export_pjson", variant_url("png32", "pjson"), client_name="requests")
        if rbody is not None:
            evidence["metadata"]["export_pjson"]["body_prefix_500"] = rbody[:500].decode("utf-8", "replace")
            evidence["completed_sections"].append("export_pjson")
        else:
            evidence["failed_sections"].append("export_pjson")

        if raw_body is not None:
            evidence["http_priority"] = {
                "status": evidence["clients"].get("requests_exact", {}).get("status"),
                "final_url": evidence["clients"].get("requests_exact", {}).get("url"),
                "redirect_chain": evidence["clients"].get("requests_exact", {}).get("redirects", []),
                "content_type": evidence["clients"].get("requests_exact", {}).get("content-type", evidence["clients"].get("requests_exact", {}).get("headers", {}).get("content-type")),
                "headers": evidence["clients"].get("requests_exact", {}).get("headers", {}),
                "body_length": len(raw_body),
                "first64_hex": raw_body[:64].hex(" "),
                "png_signature": raw_body[:8] == b"\x89PNG\r\n\x1a\n",
                "image_validity": image_validity(raw_body, classify(raw_body)),
            }
        else:
            evidence["http_priority"] = {"event": "unavailable", "reason": "requests exact GET failed; inspect curl evidence"}

        evidence["browser"] = browser_section()
        evidence["completed_sections"].append("browser_diagnostics")

        browser_trace = evidence["browser"].get("trace", [])
        response_seen = any(x.get("kind") == "Network.responseReceived" for x in browser_trace)
        failures = [x for x in browser_trace if x.get("kind") == "Network.loadingFailed"]
        failure = failures[0] if failures else None
        status = evidence.get("clients", {}).get("requests_exact", {}).get("status") if raw_body is not None else None
        cls = classify(raw_body) if raw_body is not None else "unknown"
        if status is None:
            category = "11. other"
            confidence = "LOW"
        elif status >= 400:
            category = "6. HTTP error response"
            confidence = "HIGH"
        elif cls not in ("PNG", "JPEG", "GIF"):
            category = "7. invalid/non-image response body"
            confidence = "HIGH"
        elif evidence["browser"].get("timed_out"):
            category = "11. other"
            confidence = "MEDIUM"
        elif response_seen and failure and failure.get("payload", {}).get("blockedReason"):
            category = "8. valid image + browser cross-origin delivery policy"
            confidence = "HIGH"
        elif response_seen and failure and "ORB" in str(failure):
            category = "9. invalid/missing response headers causing ORB"
            confidence = "MEDIUM"
        elif failure and "BLOCKED_BY_ORB" in str(failure):
            category = "9. invalid/missing response headers causing ORB"
            confidence = "MEDIUM"
        elif status == 200 and cls in ("PNG", "JPEG", "GIF"):
            category = "8. valid image + browser cross-origin delivery policy"
            confidence = "MEDIUM"
        else:
            category = "11. other"
            confidence = "MEDIUM"
        evidence["classification"] = {
            "primary": category,
            "confidence": confidence,
            "proof": [
                f"raw status={status}",
                f"raw body classification={cls}",
                f"raw body length={len(raw_body) if raw_body is not None else None}",
                f"PNG signature={raw_body[:8].hex(' ') if raw_body is not None else None}",
                f"Network.responseReceived={response_seen}",
                f"Network.loadingFailed={bool(failure)}",
                f"loadingFailed payload={failure.get('payload') if failure else None}",
            ],
        }
    except Exception as e:
        evidence["diagnostic_errors"].append({"section": "main", "exception_type": type(e).__name__, "exception_text": str(e)})
        evidence["failed_sections"].append("main")
    finally:
        try:
            if raw_body is not None and not RAW.exists():
                RAW.write_bytes(raw_body)
        except Exception as e:
            evidence["diagnostic_errors"].append({"section": "save_raw", "exception_type": type(e).__name__, "exception_text": str(e)})
        if not exact_req and not HEADERS_FILE.exists():
            try:
                HEADERS_FILE.write_text(json.dumps(evidence.get("http_priority", {}), indent=2), encoding="utf-8")
            except Exception as e:
                evidence["diagnostic_errors"].append({"section": "save_headers", "exception_type": type(e).__name__, "exception_text": str(e)})

        for section_name, section in evidence.items():
            if isinstance(section, dict) and section.get("event") == "timeout":
                evidence["timed_out_sections"].append(section_name)
        evidence["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            REPORT_JSON.write_text(json.dumps(evidence, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        except Exception as e:
            evidence["diagnostic_errors"].append({"section": "write_json", "exception_type": type(e).__name__, "exception_text": str(e)})
        try:
            lines = [
                "URBION SCHARMS EXPORT FORENSIC",
                f"EXACT URL: {EXACT}",
                f"UTC: {evidence['timestamp_utc']}",
                "",
                "COMPLETED SECTIONS",
                json.dumps(evidence["completed_sections"], indent=2),
                "",
                "FAILED SECTIONS",
                json.dumps(evidence["failed_sections"], indent=2),
                "",
                "TIMED-OUT SECTIONS",
                json.dumps(evidence["timed_out_sections"], indent=2),
                "",
                "HTTP PRIORITY",
                json.dumps(evidence.get("http_priority", {}), indent=2, ensure_ascii=False, default=str),
                "",
                "EXACT PNG32 CLIENTS",
                json.dumps(evidence.get("clients", {}), indent=2, ensure_ascii=False, default=str),
                "",
                "FORMAT / ORIGIN DIFFERENTIAL",
                json.dumps({"variants": evidence.get("variants", {}), "origin_tests": evidence.get("origin_tests", {})}, indent=2, ensure_ascii=False, default=str),
                "",
                "METADATA",
                json.dumps(evidence.get("metadata", {}), indent=2, ensure_ascii=False, default=str),
                "",
                "BROWSER / CDP",
                json.dumps(evidence.get("browser", {}), indent=2, ensure_ascii=False, default=str),
                "",
                "CLASSIFICATION",
                json.dumps(evidence.get("classification", {}), indent=2, ensure_ascii=False, default=str),
                "",
                "DIAGNOSTIC ERRORS",
                json.dumps(evidence.get("diagnostic_errors", []), indent=2, ensure_ascii=False, default=str),
            ]
            REPORT_TXT.write_text("\n".join(lines), encoding="utf-8")
        except Exception as e:
            evidence["diagnostic_errors"].append({"section": "write_text", "exception_type": type(e).__name__, "exception_text": str(e)})

    print(json.dumps(evidence.get("classification", {}), indent=2))
    print(f"REPORT_JSON={REPORT_JSON}")
    print(f"REPORT_TXT={REPORT_TXT}")
    print(f"RAW={RAW}")
    print(f"HEADERS={HEADERS_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
