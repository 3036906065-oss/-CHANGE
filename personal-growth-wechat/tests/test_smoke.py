from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from personal_growth_push.config import Settings
from personal_growth_push.services.fitness import training_for_day
from personal_growth_push.services.nutrition import meal_plan_for_day


def fake_settings() -> Settings:
    return Settings(
        project_root=ROOT,
        data_dir=ROOT / "data",
        timezone="Asia/Shanghai",
        plan_start_date=date(2026, 6, 1),
        openai_api_key="",
        openai_model="gpt-5.4-mini",
        openai_timeout_seconds=60,
        wechat_app_id="",
        wechat_app_secret="",
        wechat_openids=(),
        wechat_template_id="",
        wechat_template_id_morning="",
        wechat_template_id_evening="",
        wechat_max_content_chars=1400,
        wechat_verify_token="test_token",
        morning_hour=7,
        morning_minute=30,
        news_fetch_hour=7,
        news_fetch_minute=0,
        evening_hour=18,
        evening_minute=0,
        news_feeds=(),
        rss_timeout_seconds=15,
    )


def test_monday_training_is_push():
    plan = training_for_day(fake_settings(), date(2026, 6, 1))
    assert plan["title"] == "Push"
    assert any(item["name"] == "杠铃卧推" for item in plan["exercises"])


def test_meal_plan_hits_target_range():
    plan = meal_plan_for_day(date(2026, 6, 1))
    assert 2300 <= plan["totals"]["kcal"] <= 2400
    assert plan["totals"]["protein"] >= 170
