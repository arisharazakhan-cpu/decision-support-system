from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.sla_definition import SLADefinition
from app.services.sla_eval import evaluate_sla


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(response: Response, db: Session = Depends(get_db)):
    slas = db.query(SLADefinition).filter(SLADefinition.is_active == True).all()

    as_of = datetime.now(timezone.utc).isoformat()

    if not slas:
        response.status_code = 204
        return {
            "as_of": as_of,
            "total_slas": 0,
            "passing": 0,
            "failing": 0,
            "no_data": 0,
            "overall_status": "no_slas_configured",
            "results": [],
        }

    results = [evaluate_sla(db, sla) for sla in slas]

    passing = sum(1 for r in results if r["status"] == "pass")
    failing = sum(1 for r in results if r["status"] == "fail")
    no_data = sum(1 for r in results if r["status"] == "no_data")

    if failing > 0:
        overall = "critical"
        response.status_code = 503
    elif no_data > 0:
        overall = "degraded"
        response.status_code = 206
    else:
        overall = "healthy"
        response.status_code = 200

    return {
        "as_of": as_of,
        "total_slas": len(results),
        "passing": passing,
        "failing": failing,
        "no_data": no_data,
        "overall_status": overall,
        "results": results,
    }