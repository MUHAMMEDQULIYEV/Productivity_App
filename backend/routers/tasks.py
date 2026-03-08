"""Task CRUD router."""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter()


@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)) -> TaskOut:
    """Create a new task."""
    task = Task(**payload.model_dump())
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return TaskOut.model_validate(task)


@router.get("/tasks/upcoming", response_model=list[TaskOut])
async def list_upcoming_tasks(db: AsyncSession = Depends(get_db)) -> list[TaskOut]:
    """Return tasks whose deadline falls within the next 24 hours."""
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(hours=24)
    result = await db.execute(
        select(Task)
        .where(Task.deadline >= now, Task.deadline <= cutoff)
        .where(Task.status != "completed")
        .where(Task.status != "archived")
        .order_by(Task.deadline)
    )
    tasks = result.scalars().all()
    return [TaskOut.model_validate(t) for t in tasks]


@router.get("/tasks", response_model=list[TaskOut])
async def list_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    category: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[TaskOut]:
    """List tasks with optional filters."""
    stmt = select(Task).order_by(Task.created_at.desc())
    if status_filter:
        stmt = stmt.where(Task.status == status_filter)
    if category:
        stmt = stmt.where(Task.category == category)
    if priority:
        stmt = stmt.where(Task.priority == priority)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return [TaskOut.model_validate(t) for t in tasks]


@router.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> TaskOut:
    """Retrieve a single task by ID."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskOut.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: uuid.UUID, payload: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> TaskOut:
    """Update an existing task."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    await db.flush()
    await db.refresh(task)
    return TaskOut.model_validate(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    """Permanently delete a task."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await db.delete(task)
