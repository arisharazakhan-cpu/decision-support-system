from sqlalchemy import ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base

class RawEvent(Base):
    __tablename__ = "raw_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("data_sources.id"), nullable=False
    )

    event_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
