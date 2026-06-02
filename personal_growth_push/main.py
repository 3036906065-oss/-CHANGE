from __future__ import annotations

import argparse
import json
import logging
from datetime import date

from .config import load_settings
from .jobs import build_evening_message, build_morning_message, fetch_news_job, send_evening, send_morning
from .scheduler import run_scheduler


def main() -> int:
    parser = argparse.ArgumentParser(description="Kovan personal growth WeChat push system")
    parser.add_argument(
        "--env",
        default=None,
        help="Path to .env file. Defaults to project .env.",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Override date as YYYY-MM-DD for preview/testing.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Run the production scheduler.")
    subparsers.add_parser("fetch-news", help="Fetch and cache today's news.")

    morning = subparsers.add_parser("send-morning", help="Send or preview morning push.")
    morning.add_argument("--dry-run", action="store_true", help="Print message instead of sending.")

    evening = subparsers.add_parser("send-evening", help="Send or preview evening push.")
    evening.add_argument("--dry-run", action="store_true", help="Print message instead of sending.")

    subparsers.add_parser("preview-morning", help="Build morning content and print JSON.")
    subparsers.add_parser("preview-evening", help="Build evening content and print JSON.")
    subparsers.add_parser("health", help="Print configuration health.")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    settings = load_settings(args.env)
    target_day = date.fromisoformat(args.date) if args.date else None

    if args.command == "run":
        run_scheduler(settings)
        return 0
    if args.command == "fetch-news":
        print(json.dumps(fetch_news_job(settings, target_day), ensure_ascii=False, indent=2))
        return 0
    if args.command == "send-morning":
        send_morning(settings, dry_run=args.dry_run, day=target_day)
        return 0
    if args.command == "send-evening":
        send_evening(settings, dry_run=args.dry_run, day=target_day)
        return 0
    if args.command == "preview-morning":
        print(json.dumps(build_morning_message(settings, target_day), ensure_ascii=False, indent=2))
        return 0
    if args.command == "preview-evening":
        print(json.dumps(build_evening_message(settings, target_day), ensure_ascii=False, indent=2))
        return 0
    if args.command == "health":
        payload = {
            "openai_enabled": settings.openai_enabled,
            "wechat_enabled": settings.wechat_enabled,
            "wechat_verify_token_configured": bool(settings.wechat_verify_token),
            "timezone": settings.timezone,
            "plan_start_date": settings.plan_start_date.isoformat(),
            "data_dir": str(settings.data_dir),
            "news_feeds": settings.news_feeds,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    parser.error("Unknown command")
    return 2
