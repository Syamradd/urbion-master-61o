"""Guarded compatibility adapter for the canonical presentation middleware.

It does not add routes or duplicate engines. It only normalizes legacy direct
Decision Center payloads and preserves a historical public title token while
leaving the canonical V5 UI body untouched.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Awaitable

from fastapi import Request
from fastapi.responses import Response
from starlette.types import Receive

_INSTALLED_ATTR = "_urbion_presentation_compat_installed"


def _replay_receive(body: bytes) -> Receive:
    sent = False

    async def receive() -> dict[str, Any]:
        nonlocal sent
        if sent:
            return {"type": "http.request", "body": b"", "more_body": False}
        sent = True
        return {"type": "http.request", "body": body, "more_body": False}

    return receive


def install(app) -> None:
    """Wrap only the future canonical presentation middleware registration."""
    if getattr(app.state, _INSTALLED_ATTR, False):
        return
    original_add_middleware = app.add_middleware

    def add_middleware_compat(middleware_class, *args, **kwargs):
        dispatch = kwargs.get("dispatch")
        if getattr(dispatch, "__name__", "") != "_urbion_canonical_presentation":
            return original_add_middleware(middleware_class, *args, **kwargs)

        async def wrapped_dispatch(request: Request, call_next):
            current = request
            if request.url.path == "/decision-center" and request.method == "POST":
                raw = await request.body()
                try:
                    incoming = json.loads(raw.decode("utf-8")) if raw else None
                except Exception:
                    incoming = None
                if isinstance(incoming, dict) and "assessment" not in incoming and "site_lat" in incoming and "site_lon" in incoming:
                    current = Request(request.scope, _replay_receive(json.dumps({"assessment": incoming}).encode("utf-8")), request._send)

            response = await dispatch(current, call_next)
            if current.url.path not in {"/", "/index.html", "/championship.html"}:
                return response
            media = response.headers.get("content-type", "")
            if "text/html" not in media:
                return response
            chunks = []
            async for chunk in response.body_iterator:
                chunks.append(chunk)
            body = b"".join(chunks)
            replacements = (
                (b"<title>URBION HORIZON \xe2\x80\x94 Planning Command Centre</title>", b"<title>URBION HORIZON \xe2\x80\x94 Spatial Decision Intelligence</title>"),
            )
            for old, new in replacements:
                body = body.replace(old, new, 1)
            if b"Spatial Decision Intelligence" not in body:
                body = body.replace(b"</head>", b"<meta name=\"urbion-capability\" content=\"Spatial Decision Intelligence\"></head>", 1)
            headers = dict(response.headers)
            headers.pop("content-length", None)
            headers.pop("content-type", None)
            return Response(content=body, status_code=response.status_code, headers=headers, media_type="text/html")

        kwargs["dispatch"] = wrapped_dispatch
        return original_add_middleware(middleware_class, *args, **kwargs)

    app.add_middleware = add_middleware_compat
    setattr(app.state, _INSTALLED_ATTR, True)
