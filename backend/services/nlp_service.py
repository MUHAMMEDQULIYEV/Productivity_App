"""NLP service for word extraction using NLTK."""

import re
from collections import Counter

# Lazy import — NLTK data downloaded at container build time.
import nltk

_NLTK_READY = False


def _ensure_nltk() -> None:
    """Download required NLTK corpora if not already present."""
    global _NLTK_READY
    if _NLTK_READY:
        return
    resource_paths = {
        "punkt": "tokenizers/punkt",
        "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger",
        "stopwords": "corpora/stopwords",
    }
    for resource, path in resource_paths.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(resource, quiet=True)
    _NLTK_READY = True


def extract_words(text: str, language: str = "english") -> list[dict]:
    """Extract meaningful words with POS tags and frequencies from text.

    Args:
        text: Raw input text (transcript, notes, etc.).
        language: Language hint ('english' or 'korean').

    Returns:
        List of dicts with keys: word, pos, frequency — sorted by frequency desc.
    """
    if language == "korean":
        return _extract_korean(text)
    return _extract_english(text)


def _extract_english(text: str) -> list[dict]:
    """Extract English vocabulary using NLTK tokenisation and POS tagging."""
    _ensure_nltk()
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    # Keep only alphabetic tokens that are not stopwords
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words and len(t) > 2]

    tagged = nltk.pos_tag(tokens)
    freq = Counter(t for t, _ in tagged)
    pos_map: dict[str, str] = {}
    for token, tag in tagged:
        pos_map.setdefault(token, tag)

    return [
        {"word": word, "pos": pos_map.get(word, ""), "frequency": count}
        for word, count in freq.most_common()
    ]


def _extract_korean(text: str) -> list[dict]:
    """Best-effort Korean word extraction using character-level splitting."""
    # Split on whitespace and punctuation; keep Korean character sequences
    tokens = re.findall(r"[가-힣]+", text)
    freq = Counter(t for t in tokens if len(t) > 1)
    return [
        {"word": word, "pos": "unknown", "frequency": count}
        for word, count in freq.most_common()
    ]
