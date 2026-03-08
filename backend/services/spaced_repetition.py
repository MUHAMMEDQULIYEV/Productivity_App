"""SM-2 spaced repetition algorithm implementation."""

from datetime import datetime, timedelta, timezone


def sm2_review(
    ease_factor: float,
    interval: int,
    repetitions: int,
    quality: int,
) -> dict:
    """Apply the SM-2 algorithm and return updated scheduling parameters.

    Args:
        ease_factor: Current ease factor (e.g. 2.5).
        interval: Current review interval in days.
        repetitions: Number of successful consecutive reviews.
        quality: Review quality rating 0–5 (0=blackout, 5=perfect recall).

    Returns:
        dict with keys: ease_factor, interval, repetitions, next_review (datetime).
    """
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)
        repetitions += 1

    ease_factor = max(
        1.3,
        ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02),
    )
    next_review = datetime.now(timezone.utc) + timedelta(days=interval)

    return {
        "ease_factor": ease_factor,
        "interval": interval,
        "repetitions": repetitions,
        "next_review": next_review,
    }
