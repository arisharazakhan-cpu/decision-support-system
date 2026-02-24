from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.metric_point import MetricPoint
from app.models.sla_definition import SLADefinition


def evaluate_sla(db: Session, sla: SLADefinition) -> dict:
    # MySQL DATETIME is timezone naive, so treat stored timestamps as naive UTC
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=sla.window_minutes)

    q = (
        db.query(func.avg(MetricPoint.value))
        .filter(MetricPoint.product_id == sla.data_source_id)
        .filter(MetricPoint.metric_name == sla.metric_key)
        .filter(MetricPoint.computed_at >= window_start)
    )

    value = q.scalar()

    def iso_utc(dt: datetime) -> str:
        return dt.replace(tzinfo=timezone.utc).isoformat()

    if value is None:
        return {
            "sla_id": sla.id,
            "name": sla.name,
            "status": "no_data",
            "observed": None,
            "threshold": float(sla.threshold),
            "window_minutes": int(sla.window_minutes),
            "metric_key": sla.metric_key,
            "statistic": sla.statistic,
            "window_start": iso_utc(window_start),
            "window_end": iso_utc(now),
        }

    passed = float(value) <= float(sla.threshold)

    return {
        "sla_id": sla.id,
        "name": sla.name,
        "status": "pass" if passed else "fail",
        "observed": float(value),
        "threshold": float(sla.threshold),
        "window_minutes": int(sla.window_minutes),
        "metric_key": sla.metric_key,
        "statistic": sla.statistic,
        "window_start": iso_utc(window_start),
        "window_end": iso_utc(now),
    }