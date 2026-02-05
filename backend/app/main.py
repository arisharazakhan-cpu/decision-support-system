from fastapi import FastAPI

from app.db import engine
from app.routers.health import router as health_router
from app.routers.raw_events import router as raw_events_router

app = FastAPI(title="Decision Support System")

# routers
app.include_router(health_router)
app.include_router(raw_events_router)

@app.on_event("startup")
def startup_db_check():
    with engine.connect() as conn:
        print("Database connection successful")



