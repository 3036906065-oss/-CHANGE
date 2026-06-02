from __future__ import annotations

from datetime import date
from typing import Any

from ..profile import MEAL_ROTATION


def calories(protein: int, carbs: int, fat: int) -> int:
    return protein * 4 + carbs * 4 + fat * 9


def meal_plan_for_day(day: date) -> dict[str, Any]:
    meals = MEAL_ROTATION[day.weekday()]
    enriched = []
    totals = {"protein": 0, "carbs": 0, "fat": 0, "kcal": 0}
    for meal in meals:
        kcal = calories(meal["protein"], meal["carbs"], meal["fat"])
        item = {**meal, "kcal": kcal}
        enriched.append(item)
        totals["protein"] += meal["protein"]
        totals["carbs"] += meal["carbs"]
        totals["fat"] += meal["fat"]
        totals["kcal"] += kcal
    return {
        "date": day.isoformat(),
        "target": "2300-2400 kcal",
        "meals": enriched,
        "totals": totals,
        "notes": [
            "训练日碳水围绕训练前后；休息日如果不饿，可以把训练后加餐换成酸奶或水果。",
            "每天饮水 2.5-3L，盐分不要过低，减脂期仍要保证训练表现。",
        ],
    }


def render_meal_plan(plan: dict[str, Any]) -> str:
    lines = [f"饮食目标：{plan['target']}", ""]
    for meal in plan["meals"]:
        lines.append(f"{meal['name']}：{meal['items']}")
        lines.append(
            f"  蛋白 {meal['protein']}g | 碳水 {meal['carbs']}g | "
            f"脂肪 {meal['fat']}g | {meal['kcal']} kcal"
        )
    totals = plan["totals"]
    lines.extend(
        [
            "",
            "全天合计：",
            f"蛋白 {totals['protein']}g | 碳水 {totals['carbs']}g | "
            f"脂肪 {totals['fat']}g | {totals['kcal']} kcal",
            "",
            "执行提示：",
        ]
    )
    lines.extend(f"- {note}" for note in plan["notes"])
    return "\n".join(lines)
