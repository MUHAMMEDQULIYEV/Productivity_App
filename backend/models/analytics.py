"""Analytics ORM models."""

import uuid
from datetime import date

from sqlalchemy import Date, Float, Integer, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProductivityAnalytics(Base):
    """Daily snapshot of task completion metrics."""

    __tablename__ = "productivity_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    tasks_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tasks_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_breakdown: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    completion_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class LanguageProgress(Base):
    """Daily snapshot of language learning progress."""

    __tablename__ = "language_progress"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    language: Mapped[str] = mapped_column(String(50), nullable=False, default="english")
    date: Mapped[date] = mapped_column(Date, nullable=False)
    words_learned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    flashcard_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    time_spent: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="Minutes"
    )
    topics_studied: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
