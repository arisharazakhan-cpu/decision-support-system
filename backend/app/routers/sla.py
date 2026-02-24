from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.sla_definition import SLADefinition
from app.services.sla_eval import evaluate_sla


router = APIRouter(prefix="/sla-definitions", tags=["SLA"])


class SLACreate(BaseModel):
    name: str
    data_source_id: int
    threshold: float
    window_minutes: int = 60
    metric_key: str = "latency_ms"
    statistic: str = "p95"
    is_active: bool = True


class SLAUpdate(BaseModel):
    name: str | None = None
    threshold: float | None = None
    window_minutes: int | None = None
    metric_key: str | None = None
    statistic: str | None = None
    is_active: bool | None = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sla(payload: SLACreate, db: Session = Depends(get_db)):
    sla = SLADefinition(
        name=payload.name,
        data_source_id=payload.data_source_id,
        threshold=payload.threshold,
        window_minutes=payload.window_minutes,
        metric_key=payload.metric_key,
        statistic=payload.statistic,
        is_active=payload.is_active,
    )
    db.add(sla)
    db.commit()
    db.refresh(sla)
    return sla


@router.get("/")
def list_slas(db: Session = Depends(get_db)):
    return db.query(SLADefinition).all()


@router.get("/{sla_id}")
def get_sla(sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLADefinition).filter(SLADefinition.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return sla


@router.patch("/{sla_id}")
def update_sla(sla_id: int, payload: SLAUpdate, db: Session = Depends(get_db)):
    sla = db.query(SLADefinition).filter(SLADefinition.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")

    update_data = payload.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(sla, key, value)

    db.commit()
    db.refresh(sla)
    return sla


@router.delete("/{sla_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sla(sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLADefinition).filter(SLADefinition.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")

    db.delete(sla)
    db.commit()
    return


@router.get("/evaluate/all")
def evaluate_all_slas(db: Session = Depends(get_db)):
    slas = db.query(SLADefinition).all()
    return [evaluate_sla(db, sla) for sla in slas]


@router.get("/{sla_id}/evaluate")
def evaluate_one_sla(sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLADefinition).filter(SLADefinition.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return evaluate_sla(db, sla)