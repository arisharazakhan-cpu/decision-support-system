from datetime import datetime, timezone
from math import ceil
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.raw_event import RawEvent
from app.models.metric_point import MetricPoint
from app.models.product import Product  # noqa: F401


METRIC_NAME = "latency_p95"


def percentile(values: list[float], p: float) -> float:
    if not values:
        raise ValueError("No values to compute percentile")
    values = sorted(values)
    k = ceil((p / 100.0) * len(values)) - 1
    k = max(0, min(k, len(values) - 1))
    return float(values[k])


def main():
    db: Session = SessionLocal()
    try:
        # for demo: compute p95 for the most recent product_id in raw_events
        latest = db.execute(select(RawEvent).order_by(RawEvent.id.desc()).limit(1)).scalar_one()
        product_id = latest.product_id

        rows = db.execute(
            select(RawEvent.payload)
            .where(RawEvent.product_id == product_id)
        ).all()

        latencies = []
        for (payload,) in rows:
            if isinstance(payload, dict) and "latency_ms" in payload:
                latencies.append(float(payload["latency_ms"]))

        p95 = percentile(latencies, 95)

        bucket = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

        mp = MetricPoint(
            product_id=product_id,
            metric_name=METRIC_NAME,
            ts_bucket=bucket.replace(tzinfo=None),
            value=p95,
        )
        db.add(mp)
        db.commit()

        print(f"Computed {METRIC_NAME} for product_id={product_id}: {p95} ms (bucket={bucket.isoformat()})")

    finally:
        db.close()


if __name__ == "__main__":
    main()
