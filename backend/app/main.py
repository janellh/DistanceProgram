import os, time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from .db import Base, engine
from . import models
from .api.v1.health import router as health_router
from .api.v1.distance import router as distance_router
from .api.v1.history import router as history_router
from .middleware.request_id import RequestIDMiddleware
from .middleware.rate_limit import RateLimitMiddleware


app = FastAPI(title="DistanceChallenge")

# ---------- DB init with retries ----------
@app.on_event("startup")
def init_db():
    for _ in range(20):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            time.sleep(1)
    Base.metadata.create_all(bind=engine)

# ---------- CORS (dev-friendly; tweak if you have settings) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Middlewares ----------
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)

# ---------- API ----------
app.include_router(health_router,  prefix="/api/v1", tags=["health"])
app.include_router(distance_router, prefix="/api/v1", tags=["distance"])
app.include_router(history_router,  prefix="/api/v1", tags=["history"])
app.include_router(health_router,  prefix="", tags=["health-legacy"])
app.include_router(distance_router, prefix="", tags=["distance-legacy"])
app.include_router(history_router,  prefix="", tags=["history-legacy"])


# ---------- Frontend (SPA) serving ----------
FRONTEND_DIR = os.getenv("FRONTEND_DIR", "static")  # /app/static at runtime

def _exists(p: str) -> bool:
    return os.path.exists(p)

# Mount whichever client asset dir exists (SvelteKit outputs "_app" or "assets")
for _candidate in ("_app", "assets"):
    _path = os.path.join(FRONTEND_DIR, _candidate)
    if os.path.isdir(_path):
        app.mount(f"/{_candidate}", StaticFiles(directory=_path), name=_candidate)

def _root_html_path() -> str:
    # Prefer SPA fallback 200.html; fall back to index.html
    p200 = os.path.join(FRONTEND_DIR, "200.html")
    if _exists(p200):
        return p200
    return os.path.join(FRONTEND_DIR, "index.html")

@app.get("/", response_class=HTMLResponse)
async def root():
    html = _root_html_path()
    if not _exists(html):
        listing = "\n".join(os.listdir(FRONTEND_DIR)) if os.path.isdir(FRONTEND_DIR) else "(dir missing)"
        return PlainTextResponse(
            f"Root HTML not found at {html}\nFRONTEND_DIR contents:\n{listing}",
            status_code=500
        )
    return FileResponse(html)

# SPA fallback: serve root HTML for unknown GET routes that aren't API
@app.exception_handler(StarletteHTTPException)
async def spa_fallback(request, exc: StarletteHTTPException):
    if request.url.path.startswith((
        "/api/v1/distance", "/api/v1/history", "/api/v1/healthz",
        "/distance", "/history", "/healthz"
    )):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    if request.method == "GET" and exc.status_code == 404:
        html = _root_html_path()
        if _exists(html):
            return FileResponse(html)
    return JSONResponse({"detail": exc.code if hasattr(exc, 'code') else exc.detail}, status_code=exc.status_code)
