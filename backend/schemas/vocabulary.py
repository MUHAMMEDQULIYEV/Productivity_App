"""Pydantic schemas for Vocabulary endpoints."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class VocabularyItem(BaseModel):
    """A single extracted vocabulary word (not yet persisted)."""

    word: str
    pos: str = ""
    frequency: int = 1


class VocabularySaveRequest(BaseModel):
    items: list[VocabularyItem]
    language: str = "english"
    source_url: str | None = None


class VocabularyOut(BaseModel):
    id: uuid.UUID
    word: str
    language: str
    translation: str | None
    frequency_count: int
    source_url: str | None
    learned: bool
    date_learned: date | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ExtractionRequest(BaseModel):
    url: str = Field(..., description="YouTube URL")


class TextExtractionRequest(BaseModel):
    text: str = Field(..., min_length=1)
