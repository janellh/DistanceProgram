from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc

from ...db import get_db
from ...models import QueryRecord
from ...schemas import HistoryResponse, HistoryItem

router = APIRouter()

@router.get("/history", response_model=HistoryResponse)
def history(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
):
    rows = db.execute(
        select(QueryRecord).order_by(desc(QueryRecord.id)).limit(limit)
    ).scalars().all()

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
