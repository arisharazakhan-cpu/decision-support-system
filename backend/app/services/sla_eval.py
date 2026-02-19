from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.metric_point import MetricPoint
from app.models.sla_definition import SLADefinition


def evaluate_sla(db: Session, sla: SLADefinition) -> dict:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=int(sla.window_minutes))

    # SLA uses metric_key, metric_points uses metric_name
    # Now we correctly link via MetricPoint.data_source_id
    value = (
        db.query(func.avg(MetricPoint.value))
        .filter(MetricPoint.data_source_id == sla.data_source_id)
        .filter(MetricPoint.metric_name == sla.metric_key)
        .filter(MetricPoint.computed_at >= window_start)
        .scalar()
    )

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
            "window_start": window_start.isoformat(),
            "window_end": now.isoformat(),
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
        "window_start": window_start.isoformat(),
        "window_end": now.isoformat(),
    }