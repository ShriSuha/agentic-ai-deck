"""Use the Ollama server configured in .env or default to 127.0.0.1:11434"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "http://127.0.0.1:11434"
SERVE_LOG = ROOT / ".ollama" / "serve.log"


def _base_url(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return "http://" + value


def installed_models(base_url: str) -> list[str] | None:
    """Return model names, or None when that address is not answering."""
    url = _base_url(base_url) + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            payload = json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None
    return [item.get("name", "") for item in payload.get("models", [])]


def has_model(names: list[str], wanted: str) -> bool:
    return wanted in names or f"{wanted}:latest" in names


def find_server() -> str:
    """Get Ollama server from .env or use default."""
    return _base_url(os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL))


def ensure_server() -> str:
    """Use configured server or start one on 127.0.0.1:11434."""
    server = find_server()
    
    if installed_models(server) is not None:
        return server

    if shutil.which("ollama") is None:
        raise SystemExit(
            "Ollama is not installed. Install it from https://ollama.com"
        )

    print(f"Starting Ollama at {DEFAULT_BASE_URL}")
    SERVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    log_file = SERVE_LOG.open("ab")
    env = os.environ.copy()
    env["OLLAMA_HOST"] = "127.0.0.1:11434"
    subprocess.Popen(
        ["ollama", "serve"],
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(30):
        if installed_models(DEFAULT_BASE_URL) is not None:
            print("Ollama is up.")
            return DEFAULT_BASE_URL
        time.sleep(0.5)
    raise SystemExit(f"Ollama did not start. Check {SERVE_LOG}")


def pull_model(base_url: str, model: str) -> None:
    """Download a model from Ollama."""
    if shutil.which("ollama") is None:
        raise SystemExit("Ollama is not installed. Install it from https://ollama.com")
    
    env = os.environ.copy()
    subprocess.check_call(["ollama", "pull", model], env=env)