"""Analytics router."""

from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.flashcard import Flashcard
from models.task import Task
from models.vocabulary import LanguageVocabulary
from schemas.analytics import DashboardSummary, RecommendationOut
from services.analytics_service import (
    compute_productivity_trends,
    compute_vocabulary_growth,
    find_peak_hours,
)

router = APIRouter()


@router.get("/analytics/productivity")
async def productivity_analytics(db: AsyncSession = Depends(get_db)) -> dict:
    """Return task completion trends and peak productivity hours."""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return await compute_productivity_trends(tasks)


@router.get("/analytics/language")
async def language_analytics(db: AsyncSession = Depends(get_db)) -> dict:
    """Return vocabulary growth and flashcard statistics."""
    vocab_result = await db.execute(select(LanguageVocabulary))
    vocab = vocab_result.scalars().all()
    card_result = await db.execute(select(Flashcard))
    cards = card_result.scalars().all()
    return await compute_vocabulary_growth(vocab, cards)


@router.get("/analytics/dashboard", response_model=DashboardSummary)
async def dashboard_summary(db: AsyncSession = Depends(get_db)) -> DashboardSummary:
    """Combined summary for the main dashboard."""
    today = date.today()
    now = datetime.now(timezone.utc)

    task_result = await db.execute(select(Task))
    tasks = task_result.scalars().all()

    tasks_completed_today = sum(
        1
        for t in tasks
        if t.status == "completed"
        and t.updated_at
        and t.updated_at.date() == today
    )
    tasks_due_today = sum(
        1
        for t in tasks
        if t.deadline
        and t.deadline.date() == today
        and t.status not in ("completed", "archived")
    )

    week_start = today - timedelta(days=today.weekday())
    vocab_result = await db.execute(select(LanguageVocabulary))
    vocab = vocab_result.scalars().all()
    vocab_this_week = sum(
        1
        for v in vocab
        if v.learned and v.date_learned and v.date_learned >= week_start
    )

    card_result = await db.execute(select(Flashcard))
    cards = card_result.scalars().all()
    due_cards = sum(1 for c in cards if c.next_review <= now)

    # Rough accuracy: cards reviewed at least once with repetitions > 0
    reviewed = [c for c in cards if c.repetitions > 0]
    good_cards = [c for c in reviewed if c.ease_factor >= 2.5]
    accuracy = round(len(good_cards) / len(reviewed) * 100, 2) if reviewed else 0.0

    return DashboardSummary(
        tasks_completed_today=tasks_completed_today,
        tasks_due_today=tasks_due_today,
        vocabulary_learned_this_week=vocab_this_week,
        flashcard_accuracy_this_week=accuracy,
        total_flashcards_due=due_cards,
    )


@router.get("/analytics/recommendations", response_model=list[RecommendationOut])
async def recommendations(db: AsyncSession = Depends(get_db)) -> list[RecommendationOut]:
    """Return personalised study schedule recommendations."""
    recs: list[RecommendationOut] = []

    task_result = await db.execute(select(Task))
    tasks = task_result.scalars().all()
    overdue = [
        t
        for t in tasks
        if t.deadline
        and t.deadline < datetime.now(timezone.utc)
        and t.status not in ("completed", "archived")
    ]
    if overdue:
        recs.append(
            RecommendationOut(
                message=f"You have {len(overdue)} overdue task(s). Prioritise them first.",
                priority="high",
            )
        )

    card_result = await db.execute(select(Flashcard))
    cards = card_result.scalars().all()
    due_cards = [c for c in cards if c.next_review <= datetime.now(timezone.utc)]
    if due_cards:
        recs.append(
            RecommendationOut(
                message=f"{len(due_cards)} flashcard(s) are due for review. Keep your streak!",
                priority="medium",
            )
        )

    if not recs:
        recs.append(
            RecommendationOut(
                message="Great job! You're all caught up. Consider adding new vocabulary.",
                priority="low",
            )
        )
    return recs
