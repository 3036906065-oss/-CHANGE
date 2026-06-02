from __future__ import annotations

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import Settings, load_settings
from .jobs import fetch_news_job, send_evening, send_morning

logger = logging.getLogger(__name__)


def run_scheduler(settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    scheduler = BlockingScheduler(timezone=settings.timezone)

    scheduler.add_job(
        lambda: fetch_news_job(settings),
        CronTrigger(
            hour=settings.news_fetch_hour,
            minute=settings.news_fetch_minute,
            timezone=settings.timezone,
        ),
        id="fetch_news",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )
    scheduler.add_job(
        lambda: send_morning(settings),
        CronTrigger(
            hour=settings.morning_hour,
            minute=settings.morning_minute,
            timezone=settings.timezone,
        ),
        id="send_morning",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )
    scheduler.add_job(
        lambda: send_evening(settings),
        CronTrigger(
            hour=settings.evening_hour,
            minute=settings.evening_minute,
            timezone=settings.timezone,
        ),
        id="send_evening",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )

    logger.info(
        "Scheduler started. News %02d:%02d, morning %02d:%02d, evening %02d:%02d (%s).",
        settings.news_fetch_hour,
        settings.news_fetch_minute,
        settings.morning_hour,
        settings.morning_minute,
        settings.evening_hour,
        settings.evening_minute,
        settings.timezone,
    )
    scheduler.start()
