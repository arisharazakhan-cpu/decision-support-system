from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.raw_event import RawEvent

router = APIRouter(prefix="/raw-events", tags=["raw-events"])


@router.get("")
def list_raw_events(limit: int = Query(50, ge=1, le=500)):
    db: Session = SessionLocal()
    try:
        rows = db.execute(
            select(RawEvent).order_by(RawEvent.event_time.desc()).limit(limit)
        ).scalars().all()

        return [
            {
                "id": r.id,
                "product_id": r.product_id,
                "source_id": r.source_id,
                "event_time": r.event_time.isoformat(),
                "payload": r.payload,
                "ingested_at": r.ingested_at.isoformat(),
            }
            for r in rows
        ]
    finally:
        db.close()
