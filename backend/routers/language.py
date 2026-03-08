"""Language learning router — transcript extraction and vocabulary management."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.vocabulary import LanguageVocabulary
from schemas.vocabulary import (
    ExtractionRequest,
    TextExtractionRequest,
    VocabularyItem,
    VocabularyOut,
    VocabularySaveRequest,
)
from services.nlp_service import extract_words
from services.youtube_service import fetch_transcript

router = APIRouter()


@router.post("/language/extract-youtube", response_model=list[VocabularyItem])
async def extract_from_youtube(payload: ExtractionRequest) -> list[VocabularyItem]:
    """Extract vocabulary from a YouTube video transcript."""
    try:
        transcript = await fetch_transcript(payload.url)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not fetch transcript: {exc}",
        ) from exc
    return extract_words(transcript)


@router.post("/language/extract-upload", response_model=list[VocabularyItem])
async def extract_from_upload(file: UploadFile) -> list[VocabularyItem]:
    """Extract vocabulary from an uploaded .srt or .txt file."""
    if not file.filename or not file.filename.lower().endswith((".srt", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .srt and .txt files are supported.",
        )
    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not decode file: {exc}",
        ) from exc
    return extract_words(text)


@router.post("/language/extract-text", response_model=list[VocabularyItem])
async def extract_from_text(payload: TextExtractionRequest) -> list[VocabularyItem]:
    """Extract vocabulary from raw text."""
    return extract_words(payload.text)


@router.get("/language/vocabulary", response_model=list[VocabularyOut])
async def list_vocabulary(
    language: str | None = Query(default=None),
    learned: bool | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[VocabularyOut]:
    """List stored vocabulary words."""
    stmt = select(LanguageVocabulary).order_by(LanguageVocabulary.created_at.desc())
    if language:
        stmt = stmt.where(LanguageVocabulary.language == language)
    if learned is not None:
        stmt = stmt.where(LanguageVocabulary.learned == learned)
    result = await db.execute(stmt)
    words = result.scalars().all()
    return [VocabularyOut.model_validate(w) for w in words]


@router.post(
    "/language/vocabulary/save",
    response_model=list[VocabularyOut],
    status_code=status.HTTP_201_CREATED,
)
async def save_vocabulary(
    payload: VocabularySaveRequest, db: AsyncSession = Depends(get_db)
) -> list[VocabularyOut]:
    """Persist a batch of vocabulary items to the database."""
    saved = []
    for item in payload.items:
        word = LanguageVocabulary(
            word=item.word,
            language=payload.language,
            frequency_count=item.frequency,
            source_url=payload.source_url,
        )
        db.add(word)
        await db.flush()
        await db.refresh(word)
        saved.append(VocabularyOut.model_validate(word))
    return saved


@router.put("/language/vocabulary/{vocab_id}/mark-learned", response_model=VocabularyOut)
async def mark_learned(
    vocab_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> VocabularyOut:
    """Mark a vocabulary word as learned."""
    word = await db.get(LanguageVocabulary, vocab_id)
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Word not found")
    word.learned = True
    word.date_learned = date.today()
    await db.flush()
    await db.refresh(word)
    return VocabularyOut.model_validate(word)


@router.get("/language/analytics")
async def language_analytics(db: AsyncSession = Depends(get_db)) -> dict:
    """Return vocabulary statistics."""
    result = await db.execute(select(LanguageVocabulary))
    words = result.scalars().all()
    total = len(words)
    learned = sum(1 for w in words if w.learned)
    return {
        "total_words": total,
        "learned_words": learned,
        "retention_rate": round(learned / total * 100, 2) if total else 0.0,
    }
