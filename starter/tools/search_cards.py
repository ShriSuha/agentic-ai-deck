"""Search the model-card folder. Returns filenames and a short snippet."""

from functools import lru_cache
from pathlib import Path

import nltk
from crewai.tools import BaseTool
from nltk.corpus import stopwords

from starter.settings import search_max_hits

CARDS_DIR = Path(__file__).resolve().parents[2] / "cards"


@lru_cache(maxsize=1)
def _english_stopwords() -> frozenset[str]:
    try:
        words = stopwords.words("english")
    except LookupError:
        nltk.download("stopwords", quiet=True)
        words = stopwords.words("english")
    return frozenset(words)


def search_cards(query: str) -> str:
    """Find Markdown cards whose text contains the query words."""
    words = [
        word
        for word in "".join(ch.lower() if ch.isalnum() else " " for ch in query).split()
        if len(word) > 2 and word not in _english_stopwords()
    ]
    if not words:
        return "No search words were left after ignoring common words."

    hits: list[tuple[int, str, str]] = []
    for path in sorted(CARDS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        score = sum(lowered.count(word) for word in words)
        if score == 0:
            continue
        hits.append((score, path.name, _snippet(text, words)))

    if not hits:
        return "No card matched those words."

    hits.sort(key=lambda item: (-item[0], item[1]))
    lines = [f"{name}: {snippet}" for _, name, snippet in hits[: search_max_hits()]]
    return "\n".join(lines)


def _snippet(text: str, words: list[str]) -> str:
    lowered = text.lower()
    position = min(
        (lowered.find(word) for word in words if word in lowered),
        default=0,
    )
    start = max(0, position - 40)
    chunk = " ".join(text[start : start + 160].split())
    return chunk


class SearchCardsTool(BaseTool):
    name: str = "search_cards"
    description: str = (
        "Search the model-card folder. Input is the question or a few keywords. "
        "Returns matching filenames and a short snippet from each file."
    )

    def _run(self, query: str) -> str:
        return search_cards(query)
