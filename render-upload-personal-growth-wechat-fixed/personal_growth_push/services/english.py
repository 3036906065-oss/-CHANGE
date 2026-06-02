from __future__ import annotations

import json
from datetime import date
from typing import Any

from ..openai_client import AIClient
from ..profile import USER_PROFILE

WORD_BANK = [
    {"word": "accountability", "ipa": "/əˌkaʊntəˈbɪləti/", "zh": "责任感；问责", "example": "Accountability helps me train even when motivation is low."},
    {"word": "consistency", "ipa": "/kənˈsɪstənsi/", "zh": "坚持；稳定性", "example": "Consistency matters more than one perfect workout."},
    {"word": "discipline", "ipa": "/ˈdɪsəplɪn/", "zh": "自律；纪律", "example": "Discipline turns a plan into a daily habit."},
    {"word": "recomposition", "ipa": "/ˌriːkɒmpəˈzɪʃn/", "zh": "身体重组", "example": "Body recomposition requires strength training and enough protein."},
    {"word": "calorie", "ipa": "/ˈkæləri/", "zh": "卡路里；热量", "example": "I track calories to keep my diet honest."},
    {"word": "deficit", "ipa": "/ˈdefɪsɪt/", "zh": "赤字；不足", "example": "A small calorie deficit can support fat loss."},
    {"word": "protein", "ipa": "/ˈproʊtiːn/", "zh": "蛋白质", "example": "Protein helps my muscles recover after training."},
    {"word": "carbohydrate", "ipa": "/ˌkɑːrboʊˈhaɪdreɪt/", "zh": "碳水化合物", "example": "Carbohydrates fuel hard lower-body sessions."},
    {"word": "recovery", "ipa": "/rɪˈkʌvəri/", "zh": "恢复", "example": "Good recovery makes the next workout stronger."},
    {"word": "mobility", "ipa": "/moʊˈbɪləti/", "zh": "灵活性；活动度", "example": "Hip mobility improves my squat position."},
    {"word": "compound", "ipa": "/ˈkɑːmpaʊnd/", "zh": "复合的", "example": "Squats and deadlifts are compound lifts."},
    {"word": "intensity", "ipa": "/ɪnˈtensəti/", "zh": "强度", "example": "I raise intensity only when technique stays solid."},
    {"word": "volume", "ipa": "/ˈvɑːljuːm/", "zh": "训练量；容量", "example": "Too much volume can hurt recovery during a cut."},
    {"word": "technique", "ipa": "/tekˈniːk/", "zh": "技术；技巧", "example": "Technique comes before heavier weight."},
    {"word": "priority", "ipa": "/praɪˈɔːrəti/", "zh": "优先事项", "example": "Sleep is a priority during body recomposition."},
    {"word": "sustainable", "ipa": "/səˈsteɪnəbl/", "zh": "可持续的", "example": "A sustainable diet is easier to follow for 90 days."},
    {"word": "strategy", "ipa": "/ˈstrætədʒi/", "zh": "策略", "example": "My strategy is to train hard and eat consistently."},
    {"word": "evidence", "ipa": "/ˈevɪdəns/", "zh": "证据", "example": "I prefer evidence-based training advice."},
    {"word": "adaptation", "ipa": "/ˌædæpˈteɪʃn/", "zh": "适应", "example": "Strength is an adaptation to repeated stress."},
    {"word": "capacity", "ipa": "/kəˈpæsəti/", "zh": "能力；容量", "example": "Cardio improves my work capacity."},
    {"word": "headline", "ipa": "/ˈhedlaɪn/", "zh": "新闻标题", "example": "I read the headline before studying the article."},
    {"word": "summary", "ipa": "/ˈsʌməri/", "zh": "摘要", "example": "A short summary helps me understand the main point."},
    {"word": "source", "ipa": "/sɔːrs/", "zh": "来源", "example": "Reuters is a major international news source."},
    {"word": "context", "ipa": "/ˈkɑːntekst/", "zh": "背景；语境", "example": "Context makes a difficult news story clearer."},
    {"word": "analysis", "ipa": "/əˈnæləsɪs/", "zh": "分析", "example": "Good analysis explains why the event matters."},
    {"word": "policy", "ipa": "/ˈpɑːləsi/", "zh": "政策", "example": "New policy can affect markets and daily life."},
    {"word": "economy", "ipa": "/ɪˈkɑːnəmi/", "zh": "经济", "example": "The global economy changes quickly."},
    {"word": "inflation", "ipa": "/ɪnˈfleɪʃn/", "zh": "通货膨胀", "example": "Inflation can make food and energy more expensive."},
    {"word": "negotiation", "ipa": "/nɪˌɡoʊʃiˈeɪʃn/", "zh": "谈判", "example": "Negotiation is often slow in international politics."},
    {"word": "agreement", "ipa": "/əˈɡriːmənt/", "zh": "协议；一致", "example": "The two sides reached a trade agreement."},
    {"word": "security", "ipa": "/sɪˈkjʊrəti/", "zh": "安全", "example": "Cybersecurity is becoming more important."},
    {"word": "regulation", "ipa": "/ˌreɡjuˈleɪʃn/", "zh": "监管；规定", "example": "AI regulation is a major technology issue."},
    {"word": "innovation", "ipa": "/ˌɪnəˈveɪʃn/", "zh": "创新", "example": "Innovation can create new industries."},
    {"word": "investment", "ipa": "/ɪnˈvestmənt/", "zh": "投资", "example": "Investment in chips has grown quickly."},
    {"word": "infrastructure", "ipa": "/ˈɪnfrəstrʌktʃər/", "zh": "基础设施", "example": "AI needs powerful computing infrastructure."},
    {"word": "semiconductor", "ipa": "/ˌsemikənˈdʌktər/", "zh": "半导体", "example": "Semiconductors are essential for modern electronics."},
    {"word": "competition", "ipa": "/ˌkɑːmpəˈtɪʃn/", "zh": "竞争", "example": "Competition between companies can speed up innovation."},
    {"word": "cooperation", "ipa": "/koʊˌɑːpəˈreɪʃn/", "zh": "合作", "example": "International cooperation is needed for climate action."},
    {"word": "challenge", "ipa": "/ˈtʃælɪndʒ/", "zh": "挑战", "example": "The main challenge is staying consistent."},
    {"word": "opportunity", "ipa": "/ˌɑːpərˈtuːnəti/", "zh": "机会", "example": "Every morning is an opportunity to learn."},
    {"word": "resilience", "ipa": "/rɪˈzɪliəns/", "zh": "韧性", "example": "Resilience helps me recover from setbacks."},
    {"word": "momentum", "ipa": "/moʊˈmentəm/", "zh": "势头；动量", "example": "A small win can create momentum for the day."},
    {"word": "deliberate", "ipa": "/dɪˈlɪbərət/", "zh": "刻意的；深思熟虑的", "example": "Deliberate practice improves my English faster."},
    {"word": "fluency", "ipa": "/ˈfluːənsi/", "zh": "流利度", "example": "Speaking every day builds fluency."},
    {"word": "pronunciation", "ipa": "/prəˌnʌnsiˈeɪʃn/", "zh": "发音", "example": "I repeat sentences to improve pronunciation."},
    {"word": "comprehension", "ipa": "/ˌkɑːmprɪˈhenʃn/", "zh": "理解", "example": "Listening comprehension improves with daily practice."},
    {"word": "perspective", "ipa": "/pərˈspektɪv/", "zh": "视角；观点", "example": "News gives me a wider perspective."},
    {"word": "evaluate", "ipa": "/ɪˈvæljueɪt/", "zh": "评估", "example": "I evaluate my progress every week."},
    {"word": "predict", "ipa": "/prɪˈdɪkt/", "zh": "预测", "example": "Analysts try to predict market trends."},
    {"word": "consequence", "ipa": "/ˈkɑːnsəkwens/", "zh": "后果；结果", "example": "A policy change can have global consequences."},
    {"word": "statement", "ipa": "/ˈsteɪtmənt/", "zh": "声明；陈述", "example": "The company released a statement on Monday."},
    {"word": "investigate", "ipa": "/ɪnˈvestɪɡeɪt/", "zh": "调查", "example": "Officials will investigate the incident."},
    {"word": "approve", "ipa": "/əˈpruːv/", "zh": "批准；同意", "example": "The committee approved the new plan."},
    {"word": "restrict", "ipa": "/rɪˈstrɪkt/", "zh": "限制", "example": "Some countries restrict exports of advanced chips."},
    {"word": "expand", "ipa": "/ɪkˈspænd/", "zh": "扩大；扩张", "example": "The company plans to expand overseas."},
    {"word": "decline", "ipa": "/dɪˈklaɪn/", "zh": "下降；拒绝", "example": "Oil prices declined after the report."},
    {"word": "surge", "ipa": "/sɜːrdʒ/", "zh": "激增", "example": "Demand for AI chips surged this year."},
    {"word": "stable", "ipa": "/ˈsteɪbl/", "zh": "稳定的", "example": "A stable routine reduces decision fatigue."},
    {"word": "maintain", "ipa": "/meɪnˈteɪn/", "zh": "保持；维护", "example": "I maintain good form on every rep."},
    {"word": "measure", "ipa": "/ˈmeʒər/", "zh": "衡量；措施", "example": "I measure progress with weight, photos, and strength."},
    {"word": "objective", "ipa": "/əbˈdʒektɪv/", "zh": "目标；客观的", "example": "My objective is to reach 75 kilograms."},
    {"word": "efficient", "ipa": "/ɪˈfɪʃnt/", "zh": "高效的", "example": "An efficient workout saves time and energy."},
    {"word": "accurate", "ipa": "/ˈækjərət/", "zh": "准确的", "example": "Accurate tracking prevents hidden calories."},
    {"word": "essential", "ipa": "/ɪˈsenʃl/", "zh": "必要的；核心的", "example": "Protein is essential for muscle repair."},
    {"word": "gradual", "ipa": "/ˈɡrædʒuəl/", "zh": "逐渐的", "example": "Gradual progress is easier to sustain."},
    {"word": "monitor", "ipa": "/ˈmɑːnɪtər/", "zh": "监控；观察", "example": "I monitor sleep and training performance."},
    {"word": "fatigue", "ipa": "/fəˈtiːɡ/", "zh": "疲劳", "example": "Fatigue can reduce strength in heavy sets."},
    {"word": "stimulus", "ipa": "/ˈstɪmjələs/", "zh": "刺激", "example": "Muscles grow when the stimulus is strong enough."},
    {"word": "adapt", "ipa": "/əˈdæpt/", "zh": "适应；调整", "example": "I adapt the plan when recovery is poor."},
    {"word": "confidence", "ipa": "/ˈkɑːnfɪdəns/", "zh": "信心", "example": "Daily practice builds confidence in speaking."},
    {"word": "clarify", "ipa": "/ˈklærəfaɪ/", "zh": "澄清；说明", "example": "Writing in English helps clarify my thinking."},
    {"word": "brief", "ipa": "/briːf/", "zh": "简短的", "example": "I write a brief opinion after reading the news."},
    {"word": "argument", "ipa": "/ˈɑːrɡjumənt/", "zh": "论点；争论", "example": "A strong argument needs evidence."},
    {"word": "impact", "ipa": "/ˈɪmpækt/", "zh": "影响", "example": "The news may have a major impact on markets."},
    {"word": "trend", "ipa": "/trend/", "zh": "趋势", "example": "AI remains a powerful technology trend."},
    {"word": "forecast", "ipa": "/ˈfɔːrkæst/", "zh": "预测；预报", "example": "The forecast suggests slower economic growth."},
    {"word": "priority", "ipa": "/praɪˈɔːrəti/", "zh": "优先事项", "example": "My top priority is showing up every day."},
    {"word": "routine", "ipa": "/ruːˈtiːn/", "zh": "日常安排", "example": "A simple routine makes learning automatic."},
    {"word": "reflection", "ipa": "/rɪˈflekʃn/", "zh": "反思", "example": "Reflection helps me learn from mistakes."},
]


def build_english_pack(ai: AIClient, day: date, news_pack: dict[str, Any] | None) -> dict[str, Any]:
    system_prompt = (
        "You are Kovan's strict but encouraging English coach. Generate useful daily study "
        "content for a Chinese learner. Use clean JSON only."
    )
    news_context = json.dumps((news_pack or {}).get("items", [])[:3], ensure_ascii=False)
    user_prompt = f"""
Student profile:
{json.dumps(USER_PROFILE, ensure_ascii=False)}

Date: {day.isoformat()}
News context:
{news_context}

Return strict JSON:
{{
  "words": [
    {{"word": "example", "ipa": "/.../", "zh": "中文解释", "example": "An English example sentence."}}
  ],
  "reading": {{
    "title": "English title",
    "article": "180-220 words of English news-style reading based on today's context or broad international affairs",
    "key_points_zh": ["中文要点 1", "中文要点 2", "中文要点 3"],
    "sentence_notes": [
      {{"sentence": "A useful sentence from the article.", "explanation_zh": "中文讲解"}}
    ]
  }},
  "listening_task": "A concrete 10-minute listening task",
  "output_practice": "A concrete English speaking or writing task"
}}

Rules:
- words must contain exactly 40 items.
- Prefer B1-B2 words, with a few C1 news words.
- Examples should be related to fitness, discipline, news, study, or personal growth.
- Do not mention that you are an AI.
"""
    data = ai.generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        fallback=lambda: fallback_english_pack(day, news_pack),
    )
    return normalize_english_pack(data, day, news_pack)


def normalize_english_pack(
    data: dict[str, Any], day: date, news_pack: dict[str, Any] | None
) -> dict[str, Any]:
    fallback = fallback_english_pack(day, news_pack)
    words = data.get("words", [])
    if not isinstance(words, list):
        words = []
    normalized_words = []
    for item in words:
        if not isinstance(item, dict):
            continue
        word = str(item.get("word", "")).strip()
        ipa = str(item.get("ipa", "")).strip()
        zh = str(item.get("zh", "")).strip()
        example = str(item.get("example", "")).strip()
        if word and zh and example:
            normalized_words.append(
                {"word": word, "ipa": ipa or "/", "zh": zh, "example": example}
            )
    for item in fallback["words"]:
        if len(normalized_words) >= 40:
            break
        if item["word"].lower() not in {w["word"].lower() for w in normalized_words}:
            normalized_words.append(item)

    reading = data.get("reading") if isinstance(data.get("reading"), dict) else {}
    normalized = {
        "date": day.isoformat(),
        "words": normalized_words[:40],
        "reading": {
            "title": str(reading.get("title") or fallback["reading"]["title"]),
            "article": str(reading.get("article") or fallback["reading"]["article"]),
            "key_points_zh": reading.get("key_points_zh")
            if isinstance(reading.get("key_points_zh"), list)
            else fallback["reading"]["key_points_zh"],
            "sentence_notes": reading.get("sentence_notes")
            if isinstance(reading.get("sentence_notes"), list)
            else fallback["reading"]["sentence_notes"],
        },
        "listening_task": str(
            data.get("listening_task") or fallback["listening_task"]
        ),
        "output_practice": str(
            data.get("output_practice") or fallback["output_practice"]
        ),
    }
    return normalized


def fallback_english_pack(day: date, news_pack: dict[str, Any] | None) -> dict[str, Any]:
    offset = (day.toordinal() * 7) % len(WORD_BANK)
    words = []
    seen = set()
    index = 0
    while len(words) < 40 and index < len(WORD_BANK) * 2:
        item = WORD_BANK[(offset + index) % len(WORD_BANK)]
        index += 1
        key = item["word"].lower()
        if key in seen:
            continue
        seen.add(key)
        words.append(item)
    first_news = ((news_pack or {}).get("items") or [{}])[0]
    title = first_news.get("title_en") or "Why Daily Systems Beat Motivation"
    summary = first_news.get("summary_en") or (
        "A daily system is more reliable than motivation because it reduces the number of "
        "decisions you need to make. When training, eating, reading, and listening happen "
        "at fixed times, progress becomes easier to repeat."
    )
    article = (
        f"{title}. {summary} For a learner, the useful lesson is simple: turn important "
        "information into a repeatable routine. Read the headline first, underline the main "
        "verb, and ask why the event matters. Then write one short opinion in English. This "
        "method connects vocabulary, grammar, and real-world knowledge. It also trains you "
        "to think clearly under a small time limit. Over ninety days, these small repetitions "
        "can build a stronger body and a sharper English habit at the same time."
    )
    return {
        "date": day.isoformat(),
        "words": words,
        "reading": {
            "title": title,
            "article": article,
            "key_points_zh": [
                "先抓标题和核心动词，快速判断新闻主题。",
                "把新闻和自己的观点连接起来，训练英文输出。",
                "每天固定流程比偶尔突击更容易形成长期能力。",
            ],
            "sentence_notes": [
                {
                    "sentence": "This method connects vocabulary, grammar, and real-world knowledge.",
                    "explanation_zh": "connect A, B, and C 表示“把三者连接起来”，适合写学习方法或新闻影响。",
                }
            ],
        },
        "listening_task": "用 BBC Learning English 或 Reuters 视频听 10 分钟：第一遍只抓主题，第二遍记录 5 个关键词，最后跟读 3 句。",
        "output_practice": "用英文写 80-120 词：What is the most important news today, and how might it affect young people?",
    }


def render_english_pack(pack: dict[str, Any]) -> str:
    lines = ["英语学习：", "", "40 个单词："]
    for index, item in enumerate(pack["words"], start=1):
        lines.append(
            f"{index}. {item['word']} {item.get('ipa', '')} - {item['zh']}"
        )
        lines.append(f"   例句：{item['example']}")

    reading = pack["reading"]
    lines.extend(
        [
            "",
            "英文新闻精读：",
            f"标题：{reading['title']}",
            reading["article"],
            "",
            "中文要点：",
        ]
    )
    for point in reading.get("key_points_zh", []):
        lines.append(f"- {point}")
    lines.append("句子精讲：")
    for note in reading.get("sentence_notes", [])[:3]:
        if isinstance(note, dict):
            lines.append(f"- {note.get('sentence', '')}")
            lines.append(f"  {note.get('explanation_zh', '')}")

    lines.extend(
        [
            "",
            f"10 分钟听力任务：{pack['listening_task']}",
            f"英文输出练习：{pack['output_practice']}",
        ]
    )
    return "\n".join(lines)
