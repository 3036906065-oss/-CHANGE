from __future__ import annotations

import json
import logging
from datetime import date, datetime
from zoneinfo import ZoneInfo

from .config import Settings, load_settings
from .openai_client import AIClient
from .services.english import build_english_pack, render_english_pack
from .services.fitness import render_training, training_for_day
from .services.news import build_news_pack, render_news_pack
from .services.nutrition import meal_plan_for_day, render_meal_plan
from .storage import load_daily_cache, save_daily_cache
from .wechat import WeChatClient

logger = logging.getLogger(__name__)


def today(settings: Settings) -> date:
    return datetime.now(ZoneInfo(settings.timezone)).date()


def fetch_news_job(settings: Settings | None = None, day: date | None = None) -> dict:
    settings = settings or load_settings()
    day = day or today(settings)
    ai = AIClient(settings)
    pack = build_news_pack(settings, ai, day)
    save_daily_cache(settings, "news", day, pack)
    logger.info("Fetched %s news candidates for %s.", pack.get("fetched_count", 0), day)
    return pack


def get_or_fetch_news(settings: Settings, day: date) -> dict:
    cached = load_daily_cache(settings, "news", day)
    if cached:
        return cached
    return fetch_news_job(settings, day)


def build_morning_message(settings: Settings | None = None, day: date | None = None) -> dict:
    settings = settings or load_settings()
    day = day or today(settings)
    ai = AIClient(settings)
    news_pack = get_or_fetch_news(settings, day)
    english_pack = build_english_pack(ai, day, news_pack)
    save_daily_cache(settings, "english", day, english_pack)

    content = "\n\n".join(
        [
            render_english_pack(english_pack),
            "-" * 24,
            render_news_pack(news_pack),
        ]
    )
    return {
        "slot": "morning",
        "title": "Kovan 早间成长推送",
        "date_label": day.isoformat(),
        "content": content,
        "remark": "完成英语输入和新闻精读后，用 3 句话复述今天最重要的一条新闻。",
    }


def build_evening_message(settings: Settings | None = None, day: date | None = None) -> dict:
    settings = settings or load_settings()
    day = day or today(settings)
    training = training_for_day(settings, day)
    meal_plan = meal_plan_for_day(day)
    save_daily_cache(settings, "training", day, training)
    save_daily_cache(settings, "nutrition", day, meal_plan)

    content = "\n\n".join(
        [
            render_training(training),
            "-" * 24,
            render_meal_plan(meal_plan),
        ]
    )
    return {
        "slot": "evening",
        "title": "Kovan 晚间训练与饮食",
        "date_label": day.isoformat(),
        "content": content,
        "remark": "今晚只要完成计划的 80%，也算把系统往前推进了一天。",
    }


def send_morning(
    settings: Settings | None = None, dry_run: bool = False, day: date | None = None
) -> dict:
    settings = settings or load_settings()
    message = build_morning_message(settings, day)
    return deliver(settings, message, dry_run=dry_run)


def send_evening(
    settings: Settings | None = None, dry_run: bool = False, day: date | None = None
) -> dict:
    settings = settings or load_settings()
    message = build_evening_message(settings, day)
    return deliver(settings, message, dry_run=dry_run)


def deliver(settings: Settings, message: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(json.dumps(message, ensure_ascii=False, indent=2))
        return {"dry_run": True, "message": message}

    client = WeChatClient(settings)
    results = client.broadcast(
        slot=message["slot"],
        title=message["title"],
        date_label=message["date_label"],
        content=message["content"],
        remark=message["remark"],
    )
    logger.info("Delivered %s message with %s template calls.", message["slot"], len(results))
    return {"dry_run": False, "results": results}
