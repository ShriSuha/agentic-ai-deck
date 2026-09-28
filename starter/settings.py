"""Load project settings from starter/config/settings.yaml."""

from functools import lru_cache
from pathlib import Path

import yaml

SETTINGS_PATH = Path(__file__).resolve().parent / "config" / "settings.yaml"


@lru_cache(maxsize=1)
def load_settings() -> dict:
    with SETTINGS_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    return data


def search_max_hits() -> int:
    search = load_settings().get("search") or {}
    raw = search.get("max_hits", 8) if isinstance(search, dict) else 8
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 8
    return value if value > 0 else 8
