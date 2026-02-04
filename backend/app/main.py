from fastapi import FastAPI
from app.routers.health import router as health_router
from app.db import engine

app = FastAPI(title="Decision Support System")

app.include_router(health_router)

@app.on_event("startup")
def startup_db_check():
    with engine.connect() as conn:
        print("Database connection successful")


