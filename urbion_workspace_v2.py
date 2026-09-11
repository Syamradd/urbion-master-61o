from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from server import app

BASE_DIR = Path(__file__).resolve().parent


def _workspace_v2() -> HTMLResponse:
    target = BASE_DIR / "workspace_v2.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Workspace V2 frontend is missing")
    return HTMLResponse(
        target.read_text(encoding="utf-8"),
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


app.add_api_route("/workspace-v2.html", _workspace_v2, methods=["GET"], include_in_schema=False)
