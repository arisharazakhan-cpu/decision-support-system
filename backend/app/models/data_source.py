from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # csv, api, json
    refresh_minutes: Mapped[int] = mapped_column(Integer, nullable=True)

    metric_points = relationship("MetricPoint", back_populates="data_source")
    sla_definitions = relationship("SLADefinition", back_populates="data_source")