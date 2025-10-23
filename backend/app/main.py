import os
import time
import httpx
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import QueryRecord
from .schemas import DistanceRequest, DistanceResponse, HistoryResponse, HistoryItem
from .security import is_safe
from .utils import haversine_km
from .rate_limit import allow as rate_allow

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

# ---------- Rate limiting middleware ----------
@app.middleware("http")
async def rate_limit_mw(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    if request.url.path.startswith(("/distance", "/history")):
        if not rate_allow(ip):
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
    return await call_next(request)

# ---------- API ----------
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
UA = os.getenv("NOMINATIM_UA", "DistanceChallenge/1.0 (contact@example.com)")

@app.post("/distance", response_model=DistanceResponse)
async def distance(payload: DistanceRequest, db: Session = Depends(get_db)):
    src = payload.source.strip()
    dst = payload.destination.strip()
    if not (is_safe(src) and is_safe(dst)):
        raise HTTPException(status_code=422, detail="Invalid characters in address.")

    params = {"format": "json", "limit": 1}
    headers = {"User-Agent": UA}

    async def geocode(q: str):
        for i in range(3):
            try:
                timeout = httpx.Timeout(10.0)
                async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
                    r = await client.get(NOMINATIM_URL, params={**params, "q": q})
                    r.raise_for_status()
                    data = r.json()
                    if not data:
                        return None
                    return float(data[0]["lat"]), float(data[0]["lon"])
            except Exception:
                if i == 2:
                    return None
                await asyncio.sleep(0.5 * (i + 1))  # gentle backoff

    s = await geocode(src)
    d = await geocode(dst)
    if not s or not d:
        raise HTTPException(status_code=400, detail="Unable to geocode one or both addresses.")

    km = haversine_km(s[0], s[1], d[0], d[1])
    mi = km * 0.621371

    rec = QueryRecord(
        source_raw=src, dest_raw=dst,
        source_lat=s[0], source_lon=s[1],
        dest_lat=d[0], dest_lon=d[1],
        distance_km=km, distance_mi=mi,
    )
    db.add(rec)
    db.commit()

    return {"km": round(km, 3), "mi": round(mi, 3)}

@app.get("/history", response_model=HistoryResponse)
async def history(db: Session = Depends(get_db)):
    rows = db.query(QueryRecord).order_by(QueryRecord.id.desc()).limit(50).all()
    items = [
        HistoryItem(
            id=r.id,
            source=r.source_raw,
            destination=r.dest_raw,
            km=round(r.distance_km, 3),
            mi=round(r.distance_mi, 3),
            created_at=r.created_at.isoformat() if r.created_at else ""
        )
        for r in rows
    ]
    return {"items": items}

@app.get("/healthz")
async def healthz():
    return {"ok": True}

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
async def spa_fallback(request: Request, exc: StarletteHTTPException):
    api_roots = ("/distance", "/history", "/healthz")
    if request.url.path.startswith(api_roots):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    if request.method == "GET" and exc.status_code == 404:
        html = _root_html_path()
        if _exists(html):
            return FileResponse(html)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
