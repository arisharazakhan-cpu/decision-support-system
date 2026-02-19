from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class SLADefinition(Base):
    __tablename__ = "sla_definitions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False, index=True)
    data_source = relationship("DataSource")

    metric_key = Column(String(64), nullable=False, default="latency_ms")
    statistic = Column(String(16), nullable=False, default="p95")

    threshold = Column(Float, nullable=False)
    window_minutes = Column(Integer, nullable=False, default=60)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
