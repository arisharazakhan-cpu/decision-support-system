# Decision Support System – SLA Monitoring Service

## Overview

This project implements a simplified enterprise-style SLA monitoring system.

It simulates how real backend systems evaluate service-level agreements based on incoming metrics and compute overall system health.

The system supports:

- Defining SLAs in the database
- Storing time-series metric data
- Evaluating SLAs over rolling time windows
- Aggregating overall system health
- Returning proper HTTP status codes (200, 206, 503)

This mirrors how internal monitoring systems work in production environments.

---

## Architecture Overview

This service is structured into four layers:

1. Routers (API Layer)
   - Built with FastAPI
   - Handle HTTP requests and responses
   - Endpoints:
     - /sla-definitions
     - /dashboard/summary
     - /health

2. Services (Business Logic Layer)
   - Contains SLA evaluation logic
   - Computes pass, fail, or no_data
   - Applies rolling time window logic
   - File: backend/app/services/sla_eval.py

3. Models (ORM Layer)
   - SQLAlchemy models
   - SLADefinition
   - MetricPoint
   - DataSource

4. Database (Persistence Layer)
   - MySQL
   - Stores:
     - SLA definitions
     - Time-series metric data
     - Data sources

---

## Request Flow

Client → FastAPI Router → SLA Evaluation Service → Database → JSON Response

The /dashboard/summary endpoint:

- Evaluates all active SLAs
- Counts pass, fail, no_data
- Computes overall system health
- Returns proper HTTP status codes:

Overall Status | HTTP Code
healthy        | 200
degraded       | 206
critical       | 503

This mimics real-world health signaling used in load balancers and Kubernetes.

---

## System Diagram

Client / curl
      |
      v
FastAPI Router
 (/dashboard)
      |
      v
SLA Evaluation Service
      |
      v
MySQL Database
(metric_points, sla_definitions)

---

## Example API Usage

Create an SLA:

curl -X POST http://127.0.0.1:8000/sla-definitions/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Latency p95 under 250ms",
    "data_source_id": 2,
    "metric_key": "latency_ms",
    "statistic": "p95",
    "threshold": 250,
    "window_minutes": 60,
    "is_active": true
}'

Insert a metric (via Python script):

./.venv/bin/python -c "
from datetime import datetime
from app.db import SessionLocal
from app.models.metric_point import MetricPoint
db=SessionLocal()
now=datetime.utcnow()
mp=MetricPoint(product_id=2, metric_name='latency_ms', ts_bucket=now, value=200.0, computed_at=now)
db.add(mp)
db.commit()
db.close()
"

Check dashboard health:

curl -i http://127.0.0.1:8000/dashboard/summary

Example healthy response:

{
  "total_slas": 1,
  "passing": 1,
  "failing": 0,
  "no_data": 0,
  "overall_status": "healthy"
}

Example critical response:

{
  "total_slas": 1,
  "passing": 0,
  "failing": 1,
  "no_data": 0,
  "overall_status": "critical"
}

---

## Multi-SLA Flexibility

The system supports multiple SLA types without code changes.

Examples:
- latency_ms
- error_rate
- cpu_usage
- throughput

Each SLA defines:
- metric_key
- threshold
- statistic
- rolling window

This allows flexible SLA monitoring across different metrics.

---

## Why This Project Matters

This is not a simple CRUD application.

It demonstrates:
- Time-windowed metric evaluation
- Aggregated system health computation
- Service-layer separation
- Proper HTTP semantics
- Database-driven business rules
- Monitoring system design principles

This architecture reflects patterns used in internal observability and reliability systems.