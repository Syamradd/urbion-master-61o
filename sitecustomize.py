"""URBION HORIZON runtime bootstrap.

This module is loaded by Python before the FastAPI application module. It keeps
business/API routes intact while enforcing the intended public entry flow:
landing page -> /championship.html workspace, plus the dedicated visual asset.
"""
from pathlib import Path
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import HTTPException

_ALLOWED = {
    'urbion_ui.js', 'urbion_championship_ui.js', 'urbion_championship_upgrade.js',
    'urbion_championship_dashboard.js', 'urbion_championship_polish.js',
    'urbion_championship_v279.js', 'urbion_public_source_ui.js',
    'urbion_public_spatial_v283.js', 'urbion_public_spatial_v284.js',
    'urbion_championship_visual_system_v1.js',
    'urbion_horizon_visual_overhaul.js',
}
_BASE = Path(__file__).resolve().parent

try:
    from fastapi import FastAPI

    _original_init = FastAPI.__init__
    _original_add_api_route = FastAPI.add_api_route
    _original_middleware = FastAPI.middleware

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
        inject = marker + '\n  <script src="/urbion_championship_visual_system_v1.js"></script>\n  <script src="/urbion_horizon_visual_overhaul.js"></script>'
        if marker in body and 'urbion_championship_visual_system_v1.js' not in body:
            body = body.replace(marker, inject, 1)
        elif 'urbion_horizon_visual_overhaul.js' not in body and '</body>' in body:
            body = body.replace('</body>', '<script src="/urbion_horizon_visual_overhaul.js"></script></body>', 1)
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
