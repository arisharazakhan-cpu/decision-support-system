from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.product import Product
from app.models.data_source import DataSource
from app.models.raw_event import RawEvent
from app.models.metric_point import MetricPoint
from app.models.sla_definition import SLADefinition
