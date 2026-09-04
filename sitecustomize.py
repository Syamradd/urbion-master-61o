"""MASTER-285: expose repository-owned JS assets to the FastAPI app.

Python loads sitecustomize during interpreter startup. We patch FastAPI's constructor
so the existing app gains a narrow, allow-listed JavaScript asset route without
changing application business logic or endpoint contracts.
"""
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import HTTPException

_ALLOWED = {
    'urbion_ui.js', 'urbion_championship_ui.js', 'urbion_championship_upgrade.js',
    'urbion_championship_dashboard.js', 'urbion_championship_polish.js',
    'urbion_championship_v279.js', 'urbion_public_source_ui.js',
    'urbion_public_spatial_v283.js', 'urbion_public_spatial_v284.js',
}
_BASE = Path(__file__).resolve().parent

try:
    from fastapi import FastAPI
    _original_init = FastAPI.__init__
    def _init_with_assets(self, *args, **kwargs):
        _original_init(self, *args, **kwargs)
        def _asset(asset: str):
            filename = asset + '.js'
            if filename not in _ALLOWED:
                raise HTTPException(status_code=404, detail='Unknown frontend asset')
            target = (_BASE / filename).resolve()
            if target.parent != _BASE or not target.is_file():
                raise HTTPException(status_code=404, detail='Frontend asset not found')
            return FileResponse(target, media_type='application/javascript', headers={'Cache-Control':'no-store'})
        self.add_api_route('/{asset}.js', _asset, methods=['GET'], include_in_schema=False)
    FastAPI.__init__ = _init_with_assets
except Exception:
    pass
