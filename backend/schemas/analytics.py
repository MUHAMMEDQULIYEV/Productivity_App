"""Pydantic schemas for Analytics endpoints."""

import uuid
from datetime import date

from pydantic import BaseModel


class ProductivityAnalyticsOut(BaseModel):
    id: uuid.UUID
    date: date
    tasks_completed: int
    tasks_total: int
    category_breakdown: dict
    completion_rate: float

    model_config = {"from_attributes": True}


class LanguageProgressOut(BaseModel):
    id: uuid.UUID
    language: str
    date: date
    words_learned: int
    flashcard_accuracy: float
    time_spent: int
    topics_studied: list

    model_config = {"from_attributes": True}


class DashboardSummary(BaseModel):
    tasks_completed_today: int
    tasks_due_today: int
    vocabulary_learned_this_week: int
    flashcard_accuracy_this_week: float
    total_flashcards_due: int


class RecommendationOut(BaseModel):
    message: str
    priority: str
