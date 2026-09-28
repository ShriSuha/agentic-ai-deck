"""Read one model card by filename."""

from pathlib import Path

from crewai.tools import BaseTool

CARDS_DIR = Path(__file__).resolve().parents[2] / "cards"


def read_card(filename: str) -> str:
    """Return one Markdown card. Refuse any path outside the cards folder."""
    root = CARDS_DIR.resolve()
    requested = (root / filename).resolve()
    try:
        requested.relative_to(root)
    except ValueError:
        return "Refusing to read a file outside the cards folder."
    if requested.suffix.lower() != ".md" or not requested.is_file():
        return f"No card named {Path(filename).name}."
    return requested.read_text(encoding="utf-8")


class ReadCardTool(BaseTool):
    name: str = "read_card"
    description: str = (
        "Read one model card. Input is a filename from search_cards, "
        "such as bert-base-uncased.md. Returns the full Markdown text."
    )

    def _run(self, filename: str) -> str:
        return read_card(filename)
