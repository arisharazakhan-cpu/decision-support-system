from fastapi import FastAPI

import app.models # noqa: F401

from app.db import engine
from app.routers.health import router as health_router
from app.routers.raw_events import router as raw_events_router
from app.routers.metrics import router as metrics_router
from app.routers.sla import router as sla_router
from app.routers.dashboard import router as dashboard_router
from app.routers.healthz import router as healthz_router

app = FastAPI(title="Decision Support System")

app.include_router(health_router)
app.include_router(raw_events_router)
app.include_router(metrics_router)
app.include_router(sla_router)
app.include_router(dashboard_router)
app.include_router(healthz_router)

@app.on_event("startup")
def startup_db_check():
    with engine.connect() as conn:
        print("Database connection successful")



