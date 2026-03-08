"""Flashcard deck and card router."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.flashcard import Flashcard, FlashcardDeck
from schemas.flashcard import (
    DeckCreate,
    DeckListOut,
    DeckOut,
    FlashcardCreate,
    FlashcardOut,
    FlashcardReviewRequest,
)
from services.spaced_repetition import sm2_review

router = APIRouter()


# ── Decks ────────────────────────────────────────────────────────────────────

@router.post("/decks", response_model=DeckOut, status_code=status.HTTP_201_CREATED)
async def create_deck(payload: DeckCreate, db: AsyncSession = Depends(get_db)) -> DeckOut:
    """Create a new flashcard deck."""
    deck = FlashcardDeck(**payload.model_dump())
    db.add(deck)
    await db.flush()
    await db.refresh(deck)
    return DeckOut.model_validate(deck)


@router.get("/decks", response_model=list[DeckListOut])
async def list_decks(db: AsyncSession = Depends(get_db)) -> list[DeckListOut]:
    """List all decks (without cards)."""
    result = await db.execute(
        select(FlashcardDeck).order_by(FlashcardDeck.created_at.desc())
    )
    decks = result.scalars().all()
    out = []
    for deck in decks:
        count_result = await db.execute(
            select(Flashcard).where(Flashcard.deck_id == deck.id)
        )
        card_count = len(count_result.scalars().all())
        d = DeckListOut.model_validate(deck)
        d.card_count = card_count
        out.append(d)
    return out


@router.get("/decks/{deck_id}", response_model=DeckOut)
async def get_deck(deck_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> DeckOut:
    """Get a deck including all its cards."""
    result = await db.execute(
        select(FlashcardDeck)
        .where(FlashcardDeck.id == deck_id)
        .options(selectinload(FlashcardDeck.cards))
    )
    deck = result.scalars().first()
    if not deck:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found")
    return DeckOut.model_validate(deck)


@router.delete("/decks/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deck(deck_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    """Delete a deck and all its cards."""
    deck = await db.get(FlashcardDeck, deck_id)
    if not deck:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found")
    await db.delete(deck)


# ── Cards ────────────────────────────────────────────────────────────────────

@router.post("/cards", response_model=FlashcardOut, status_code=status.HTTP_201_CREATED)
async def create_card(payload: FlashcardCreate, db: AsyncSession = Depends(get_db)) -> FlashcardOut:
    """Create a new flashcard in a deck."""
    deck = await db.get(FlashcardDeck, payload.deck_id)
    if not deck:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found")
    card = Flashcard(**payload.model_dump())
    db.add(card)
    await db.flush()
    await db.refresh(card)
    return FlashcardOut.model_validate(card)


@router.get("/cards/review/{deck_id}", response_model=list[FlashcardOut])
async def get_due_cards(deck_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[FlashcardOut]:
    """Return cards that are due for review (next_review <= now)."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Flashcard)
        .where(Flashcard.deck_id == deck_id, Flashcard.next_review <= now)
        .order_by(Flashcard.next_review)
    )
    cards = result.scalars().all()
    return [FlashcardOut.model_validate(c) for c in cards]


@router.put("/cards/{card_id}/review", response_model=FlashcardOut)
async def review_card(
    card_id: uuid.UUID,
    payload: FlashcardReviewRequest,
    db: AsyncSession = Depends(get_db),
) -> FlashcardOut:
    """Submit a review result for a card using the SM-2 algorithm."""
    card = await db.get(Flashcard, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    result = sm2_review(card.ease_factor, card.interval, card.repetitions, payload.quality)
    card.ease_factor = result["ease_factor"]
    card.interval = result["interval"]
    card.repetitions = result["repetitions"]
    card.last_reviewed = datetime.now(timezone.utc)
    card.next_review = result["next_review"]
    await db.flush()
    await db.refresh(card)
    return FlashcardOut.model_validate(card)


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(card_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    """Delete a flashcard."""
    card = await db.get(Flashcard, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    await db.delete(card)
