"""Reject answers that name a missing card or invent text that is not in the file."""

import re
from pathlib import Path

CARDS_DIR = Path(__file__).resolve().parents[2] / "cards"
FILENAME = re.compile(r"[\w.-]+\.md")


def check_answer(output) -> tuple[bool, str]:
    """Return whether the answer is grounded in a real model card."""
    text = getattr(output, "raw", None) or str(output)
    names = [
        name
        for name in dict.fromkeys(FILENAME.findall(text))
        if (CARDS_DIR / name).is_file()
    ]
    pasted = _pasted_card_lines(text)

    if not names:
        if _refuses(text) and not pasted:
            return True, text
        return (
            False,
            "Name a real file from the cards folder, such as bert-base-uncased.md, "
            "or say that the collection does not contain the answer. "
            "Do not invent a model card.",
        )

    files = {name: (CARDS_DIR / name).read_text(encoding="utf-8") for name in names}
    for line in pasted:
        if not any(_norm(line) in _norm(body) for body in files.values()):
            used = ", ".join(names)
            return (
                False,
                f"The answer includes card text that is not in {used}. "
                "Open the file with read_card and use only what it says.",
            )

    license_name = _stated_license(text)
    if license_name and not any(_file_has_license(body, license_name) for body in files.values()):
        used = ", ".join(names)
        return (
            False,
            f"The license in the answer is not written in {used}. "
            "Read the card again and quote the license from that file.",
        )
    return True, text


def _refuses(text: str) -> bool:
    lowered = text.lower()
    return (
        "does not contain" in lowered
        or "do not contain" in lowered
        or "doesn't contain" in lowered
        or "not in the collection" in lowered
        or "not in the cards" in lowered
    )


def _pasted_card_lines(text: str) -> list[str]:
    lines = text.splitlines()
    if not any(line.strip().startswith("#") for line in lines):
        return []
    pasted: list[str] = []
    copying = False
    for line in lines:
        stripped = line.strip().strip("`")
        if stripped.startswith("#"):
            copying = True
        if copying and stripped:
            pasted.append(stripped)
    return pasted


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def _stated_license(text: str) -> str | None:
    lowered = text.lower()
    if "apache" in lowered and "2.0" in lowered:
        return "apache"
    if "llama 2 community" in lowered:
        return "llama"
    if "noncommercial" in lowered or "non-commercial" in lowered or "cc-by-nc" in lowered:
        return "cc-by-nc"
    if "cc-by-4.0" in lowered or "attribution 4.0" in lowered:
        return "cc-by"
    if "bsd" in lowered:
        return "bsd"
    if "mit license" in lowered:
        return "mit"
    return None


def _file_has_license(file_text: str, kind: str) -> bool:
    lowered = file_text.lower()
    if kind == "apache":
        return "apache license 2.0" in lowered or "apache-2.0" in lowered
    if kind == "llama":
        return "llama 2 community license" in lowered
    if kind == "cc-by-nc":
        return "noncommercial" in lowered or "non-commercial" in lowered or "cc-by-nc" in lowered
    if kind == "cc-by":
        return "cc-by-4.0" in lowered or "attribution 4.0" in lowered
    if kind == "bsd":
        return "bsd 3-clause" in lowered or "bsd-3-clause" in lowered
    if kind == "mit":
        return "mit license" in lowered
    return False
