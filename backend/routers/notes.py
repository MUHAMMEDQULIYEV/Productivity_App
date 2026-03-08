"""Notes CRUD router with full-text search."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.note import Note
from schemas.note import NoteCreate, NoteOut, NoteUpdate

router = APIRouter()


@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate, db: AsyncSession = Depends(get_db)) -> NoteOut:
    """Create a new note."""
    note = Note(**payload.model_dump())
    db.add(note)
    await db.flush()
    await db.refresh(note)
    return NoteOut.model_validate(note)


@router.get("/notes/search", response_model=list[NoteOut])
async def search_notes(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
) -> list[NoteOut]:
    """Full-text search on title and content."""
    term = f"%{q}%"
    result = await db.execute(
        select(Note)
        .where(or_(Note.title.ilike(term), Note.content.ilike(term)))
        .order_by(Note.updated_at.desc())
    )
    notes = result.scalars().all()
    return [NoteOut.model_validate(n) for n in notes]


@router.get("/notes", response_model=list[NoteOut])
async def list_notes(
    tag: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[NoteOut]:
    """List all notes, optionally filtered by tag."""
    result = await db.execute(select(Note).order_by(Note.updated_at.desc()))
    notes = result.scalars().all()
    if tag:
        notes = [n for n in notes if tag in (n.tags or [])]
    return [NoteOut.model_validate(n) for n in notes]


@router.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> NoteOut:
    """Retrieve a single note."""
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut.model_validate(note)


@router.put("/notes/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: uuid.UUID, payload: NoteUpdate, db: AsyncSession = Depends(get_db)
) -> NoteOut:
    """Update an existing note."""
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    await db.flush()
    await db.refresh(note)
    return NoteOut.model_validate(note)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    """Delete a note."""
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    await db.delete(note)
