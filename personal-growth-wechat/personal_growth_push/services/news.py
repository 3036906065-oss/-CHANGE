from __future__ import annotations

import html
import json
import logging
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Iterable

import feedparser
import requests

from ..config import Settings
from ..openai_client import AIClient

logger = logging.getLogger(__name__)

IMPORTANT_KEYWORDS = {
    "war": 8,
    "conflict": 8,
    "ceasefire": 8,
    "election": 7,
    "president": 5,
    "minister": 5,
    "china": 5,
    "u.s.": 5,
    "us ": 5,
    "europe": 4,
    "russia": 5,
    "ukraine": 5,
    "israel": 5,
    "gaza": 5,
    "market": 4,
    "economy": 5,
    "inflation": 5,
    "central bank": 5,
    "ai": 4,
    "artificial intelligence": 7,
    "chip": 4,
    "semiconductor": 5,
    "climate": 4,
    "court": 4,
    "sanction": 5,
}

VOCAB_ZH = {
    "election": "选举",
    "inflation": "通货膨胀",
    "ceasefire": "停火",
    "sanction": "制裁",
    "minister": "部长；大臣",
    "economy": "经济",
    "market": "市场",
    "policy": "政策",
    "summit": "峰会",
    "conflict": "冲突",
    "semiconductor": "半导体",
    "intelligence": "情报；智能",
    "regulation": "监管",
    "climate": "气候",
    "security": "安全",
    "investment": "投资",
}


@dataclass
class NewsArticle:
    title: str
    summary: str
    url: str
    source: str
    published_at: str
    score: float


def build_news_pack(settings: Settings, ai: AIClient, day: date) -> dict[str, Any]:
    articles = fetch_rss_articles(settings)
    selected = select_top_articles(articles, limit=10)
    if not selected:
        return no_news_pack(day)

    prompt_articles = [asdict(item) for item in selected]
    system_prompt = (
        "You are a careful bilingual news editor. Select the three most globally important "
        "items from supplied RSS candidates. Do not invent facts, dates, sources, quotes, "
        "or URLs. If the provided summary is thin, say only what can be inferred from the title."
    )
    user_prompt = f"""
Date: {day.isoformat()}
Audience: Kovan, a Chinese native speaker building an English news habit.

Return strict JSON with this shape:
{{
  "items": [
    {{
      "title_en": "English headline",
      "source": "source name",
      "url": "article url",
      "summary_en": "45-70 English words based only on supplied article data",
      "explanation_zh": "用中文解释新闻背景和为什么重要，70-110 字",
      "vocab": [
        {{"word": "word", "meaning_zh": "中文释义"}},
        {{"word": "word", "meaning_zh": "中文释义"}},
        {{"word": "word", "meaning_zh": "中文释义"}}
      ],
      "difficulty": "B1/B2/C1"
    }}
  ]
}}

Candidates:
{json.dumps(prompt_articles, ensure_ascii=False)}
"""
    data = ai.generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        fallback=lambda: fallback_news_pack(day, selected),
    )
    items = _valid_items(data.get("items", []))
    if len(items) < 3:
        return fallback_news_pack(day, selected)
    return {
        "date": day.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fetched_count": len(articles),
        "items": items[:3],
    }


def fetch_rss_articles(settings: Settings) -> list[NewsArticle]:
    articles: list[NewsArticle] = []
    for descriptor in settings.news_feeds:
        source_name, url = parse_feed_descriptor(descriptor)
        try:
            response = requests.get(
                url,
                timeout=settings.rss_timeout_seconds,
                headers={"User-Agent": "personal-growth-wechat/1.0"},
            )
            response.raise_for_status()
            parsed = feedparser.parse(response.content)
        except Exception:
            logger.exception("Failed to fetch RSS feed: %s", descriptor)
            continue

        feed_title = parsed.feed.get("title", source_name) if parsed.feed else source_name
        for entry in parsed.entries[:30]:
            title = clean_text(entry.get("title", ""))
            if not title:
                continue
            summary = clean_text(
                entry.get("summary")
                or entry.get("description")
                or entry.get("subtitle")
                or ""
            )
            url = entry.get("link", "")
            published = parse_published(entry)
            source_info = entry.get("source") or {}
            source_title = source_info.get("title") if hasattr(source_info, "get") else ""
            source = source_title or feed_title or source_name
            articles.append(
                NewsArticle(
                    title=title,
                    summary=summary[:500],
                    url=url,
                    source=clean_text(source),
                    published_at=published.isoformat() if published else "",
                    score=score_article(title, summary, source_name, published),
                )
            )
    return dedupe_articles(articles)


def parse_feed_descriptor(descriptor: str) -> tuple[str, str]:
    if "|" not in descriptor:
        return descriptor, descriptor
    name, url = descriptor.split("|", 1)
    return name.strip(), url.strip()


def parse_published(entry: Any) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime(*parsed[:6], tzinfo=timezone.utc)
    raw = entry.get("published") or entry.get("updated")
    if raw:
        try:
            dt = parsedate_to_datetime(raw)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            return None
    return None


def clean_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score_article(
    title: str, summary: str, source_name: str, published: datetime | None
) -> float:
    text = f"{title} {summary}".lower()
    score = 0.0
    for keyword, weight in IMPORTANT_KEYWORDS.items():
        if keyword in text:
            score += weight
    source_lower = source_name.lower()
    if "reuters" in source_lower:
        score += 4
    if "bbc" in source_lower:
        score += 3
    if published:
        hours_old = max(0.0, (datetime.now(timezone.utc) - published).total_seconds() / 3600)
        score += max(0.0, 12 - min(hours_old, 24) * 0.4)
    return score


def dedupe_articles(articles: Iterable[NewsArticle]) -> list[NewsArticle]:
    seen: set[str] = set()
    unique: list[NewsArticle] = []
    for article in sorted(articles, key=lambda item: item.score, reverse=True):
        key = re.sub(r"[^a-z0-9]+", "", article.title.lower())[:80]
        if key in seen:
            continue
        seen.add(key)
        unique.append(article)
    return unique


def select_top_articles(articles: list[NewsArticle], limit: int) -> list[NewsArticle]:
    return sorted(articles, key=lambda item: item.score, reverse=True)[:limit]


def fallback_news_pack(day: date, selected: list[NewsArticle]) -> dict[str, Any]:
    items = []
    for article in selected[:3]:
        text = f"{article.title} {article.summary}"
        items.append(
            {
                "title_en": article.title,
                "source": article.source,
                "url": article.url,
                "summary_en": summarize_fallback(article),
                "explanation_zh": "这是一条来自 RSS 的重点新闻候选。当前模型不可用，所以系统保留标题和摘要，并建议打开原文核对更多背景。",
                "vocab": fallback_vocab(text),
                "difficulty": difficulty_for(text),
            }
        )
    return {
        "date": day.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fetched_count": len(selected),
        "items": items,
    }


def no_news_pack(day: date) -> dict[str, Any]:
    return {
        "date": day.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fetched_count": 0,
        "items": [
            {
                "title_en": "RSS fetch failed",
                "source": "System",
                "url": "",
                "summary_en": "No current RSS articles were available. Check the deployment network, feed URLs, or retry the fetch job.",
                "explanation_zh": "今天没有抓到新闻内容。请检查部署网络、RSS 地址或稍后重试；系统不会编造当天新闻。",
                "vocab": [
                    {"word": "fetch", "meaning_zh": "抓取"},
                    {"word": "retry", "meaning_zh": "重试"},
                    {"word": "source", "meaning_zh": "来源"},
                ],
                "difficulty": "B1",
            }
        ],
    }


def summarize_fallback(article: NewsArticle) -> str:
    if article.summary:
        return article.summary[:280]
    return f"This item was selected from RSS because its headline appears important: {article.title}"


def fallback_vocab(text: str) -> list[dict[str, str]]:
    words = []
    for raw in re.findall(r"[A-Za-z][A-Za-z-]{5,}", text.lower()):
        word = raw.strip("-")
        if word in {"reuters", "reported", "according", "through"}:
            continue
        meaning = VOCAB_ZH.get(word, "新闻高频词")
        item = {"word": word, "meaning_zh": meaning}
        if item not in words:
            words.append(item)
        if len(words) == 3:
            break
    while len(words) < 3:
        words.append({"word": "policy", "meaning_zh": "政策"})
    return words


def difficulty_for(text: str) -> str:
    words = re.findall(r"[A-Za-z]+", text)
    avg_len = sum(len(word) for word in words) / max(1, len(words))
    if len(words) > 80 or avg_len > 6.0:
        return "C1"
    if len(words) > 35 or avg_len > 5.2:
        return "B2"
    return "B1"


def _valid_items(items: Any) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        return []
    valid = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title_en", "")).strip()
        summary = str(item.get("summary_en", "")).strip()
        if not title or not summary:
            continue
        vocab = item.get("vocab")
        if not isinstance(vocab, list):
            vocab = []
        valid.append(
            {
                "title_en": title,
                "source": str(item.get("source", "")).strip(),
                "url": str(item.get("url", "")).strip(),
                "summary_en": summary,
                "explanation_zh": str(item.get("explanation_zh", "")).strip(),
                "vocab": vocab[:5],
                "difficulty": str(item.get("difficulty", "B2")).strip() or "B2",
            }
        )
    return valid


def render_news_pack(pack: dict[str, Any]) -> str:
    lines = ["国际重点新闻："]
    for index, item in enumerate(pack.get("items", []), start=1):
        lines.extend(
            [
                "",
                f"{index}. {item.get('title_en', '')}",
                f"来源：{item.get('source', '')} | 难度：{item.get('difficulty', 'B2')}",
                f"英文摘要：{item.get('summary_en', '')}",
                f"中文解释：{item.get('explanation_zh', '')}",
                "高频词汇："
            ]
        )
        for vocab in item.get("vocab", []):
            lines.append(f"- {vocab.get('word', '')}: {vocab.get('meaning_zh', '')}")
        if item.get("url"):
            lines.append(f"原文：{item['url']}")
    return "\n".join(lines)
