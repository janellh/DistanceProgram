import os, httpx, asyncio
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ...db import get_db
from ...schemas import DistanceRequest, DistanceResponse
from ...security import is_safe
from ...utils import haversine_km

router = APIRouter()

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
UA = os.getenv("NOMINATIM_UA", "DistanceChallenge/1.0 (contact@example.com)")

@router.post("/distance", response_model=DistanceResponse)
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
                await asyncio.sleep(0.5 * (i + 1))

    s = await geocode(src)
    d = await geocode(dst)
    if not s or not d:
        raise HTTPException(status_code=400, detail="Unable to geocode one or both addresses.")

    km = haversine_km(s[0], s[1], d[0], d[1])
    mi = km * 0.621371

    # Persist using your existing model
    from app.models import QueryRecord
    rec = QueryRecord(
        source_raw=src, dest_raw=dst,
        source_lat=s[0], source_lon=s[1],
        dest_lat=d[0], dest_lon=d[1],
        distance_km=km, distance_mi=mi,
    )
    db.add(rec)
    db.commit()

    return {"km": round(km, 3), "mi": round(mi, 3)}
