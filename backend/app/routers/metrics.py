from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.metric_point import MetricPoint

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/latency/p95")
def get_latency_p95(
    product_id: int = Query(...),
    limit: int = Query(24, ge=1, le=500),
):
    db: Session = SessionLocal()
    try:
        rows = db.execute(
            select(MetricPoint)
            .where(
                MetricPoint.product_id == product_id,
                MetricPoint.metric_name == "latency_p95",
            )
            .order_by(MetricPoint.ts_bucket.desc())
            .limit(limit)
        ).scalars().all()

        return [
            {
                "ts_bucket": r.ts_bucket.isoformat(),
                "value": r.value,
                "computed_at": r.computed_at.isoformat(),
            }
            for r in rows
        ]
    finally:
        db.close()
