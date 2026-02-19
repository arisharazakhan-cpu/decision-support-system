from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MetricPoint(Base):
    __tablename__ = "metric_points"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Existing
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # New: proper linkage to the source that produced this metric
    data_source_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("data_sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ts_bucket: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    computed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships (optional but nice)
    data_source = relationship("DataSource", back_populates="metric_points")