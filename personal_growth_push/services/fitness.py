from __future__ import annotations

from datetime import date
from typing import Any

from ..config import Settings
from ..profile import TRAINING_PLAN, WEEKDAY_KEYS


def week_number(settings: Settings, day: date) -> int:
    delta = (day - settings.plan_start_date).days
    return max(1, delta // 7 + 1)


def training_for_day(settings: Settings, day: date) -> dict[str, Any]:
    key = WEEKDAY_KEYS[day.weekday()]
    plan = TRAINING_PLAN[key]
    week = week_number(settings, day)
    return {
        "date": day.isoformat(),
        "week": week,
        "day_key": key,
        "title": plan["title"],
        "focus": plan["focus"],
        "exercises": plan["exercises"],
        "progression": progression_advice(week, plan["title"]),
    }


def progression_advice(week: int, title: str) -> str:
    if title == "Rest":
        return "今天不加量。用睡眠、步数和补水把下一周的训练状态垫起来。"
    if title == "Cardio Recovery":
        return "有氧只加时长不加强度：本周若恢复好，可比上周多 5 分钟；腿酸明显就维持原量。"
    if week % 4 == 0:
        return "本周作为降载周：主项重量降 10-15%，组数减少 1 组，动作速度和技术标准不降。"
    if week <= 3:
        return "双进阶：同重量先把每组做到上限次数；全部达标后，下次主项加 2.5kg，上肢辅助加 1-2kg。"
    if week <= 8:
        return "进入稳定推进期：主项保持 RPE 7-8，连续两次完成上限次数再加重量；辅助动作优先加次数。"
    return "最后阶段不要贪重：主项小幅加重量，动作质量下降就回退 2.5-5kg，保持减脂期恢复能力。"


def render_training(training: dict[str, Any]) -> str:
    lines = [
        f"今日训练：{training['title']}（第 {training['week']} 周）",
        f"训练重点：{training['focus']}",
        "",
        "动作安排：",
    ]
    for index, item in enumerate(training["exercises"], start=1):
        lines.append(
            f"{index}. {item['name']} - {item['sets']} 组 x {item['reps']}，"
            f"重量：{item['load']}，休息：{item['rest']}"
        )
        lines.append(f"   要点：{item['note']}")
    lines.extend(["", f"渐进超负荷：{training['progression']}"])
    return "\n".join(lines)
