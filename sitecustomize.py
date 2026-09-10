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
}
_BASE = Path(__file__).resolve().parent

try:
    from fastapi import FastAPI

    _original_init = FastAPI.__init__
    _original_add_api_route = FastAPI.add_api_route
    _original_middleware = FastAPI.middleware

    def _landing():
        target = (_BASE / 'index.html').resolve()
        if target.parent != _BASE or not target.is_file():
            raise HTTPException(status_code=404, detail='Landing frontend not found')
        return FileResponse(target, media_type='text/html', headers={'Cache-Control': 'no-store, max-age=0'})

    def _workspace():
        from championship_server import _frontend_root
        response = _frontend_root()
        body = response.body.decode('utf-8')
        marker = '<script src="/urbion_championship_horizon_ui.js"></script>'
        inject = marker + '\n  <script src="/urbion_championship_visual_system_v1.js"></script>'
        if marker in body and 'urbion_championship_visual_system_v1.js' not in body:
            body = body.replace(marker, inject, 1)
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
