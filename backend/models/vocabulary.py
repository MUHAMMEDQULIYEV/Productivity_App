"""LanguageVocabulary ORM model."""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class LanguageVocabulary(Base):
    """Stores vocabulary words extracted from various sources."""

    __tablename__ = "language_vocabulary"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    word: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False, default="english")
    translation: Mapped[str | None] = mapped_column(String(512), nullable=True)
    frequency_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    source_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    learned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    date_learned: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
