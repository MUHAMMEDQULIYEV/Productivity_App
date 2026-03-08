"""Pydantic schemas for Flashcard endpoints."""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


DeckLanguage = Literal["english", "korean"]
DeckSourceType = Literal["youtube", "manual", "upload"]


class DeckCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    language: DeckLanguage = "english"
    source_type: DeckSourceType = "manual"


class DeckOut(DeckCreate):
    id: uuid.UUID
    created_at: datetime
    cards: list["FlashcardOut"] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class DeckListOut(DeckCreate):
    id: uuid.UUID
    created_at: datetime
    card_count: int = 0

    model_config = {"from_attributes": True}


class FlashcardCreate(BaseModel):
    deck_id: uuid.UUID
    front: str = Field(..., min_length=1)
    back: str = Field(..., min_length=1)


class FlashcardReviewRequest(BaseModel):
    quality: int = Field(..., ge=0, le=5, description="SM-2 quality rating 0-5")


class FlashcardOut(BaseModel):
    id: uuid.UUID
    deck_id: uuid.UUID
    front: str
    back: str
    ease_factor: float
    interval: int
    repetitions: int
    last_reviewed: datetime | None
    next_review: datetime

    model_config = {"from_attributes": True}


DeckOut.model_rebuild()
