"""Task ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class Task(Base):
    """Represents a user task with priority, category, and deadline."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(
        Enum("work", "study", "learning", "personal", name="task_category"),
        nullable=False,
        default="personal",
    )
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[str] = mapped_column(
        Enum("high", "medium", "low", name="task_priority"),
        nullable=False,
        default="medium",
    )
    status: Mapped[str] = mapped_column(
        Enum(
            "not_started",
            "in_progress",
            "completed",
            "archived",
            name="task_status",
        ),
        nullable=False,
        default="not_started",
    )
    estimated_duration: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Duration in minutes"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
