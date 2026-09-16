"""URBION HORIZON runtime bootstrap.

This module is loaded by Python before the FastAPI application module. It keeps
business/API routes intact while enforcing the intended public entry flow:
landing page -> /championship.html workspace, plus the dedicated visual assets.
"""
from pathlib import Path
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi import HTTPException, Request

_ALLOWED = {
    'urbion_ui.js', 'urbion_championship_ui.js', 'urbion_championship_upgrade.js',
    'urbion_championship_dashboard.js', 'urbion_championship_polish.js',
    'urbion_championship_v279.js', 'urbion_public_source_ui.js',
    'urbion_public_spatial_v283.js', 'urbion_public_spatial_v284.js',
    'urbion_championship_visual_system_v1.js',
    'urbion_horizon_visual_overhaul.js',
    'urbion_championship_visual_system_v2.js',
}
_BASE = Path(__file__).resolve().parent

try:
    import asyncio
    import httpx

    _original_get = httpx.AsyncClient.get
    _original_request = httpx.AsyncClient.request
    _GIS_DIRECT_RETRY_LAYERS = {
        "iplan:rsn",
        "iplan:risiko_bencana",
        "iplan:hutan",
        "iplan:rumah_mampu_milik",
    }
    _GIS_GWC_PATH = "/geoserver/gwc/service/wms"
    _GIS_DIRECT_WMS = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
    _GIS_ARCGIS_FALLBACKS = {
        "iplan:hutan": (
            "https://gisdev.planmalaysia.gov.my/server/rest/services/RFN4/04_PERANCANGAN_ALAM_SEKITAR/MapServer",
            5,
        ),
        "iplan:risiko_bencana": (
            "https://gisdev.planmalaysia.gov.my/server/rest/services/RFN4/04_PERANCANGAN_ALAM_SEKITAR/MapServer",
            12,
        ),
    }

    def _direct_wms_variants(params):
        base = dict(params or {})
        base.pop("tiled", None)
        base.pop("tilesorigin", None)
        base.setdefault("format", "image/png")
        base.setdefault("version", "1.1.1")
        base.setdefault("request", "GetMap")
        base.setdefault("service", "WMS")
        variants = [base]
        spatial = str(base.get("srs") or base.get("crs") or "")
        if spatial.upper() == "EPSG:3857":
            alt = dict(base)
            alt["srs"] = "EPSG:900913"
            alt.pop("crs", None)
            variants.append(alt)
        return variants

    def _arcgis_image_params(params, layer_id):
        spatial_ref = str(params.get("srs") or params.get("crs") or "EPSG:3857").upper()
        wkid = "4326" if spatial_ref.endswith(":4326") else "3857"
        return {
            "bbox": str(params.get("bbox", "")),
            "bboxSR": wkid,
            "imageSR": wkid,
            "size": f"{params.get('width', '256')},{params.get('height', '256')}",
            "dpi": "96",
            "format": "png32",
            "transparent": str(params.get("transparent", "true")),
            "f": "image",
            "layers": f"show:{layer_id}",
        }

    async def _get_with_authoritative_retry(self, url, *args, **kwargs):
        response = None
        error = None
        try:
            response = await _original_get(self, url, *args, **kwargs)
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            error = exc

        parsed_url = str(url)
        params = kwargs.get("params")
        layer = None
        if isinstance(params, dict):
            layer = str(params.get("layers") or "")
        should_retry = _GIS_GWC_PATH in parsed_url and layer in _GIS_DIRECT_RETRY_LAYERS

        if not should_retry:
            if response is not None:
                return response
            if error is not None:
                raise error
            raise httpx.ConnectError("GIS upstream request failed")

        original_ok = (
            response is not None
            and response.status_code == 200
            and response.headers.get("content-type", "").lower().startswith("image/")
        )
        if original_ok:
            return response

        # Some i-Plan GWC layers are exposed on EPSG:900913 even when the
        # browser asks for EPSG:3857. Retry the authoritative tile endpoint
        # with the alternate gridset before falling back to untiled WMS.
        if layer == "iplan:rsn" and isinstance(params, dict):
            spatial = str(params.get("srs") or params.get("crs") or "")
            if spatial.upper() == "EPSG:3857":
                alt = dict(params)
                alt["srs"] = "EPSG:900913"
                alt.pop("crs", None)
                try:
                    gwc_alt = await _original_get(self, url, params=alt)
                except (httpx.HTTPError, asyncio.TimeoutError):
                    gwc_alt = None
                if gwc_alt is not None and gwc_alt.status_code == 200 and gwc_alt.headers.get("content-type", "").lower().startswith("image/"):
                    gwc_alt.headers["X-URBION-GIS-Fallback"] = "PLANMalaysia-GWC-EPSG900913"
                    return gwc_alt

        # First try the direct i-Plan WMS with both 3857 and 900913 variants.
        for direct_params in _direct_wms_variants(params):
            try:
                direct = await _original_request(self, "GET", _GIS_DIRECT_WMS, params=direct_params)
            except (httpx.HTTPError, asyncio.TimeoutError):
                continue
            if direct.status_code == 200 and direct.headers.get("content-type", "").lower().startswith("image/"):
                direct.headers["X-URBION-GIS-Fallback"] = "PLANMalaysia-WMS-DIRECT-RETRY"
                return direct

        # HUTAN and RISIKO have verified current official PLANMalaysia GISDev
        # MapServer layers with exact semantic matches (IDs 5 and 12).
        arcgis_target = _GIS_ARCGIS_FALLBACKS.get(layer)
        if arcgis_target:
            service_url, layer_id = arcgis_target
            try:
                arcgis = await _original_request(
                    self,
                    "GET",
                    service_url + "/export",
                    params=_arcgis_image_params(params, layer_id),
                )
            except (httpx.HTTPError, asyncio.TimeoutError):
                arcgis = None
            if arcgis is not None and arcgis.status_code == 200 and arcgis.headers.get("content-type", "").lower().startswith("image/"):
                arcgis.headers["X-URBION-GIS-Fallback"] = "PLANMalaysia-GISDev-ArcGIS-RFN4"
                return arcgis

        if response is not None:
            return response
        if error is not None:
            raise error
        raise httpx.ConnectError("GIS GWC and authoritative render fallbacks failed")

    if not getattr(httpx.AsyncClient.get, "__urbion_authoritative_retry_v2__", False):
        _get_with_authoritative_retry.__urbion_authoritative_retry_v2__ = True
        httpx.AsyncClient.get = _get_with_authoritative_retry
except Exception:
    pass

try:
    from fastapi import FastAPI
    _original_init = FastAPI.__init__
    _original_add_api_route = FastAPI.add_api_route
    _original_middleware = FastAPI.middleware

    async def _legend_proxy(request: Request):
        layer = str(request.query_params.get("layer", "")).strip()
        if not layer.startswith("iplan:"):
            raise HTTPException(status_code=400, detail="Legend layer is not in the allow-listed i-Plan namespace")
        upstream_params = {
            "REQUEST": "GetLegendGraphic",
            "VERSION": str(request.query_params.get("version", "1.1.1")),
            "FORMAT": "image/png",
            "LAYER": layer,
            "STYLE": str(request.query_params.get("style", "")),
            "LEGEND_OPTIONS": str(request.query_params.get("legend_options", "forceLabels:on;fontAntiAliasing:true")),
        }
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                upstream = await client.get(_GIS_DIRECT_WMS, params=upstream_params, headers={"Accept": "image/png,image/*;q=0.9"})
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            raise HTTPException(status_code=502, detail=f"i-Plan legend upstream unavailable: {exc}")
        content_type = upstream.headers.get("content-type", "")
        if upstream.status_code == 200 and content_type.lower().startswith("image/") and len(upstream.content) > 32:
            media_type = content_type.split(";", 1)[0].strip() or "image/png"
            return Response(
                content=upstream.content,
                status_code=200,
                media_type=media_type,
                headers={"Cache-Control": "no-store, max-age=0", "X-URBION-GIS-Fallback": "PLANMalaysia-WMS-LEGEND"},
            )
        raise HTTPException(status_code=502, detail=f"i-Plan legend upstream render failed: HTTP={upstream.status_code} CT={content_type or '-'}")

    def _landing():
        target = (_BASE / 'urbion_horizon_landing.html').resolve()
        if target.parent != _BASE or not target.is_file():
            raise HTTPException(status_code=404, detail='Landing frontend not found')
        body = target.read_text(encoding='utf-8')
        visual_script = '<script src="/urbion_horizon_visual_overhaul.js"></script>'
        welcome_strip = '''
<section class="hz-welcome-strip" aria-label="SMART CITY and About URBION HORIZON">
  <div class="hz-welcome-kicker">SMART CITY · SPATIAL DECISION INTELLIGENCE</div>
  <div class="hz-welcome-grid">
    <div><strong>SMART CITY CONTEXT</strong><span>Connect spatial signals, planning evidence, policy and scenario intelligence before action.</span></div>
    <div><strong>ABOUT URBION HORIZON</strong><span>Built around evidence-first planning, explainable intelligence and planner-in-the-loop review.</span></div>
    <a href="/about.html"><strong>MEET THE PROJECT →</strong><span>Mission, principles, capabilities and team.</span></a>
  </div>
</section>
<style>
.hz-welcome-strip{margin:0 0 82px;padding:22px;border:1px solid rgba(83,209,224,.16);border-radius:20px;background:linear-gradient(145deg,rgba(7,28,42,.82),rgba(2,14,23,.94));box-shadow:0 24px 70px rgba(0,0,0,.24);position:relative;overflow:hidden}
.hz-welcome-strip:before{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 0 38%,rgba(67,231,238,.045) 52%,transparent 70%);animation:hzWelcomeSweep 9s ease-in-out infinite;pointer-events:none}
.hz-welcome-kicker{font:900 9px Inter,sans-serif;letter-spacing:.18em;color:#61efc6;margin-bottom:14px;position:relative;z-index:1}
.hz-welcome-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;position:relative;z-index:1}.hz-welcome-grid>div,.hz-welcome-grid>a{padding:15px;border:1px solid rgba(83,209,224,.11);border-radius:12px;background:rgba(255,255,255,.018);text-decoration:none}
.hz-welcome-grid strong{display:block;font:700 11px 'Space Grotesk',sans-serif;color:#edfaff}.hz-welcome-grid span{display:block;font:500 9px/1.55 Inter,sans-serif;color:#8da9b5;margin-top:6px}
@keyframes hzWelcomeSweep{0%,100%{transform:translateX(-20%);opacity:.35}50%{transform:translateX(16%);opacity:1}}
@media(max-width:800px){.hz-welcome-grid{grid-template-columns:1fr}.hz-welcome-strip{margin-bottom:60px}}
</style>
'''
        if 'hz-welcome-strip' not in body and '</main>' in body:
            body = body.replace('</main>', welcome_strip + '</main>', 1)
        if visual_script not in body and '</body>' in body:
            body = body.replace('</body>', visual_script + '</body>', 1)
        return HTMLResponse(body, media_type='text/html; charset=utf-8', headers={'Cache-Control': 'no-store, max-age=0'})

    def _workspace():
        from championship_server import _frontend_root
        response = _frontend_root()
        body = response.body.decode('utf-8')
        marker = '<script src="/urbion_championship_horizon_ui.js"></script>'
        legend_guard = r'''<script>
(()=>{
  const normalize=(value)=>{
    try{
      const raw=String(value||'');
      if(!raw.includes('GetLegendGraphic'))return value;
      const u=new URL(raw,location.href);
      if(!u.hostname.includes('iplan.planmalaysia.gov.my'))return value;
      const layer=u.searchParams.get('LAYER')||u.searchParams.get('layer')||'';
      if(!layer.startsWith('iplan:'))return value;
      const q=new URLSearchParams();
      q.set('layer',layer); q.set('version',u.searchParams.get('VERSION')||u.searchParams.get('version')||'1.1.1');
      q.set('style',u.searchParams.get('STYLE')||u.searchParams.get('style')||'');
      q.set('legend_options',u.searchParams.get('LEGEND_OPTIONS')||u.searchParams.get('legend_options')||'forceLabels:on;fontAntiAliasing:true');
      return '/map/legend?'+q.toString();
    }catch(_){return value}
  };
  const desc=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,'src');
  if(desc&&desc.set&&!desc.set.__urbionLegendProxy){
    const setter=desc.set;
    const wrapped=function(v){return setter.call(this,normalize(v))};
    Object.defineProperty(wrapped,'__urbionLegendProxy',{value:true});
    Object.defineProperty(HTMLImageElement.prototype,'src',{...desc,set:wrapped});
  }
  const setAttr=Element.prototype.setAttribute;
  if(!setAttr.__urbionLegendProxy){
    const wrapped=function(name,value){return setAttr.call(this,String(name).toLowerCase()==='src'?normalize(value):value)};
    Object.defineProperty(wrapped,'__urbionLegendProxy',{value:true});
    Element.prototype.setAttribute=wrapped;
  }
  const fix=()=>document.querySelectorAll('img[src*="GetLegendGraphic"],img[src*="getlegendgraphic"]').forEach(img=>{const next=normalize(img.src);if(next&&next!==img.src)img.src=next});
  new MutationObserver(fix).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['src']});
  fix();
})();
</script>'''
        inject = marker + '\n  <script src="/urbion_championship_visual_system_v1.js"></script>\n  <script src="/urbion_horizon_visual_overhaul.js"></script>\n  <script src="/urbion_championship_visual_system_v2.js"></script>\n  ' + legend_guard
        if marker in body and 'GetLegendGraphic' not in body:
            body = body.replace(marker, inject, 1)
        else:
            if 'urbion_horizon_visual_overhaul.js' not in body and '</body>' in body:
                body = body.replace('</body>', '<script src="/urbion_horizon_visual_overhaul.js"></script></body>', 1)
            if 'urbion_championship_visual_system_v2.js' not in body and '</body>' in body:
                body = body.replace('</body>', '<script src="/urbion_championship_visual_system_v2.js"></script></body>', 1)
            if 'GetLegendGraphic' not in body and '</body>' in body:
                body = body.replace('</body>', legend_guard + '</body>', 1)
        return HTMLResponse(body, media_type='text/html; charset=utf-8', headers={'Cache-Control': 'no-store, max-age=0'})

    def _asset(asset: str):
        filename = asset + '.js'
        if filename not in _ALLOWED:
            raise HTTPException(status_code=404, detail='Unknown frontend asset')
        target = (_BASE / filename).resolve()
        if target.parent != _BASE or not target.is_file():
            raise HTTPException(status_code=404, detail='Frontend asset not found')
        return FileResponse(target, media_type='application/javascript', headers={'Cache-Control': 'no-store, max-age=0'})

    def _init_with_assets(self, *args, **kwargs):
        _original_init(self, *args, **kwargs)
        self.add_api_route('/{asset}.js', _asset, methods=['GET'], include_in_schema=False)
        self.add_api_route('/map/legend', _legend_proxy, methods=['GET'], include_in_schema=False)
        self.add_api_route('/', _landing, methods=['GET'], include_in_schema=False)

    def _add_api_route(self, path, endpoint, *args, **kwargs):
        if path in {'/', '/index.html'}:
            return _original_add_api_route(self, path, _landing, *args, **kwargs)
        if path == '/championship.html':
            return _original_add_api_route(self, path, _workspace, *args, **kwargs)
        return _original_add_api_route(self, path, endpoint, *args, **kwargs)

    def _middleware(self, middleware_type):
        decorator = _original_middleware(self, middleware_type)
        def register(func):
            if getattr(func, '__name__', '') == '_championship_frontend_override':
                return func
            return decorator(func)
        return register

    FastAPI.__init__ = _init_with_assets
    FastAPI.add_api_route = _add_api_route
    FastAPI.middleware = _middleware
except Exception:
    pass
