"""Pydantic schemas for Task endpoints."""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


TaskCategory = Literal["work", "study", "learning", "personal"]
TaskPriority = Literal["high", "medium", "low"]
TaskStatus = Literal["not_started", "in_progress", "completed", "archived"]


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    category: TaskCategory = "personal"
    deadline: datetime | None = None
    priority: TaskPriority = "medium"
    status: TaskStatus = "not_started"
    estimated_duration: int | None = Field(default=None, ge=1, description="Minutes")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""


class TaskUpdate(TaskBase):
    """Schema for updating an existing task (all fields optional)."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    category: TaskCategory | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None


class TaskOut(TaskBase):
    """Schema returned to the client."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
