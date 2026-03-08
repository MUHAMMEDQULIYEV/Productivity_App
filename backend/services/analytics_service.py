"""Analytics computation service using pandas and scikit-learn."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone


async def compute_productivity_trends(tasks: list) -> dict:
    """Compute task completion trends and peak productivity hours.

    Args:
        tasks: List of Task ORM instances.

    Returns:
        Serialisable dict with completion stats, category breakdown, and peak hours.
    """
    total = len(tasks)
    completed = [t for t in tasks if t.status == "completed"]
    completion_rate = round(len(completed) / total * 100, 2) if total else 0.0

    # Category breakdown
    category_totals: dict[str, int] = defaultdict(int)
    category_completed: dict[str, int] = defaultdict(int)
    for task in tasks:
        category_totals[task.category] += 1
    for task in completed:
        category_completed[task.category] += 1

    category_breakdown = {
        cat: {
            "total": category_totals[cat],
            "completed": category_completed.get(cat, 0),
        }
        for cat in category_totals
    }

    # Peak hours (hour of day with most completions)
    hour_counts: dict[int, int] = defaultdict(int)
    for task in completed:
        if task.updated_at:
            dt = task.updated_at
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            hour_counts[dt.hour] += 1

    peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else None

    return {
        "total_tasks": total,
        "completed_tasks": len(completed),
        "completion_rate": completion_rate,
        "category_breakdown": category_breakdown,
        "peak_productivity_hour": peak_hour,
        "hour_distribution": dict(hour_counts),
    }


async def compute_vocabulary_growth(vocab: list, cards: list) -> dict:
    """Compute vocabulary growth and flashcard accuracy statistics.

    Args:
        vocab: List of LanguageVocabulary ORM instances.
        cards: List of Flashcard ORM instances.

    Returns:
        Serialisable dict with vocab stats and flashcard accuracy.
    """
    total_words = len(vocab)
    learned_words = sum(1 for v in vocab if v.learned)
    retention_rate = round(learned_words / total_words * 100, 2) if total_words else 0.0

    # Group learned words by date
    words_by_date: dict[str, int] = defaultdict(int)
    for v in vocab:
        if v.learned and v.date_learned:
            words_by_date[str(v.date_learned)] += 1

    # Flashcard accuracy
    reviewed_cards = [c for c in cards if c.repetitions > 0]
    good_cards = [c for c in reviewed_cards if c.ease_factor >= 2.5]
    flashcard_accuracy = (
        round(len(good_cards) / len(reviewed_cards) * 100, 2) if reviewed_cards else 0.0
    )

    return {
        "total_words": total_words,
        "learned_words": learned_words,
        "retention_rate": retention_rate,
        "words_by_date": dict(sorted(words_by_date.items())),
        "total_flashcards": len(cards),
        "reviewed_flashcards": len(reviewed_cards),
        "flashcard_accuracy": flashcard_accuracy,
    }


async def find_peak_hours(tasks: list) -> dict[int, int]:
    """Return a mapping of hour-of-day → completion count.

    Args:
        tasks: List of Task ORM instances.

    Returns:
        Dict mapping hour (0-23) to number of tasks completed in that hour.
    """
    hour_counts: dict[int, int] = defaultdict(int)
    for task in tasks:
        if task.status == "completed" and task.updated_at:
            dt = task.updated_at
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            hour_counts[dt.hour] += 1
    return dict(hour_counts)
