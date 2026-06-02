from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv


DEFAULT_NEWS_FEEDS: Tuple[str, ...] = (
    "Reuters via Google News|https://news.google.com/rss/search?q=site%3Areuters.com%20world%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen",
    "BBC World|https://feeds.bbci.co.uk/news/world/rss.xml",
    "AI Technology|https://news.google.com/rss/search?q=%28artificial%20intelligence%20OR%20OpenAI%20OR%20AI%29%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen",
)


def _split_csv(value: str | None) -> Tuple[str, ...]:
    if not value:
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


def _date_env(name: str, default: date) -> date:
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be YYYY-MM-DD, got {raw!r}") from exc


@dataclass(frozen=True)
class Settings:
    project_root: Path
    data_dir: Path
    timezone: str
    plan_start_date: date

    openai_api_key: str
    openai_model: str
    openai_timeout_seconds: int

    wechat_app_id: str
    wechat_app_secret: str
    wechat_openids: Tuple[str, ...]
    wechat_template_id: str
    wechat_template_id_morning: str
    wechat_template_id_evening: str
    wechat_max_content_chars: int
    wechat_verify_token: str

    morning_hour: int
    morning_minute: int
    news_fetch_hour: int
    news_fetch_minute: int
    evening_hour: int
    evening_minute: int

    news_feeds: Tuple[str, ...]
    rss_timeout_seconds: int

    @property
    def openai_enabled(self) -> bool:
        return bool(self.openai_api_key)

    @property
    def wechat_enabled(self) -> bool:
        return bool(
            self.wechat_app_id
            and self.wechat_app_secret
            and self.wechat_openids
            and (
                self.wechat_template_id
                or self.wechat_template_id_morning
                or self.wechat_template_id_evening
            )
        )

    def template_for(self, slot: str) -> str:
        if slot == "morning" and self.wechat_template_id_morning:
            return self.wechat_template_id_morning
        if slot == "evening" and self.wechat_template_id_evening:
            return self.wechat_template_id_evening
        return self.wechat_template_id


def load_settings(env_file: str | Path | None = None) -> Settings:
    project_root = Path(__file__).resolve().parents[1]
    dotenv_path = Path(env_file) if env_file else project_root / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=False)

    data_dir_raw = os.getenv("DATA_DIR")
    if data_dir_raw:
        data_dir_path = Path(data_dir_raw)
        data_dir = (
            data_dir_path
            if data_dir_path.is_absolute()
            else project_root / data_dir_path
        ).resolve()
    else:
        data_dir = (project_root / "data").resolve()
    today = date.today()
    feeds = _split_csv(os.getenv("NEWS_FEEDS")) or DEFAULT_NEWS_FEEDS

    return Settings(
        project_root=project_root,
        data_dir=data_dir,
        timezone=os.getenv("TIMEZONE", "Asia/Shanghai"),
        plan_start_date=_date_env("PLAN_START_DATE", today),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        openai_timeout_seconds=_int_env("OPENAI_TIMEOUT_SECONDS", 60),
        wechat_app_id=os.getenv("WECHAT_APP_ID", ""),
        wechat_app_secret=os.getenv("WECHAT_APP_SECRET", ""),
        wechat_openids=_split_csv(os.getenv("WECHAT_OPENIDS")),
        wechat_template_id=os.getenv("WECHAT_TEMPLATE_ID", ""),
        wechat_template_id_morning=os.getenv("WECHAT_TEMPLATE_ID_MORNING", ""),
        wechat_template_id_evening=os.getenv("WECHAT_TEMPLATE_ID_EVENING", ""),
        wechat_max_content_chars=_int_env("WECHAT_MAX_CONTENT_CHARS", 1400),
        wechat_verify_token=os.getenv("WECHAT_VERIFY_TOKEN", ""),
        morning_hour=_int_env("MORNING_HOUR", 7),
        morning_minute=_int_env("MORNING_MINUTE", 30),
        news_fetch_hour=_int_env("NEWS_FETCH_HOUR", 7),
        news_fetch_minute=_int_env("NEWS_FETCH_MINUTE", 0),
        evening_hour=_int_env("EVENING_HOUR", 18),
        evening_minute=_int_env("EVENING_MINUTE", 0),
        news_feeds=feeds,
        rss_timeout_seconds=_int_env("RSS_TIMEOUT_SECONDS", 15),
    )
