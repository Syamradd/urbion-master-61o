from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx
import requests
from playwright.sync_api import sync_playwright

BASE = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer"
BBOX = "102.18383789062501,2.28455066023697,102.19482421875,2.2955282141879016"
EXACT = BASE + "/export?" + urlencode({
    "bbox": BBOX, "bboxSR": "4326", "imageSR": "4326", "size": "256,256",
    "dpi": "96", "format": "png32", "transparent": "true", "layers": "show:0", "f": "image"
})
OUT = Path(os.environ.get("URBION_SCHARMS_FORENSIC_DIR", "/tmp/urbion-scharms-forensic"))
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw_response_png32.bin"
HEADERS_FILE = OUT / "response_headers.txt"
REPORT_JSON = OUT / "scharms_forensic.json"
REPORT_TXT = OUT / "scharms_forensic.txt"
ORIGIN = "https://urbion-horizon-championship.onrender.com"


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
    out = {"valid": None, "detail": None}
    if kind == "PNG":
        if len(body) < 24 or body[:8] != b"\x89PNG\r\n\x1a\n":
            return {"valid": False, "detail": "bad PNG signature"}
        pos = 8
        chunks = []
        try:
            while pos + 12 <= len(body):
                n = int.from_bytes(body[pos:pos+4], "big")
                typ = body[pos+4:pos+8]
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
        return {"valid": len(body) >= 4 and body[:3] == b"\xff\xd8\xff" and body[-2:] == b"\xff\xd9",
                "detail": "JPEG SOI/EOI check"}
    if kind == "GIF":
        return {"valid": len(body) >= 10 and body[-1:] == b";", "detail": "GIF header/trailer check"}
    return out


def headers_dict(headers):
    wanted = ["content-type","content-length","content-encoding","cache-control","etag","server","date","location",
              "x-content-type-options","access-control-allow-origin","access-control-allow-credentials","vary"]
    result = {}
    for k, v in headers.items():
        lk = k.lower()
        if lk in wanted or "arcgis" in lk or lk.startswith(("x-", "cf-", "akamai-", "server-timing")):
            result[lk] = v
    return result


def curl_get(url: str, headers=None, out_name="curl_body.bin"):
    body_path = OUT / out_name
    cmd = ["curl", "-sS", "-L", "-D", str(OUT / (out_name + ".headers")), "-o", str(body_path), "-w", "\\nCURL_FINAL_URL=%{url_effective}\\nCURL_STATUS=%{http_code}\\n", url]
    if headers:
        for k, v in headers.items(): cmd += ["-H", f"{k}: {v}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    verbose_cmd = ["curl", "-v", "-L", "--max-time", "45", "-o", "/dev/null", url]
    if headers:
        for k, v in headers.items(): verbose_cmd += ["-H", f"{k}: {v}"]
    v = subprocess.run(verbose_cmd, capture_output=True, text=True, timeout=60)
    (OUT / (out_name + ".verbose.txt")).write_text(v.stderr + "\\n" + v.stdout, encoding="utf-8")
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr,
            "body_file": str(body_path), "headers_file": str(OUT / (out_name + ".headers")),
            "verbose_file": str(OUT / (out_name + ".verbose.txt"))}


def request_one(url, headers=None, client_name="requests"):
    if client_name == "requests":
        r = requests.get(url, headers=headers or {}, allow_redirects=True, timeout=45)
    else:
        with httpx.Client(follow_redirects=True, timeout=45) as c: r = c.get(url, headers=headers or {})
    hops = [{"status": x.status_code, "url": str(x.url), "headers": headers_dict(x.headers), "location": x.headers.get("location")} for x in r.history]
    body = r.content
    return {"status": r.status_code, "url": str(r.url), "redirects": hops, "headers": headers_dict(r.headers),
            "body_length": len(body), "first64_hex": body[:64].hex(" "), "first64_text": body[:64].decode("utf-8", "replace"),
            "classification": classify(body, r.headers.get("content-type", "")),
            "image_validity": image_validity(body, classify(body)), "body_prefix_500": body[:500].decode("utf-8", "replace") if classify(body) not in ("PNG","JPEG","GIF","binary/unknown") else None,
            "body": body}


def variant_url(fmt=None, f="image"):
    q = {"bbox": BBOX, "bboxSR":"4326", "imageSR":"4326", "size":"256,256", "dpi":"96", "transparent":"true", "layers":"show:0", "f":f}
    if fmt: q["format"] = fmt
    return BASE + "/export?" + urlencode(q)


def main():
    evidence = {"exact_url": EXACT, "bbox": BBOX, "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "curl":{}, "clients":{}, "variants":{}, "origin_tests":{}, "metadata":{}, "browser":{}, "classification":{}}

    exact_curl = curl_get(EXACT, out_name="raw_response_png32.bin")
    evidence["curl"]["exact"] = exact_curl
    exact_req = request_one(EXACT, client_name="requests")
    raw_body = exact_req.pop("body")
    RAW.write_bytes(raw_body)
    HEADERS_FILE.write_text(json.dumps(exact_req["headers"], indent=2, sort_keys=True), encoding="utf-8")
    evidence["clients"]["requests_exact"] = exact_req
    evidence["clients"]["httpx_exact"] = {k:v for k,v in request_one(EXACT, client_name="httpx").items() if k != "body"}

    for label, fmt, f in [("png32","png32","image"),("png","png","image"),("jpg","jpg","image"),("json",None,"json")]:
        r = request_one(variant_url(fmt, f), client_name="requests")
        r.pop("body", None)
        evidence["variants"][label] = r

    for label, headers in [("no_origin",{}),("origin",{"Origin":ORIGIN}),("origin_referer",{"Origin":ORIGIN,"Referer":ORIGIN+"/"})]:
        r = request_one(EXACT, headers=headers, client_name="requests")
        r.pop("body", None)
        evidence["origin_tests"][label]=r

    for path in ["?f=json", "/0?f=json"]:
        r = request_one(BASE + path, client_name="requests")
        body = r.pop("body")
        evidence["metadata"][path] = r
        evidence["metadata"][path]["body_prefix_500"] = body[:500].decode("utf-8", "replace")
        try: evidence["metadata"][path]["json"] = json.loads(body.decode("utf-8"))
        except Exception: evidence["metadata"][path]["json_parse"] = False
    rp = request_one(variant_url("png32","pjson"), client_name="requests")
    body = rp.pop("body")
    evidence["metadata"]["export_pjson"] = rp
    evidence["metadata"]["export_pjson"]["body_prefix_500"] = body[:500].decode("utf-8", "replace")

    browser_trace=[]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        cdp = context.new_cdp_session(page)
        for method in ["Network.enable"]: cdp.send(method)
        def record(kind, payload):
            if isinstance(payload, dict) and any(x in str(payload.get("request",payload.get("response",{}))) for x in ["GTsemasa_04","scharms.planmalaysia.gov.my"]):
                browser_trace.append({"kind":kind,"payload":payload})
        for event in ["Network.requestWillBeSent","Network.responseReceived","Network.loadingFailed","Network.loadingFinished"]:
            cdp.on(event, lambda p, e=event: record(e,p))
        page.on("request", lambda r: browser_trace.append({"kind":"playwright.request","url":r.url,"headers":r.all_headers(),"resource_type":r.resource_type,"frame_url":r.frame.url if r.frame else None}) if "GTsemasa_04/MapServer/export" in r.url else None)
        page.on("response", lambda r: browser_trace.append({"kind":"playwright.response","url":r.url,"status":r.status,"headers":r.all_headers()}) if "GTsemasa_04/MapServer/export" in r.url else None)
        page.on("requestfinished", lambda r: browser_trace.append({"kind":"playwright.requestfinished","url":r.url}) if "GTsemasa_04/MapServer/export" in r.url else None)
        page.on("requestfailed", lambda r: browser_trace.append({"kind":"playwright.requestfailed","url":r.url,"failure":r.failure,"headers":r.all_headers(),"resource_type":r.resource_type}) if "GTsemasa_04/MapServer/export" in r.url else None)
        page.goto("data:text/html,<html><body></body></html>")
        control = "https://httpbin.org/image/png"
        control_img = page.evaluate("""async ({url,target}) => { const a={img:null,newImage:null,fetch:null,fetchError:null};
          const done=new Promise(resolve=>{let n=0, finish=()=>{if(++n===2)resolve();};
            const i=document.createElement('img'); i.onload=()=>{a.img='load';finish()}; i.onerror=e=>{a.img='error';finish()}; i.src=url; document.body.appendChild(i);
            const j=new Image(); j.onload=()=>{a.newImage='load'}; j.onerror=()=>{a.newImage='error'}; j.src=url; });
          try { const r=await fetch(url); a.fetch={ok:r.ok,status:r.status,type:r.type,contentType:r.headers.get('content-type')}; await r.arrayBuffer(); } catch(e) {a.fetchError=String(e)}
          await done; return a; }""", {"url":EXACT,"target":"scharms"})
        control_good = page.evaluate("""async url => { const out={}; const d=new Promise(resolve=>{const i=new Image();i.onload=()=>{out.img='load';resolve()};i.onerror=()=>{out.img='error';resolve()};i.src=url;document.body.appendChild(i)}); try{const r=await fetch(url);out.fetch={ok:r.ok,status:r.status,type:r.type}}catch(e){out.fetchError=String(e)} await d; return out;}""", control)
        # explicit CSS background control for SCHARMS
        css = page.evaluate("""url => new Promise(resolve => { const d=document.createElement('div'); d.style.width='1px';d.style.height='1px';d.style.backgroundImage=`url(${url})`;document.body.appendChild(d); setTimeout(()=>resolve(getComputedStyle(d).backgroundImage),3000); })""", EXACT)
        img_test = page.evaluate("""url => new Promise(resolve=>{const i=new Image(); const o={}; i.onload=()=>{o.event='load';o.complete=i.complete;o.naturalWidth=i.naturalWidth;o.naturalHeight=i.naturalHeight;resolve(o)}; i.onerror=()=>{o.event='error';o.complete=i.complete;o.naturalWidth=i.naturalWidth;o.naturalHeight=i.naturalHeight;resolve(o)}; i.src=url;})""", EXACT)
        fetch_test = page.evaluate("""async url=>{try{const r=await fetch(url);return {success:true,status:r.status,type:r.type,url:r.url,headers:Object.fromEntries(r.headers.entries())}}catch(e){return {success:false,error:String(e)}}}""", EXACT)
        browser.close()
    evidence["browser"]={"trace":browser_trace,"img":img_test,"fetch":fetch_test,"css":css,"good_control":control_good}

    browser_gt = [x for x in browser_trace if x.get("kind") in ("Network.responseReceived","Network.loadingFailed")]
    response_seen = any(x["kind"]=="Network.responseReceived" for x in browser_gt)
    fail = next((x for x in browser_gt if x["kind"]=="Network.loadingFailed"), None)
    ctype = exact_req.get("headers",{}).get("content-type","")
    cls = exact_req["classification"]
    status = exact_req["status"]
    if status >= 400: category = "6. HTTP error response"
    elif cls not in ("PNG","JPEG","GIF"): category = "7. invalid/non-image response body"
    elif response_seen and fail and fail.get("payload",{}).get("blockedReason"):
        category = "8. valid image + browser cross-origin delivery policy"
    elif response_seen and fail and fail.get("payload",{}).get("errorText") and "ORB" in str(fail):
        category = "9. invalid/missing response headers causing ORB"
    elif not response_seen and fail and "BLOCKED_BY_ORB" in str(fail):
        category = "9. invalid/missing response headers causing ORB"
    elif status == 200 and cls in ("PNG","JPEG","GIF"):
        category = "8. valid image + browser cross-origin delivery policy"
    else: category = "11. other"
    confidence = "HIGH" if status == 200 and cls in ("PNG","JPEG","GIF") and fail else "MEDIUM"
    evidence["classification"]={"primary":category,"confidence":confidence,"proof":[
        f"curl/requests status={status}", f"body classification={cls}", f"body length={len(raw_body)}",
        f"PNG signature={raw_body[:8].hex(' ')}", f"browser responseReceived={response_seen}", f"browser loadingFailed={bool(fail)}",
        f"browser failure={fail.get('payload',{}).get('errorText') if fail else None}"]}

    REPORT_JSON.write_text(json.dumps(evidence, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    lines=["URBION SCHARMS EXPORT FORENSIC", f"EXACT URL: {EXACT}", f"UTC: {evidence['timestamp_utc']}", "", "EXACT PNG32 RESPONSE",
           json.dumps(exact_req, indent=2, ensure_ascii=False), "", "ORIGIN DIFFERENTIAL", json.dumps(evidence["origin_tests"], indent=2, ensure_ascii=False),
           "", "FORMAT DIFFERENTIAL", json.dumps(evidence["variants"], indent=2, ensure_ascii=False), "", "BROWSER", json.dumps(evidence["browser"], indent=2, ensure_ascii=False),
           "", "CLASSIFICATION", json.dumps(evidence["classification"], indent=2, ensure_ascii=False)]
    REPORT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence["classification"], indent=2))
    print(f"REPORT_JSON={REPORT_JSON}")
    print(f"REPORT_TXT={REPORT_TXT}")
    print(f"RAW={RAW}")
    print(f"HEADERS={HEADERS_FILE}")


if __name__ == "__main__": main()
