from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .config import Settings


def ensure_data_dir(settings: Settings) -> Path:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings.data_dir


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    temp.replace(path)


def daily_cache_path(settings: Settings, kind: str, day: date) -> Path:
    ensure_data_dir(settings)
    return settings.data_dir / f"{kind}_{day.isoformat()}.json"


def load_daily_cache(settings: Settings, kind: str, day: date) -> Any:
    return read_json(daily_cache_path(settings, kind, day))


def save_daily_cache(settings: Settings, kind: str, day: date, payload: Any) -> None:
    write_json(daily_cache_path(settings, kind, day), payload)
