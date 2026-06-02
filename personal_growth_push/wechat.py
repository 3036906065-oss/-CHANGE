from __future__ import annotations

import logging
import time
from typing import Any

import requests

from .config import Settings
from .storage import ensure_data_dir, read_json, write_json

logger = logging.getLogger(__name__)


class WeChatClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        ensure_data_dir(settings)
        self.token_cache_path = settings.data_dir / "wechat_token.json"

    def broadcast(
        self,
        *,
        slot: str,
        title: str,
        date_label: str,
        content: str,
        remark: str = "",
    ) -> list[dict[str, Any]]:
        if not self.settings.wechat_enabled:
            logger.warning("WeChat config is incomplete; skip sending.")
            return []

        template_id = self.settings.template_for(slot)
        chunks = split_text(content, self.settings.wechat_max_content_chars)
        results = []
        for openid in self.settings.wechat_openids:
            for index, chunk in enumerate(chunks, start=1):
                suffix = f"（{index}/{len(chunks)}）" if len(chunks) > 1 else ""
                results.append(
                    self.send_template_message(
                        openid=openid,
                        template_id=template_id,
                        title=f"{title}{suffix}",
                        date_label=date_label,
                        content=chunk,
                        remark=remark,
                    )
                )
        return results

    def send_template_message(
        self,
        *,
        openid: str,
        template_id: str,
        title: str,
        date_label: str,
        content: str,
        remark: str,
    ) -> dict[str, Any]:
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        payload = {
            "touser": openid,
            "template_id": template_id,
            "data": {
                "title": {"value": title},
                "date": {"value": date_label},
                "content": {"value": content},
                "remark": {"value": remark},
            },
        }
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        if data.get("errcode", 0) != 0:
            raise RuntimeError(f"WeChat send failed: {data}")
        return data

    def get_access_token(self) -> str:
        cached = read_json(self.token_cache_path, default={}) or {}
        now = int(time.time())
        if cached.get("access_token") and cached.get("expires_at", 0) > now + 120:
            return cached["access_token"]

        response = requests.get(
            "https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.settings.wechat_app_id,
                "secret": self.settings.wechat_app_secret,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        if "access_token" not in data:
            raise RuntimeError(f"Cannot get WeChat access token: {data}")
        expires_at = now + int(data.get("expires_in", 7200))
        write_json(
            self.token_cache_path,
            {"access_token": data["access_token"], "expires_at": expires_at},
        )
        return data["access_token"]


def split_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current = ""
    for line in text.splitlines():
        candidate = f"{current}\n{line}".strip() if current else line
        if len(candidate) <= limit:
            current = candidate
            continue
        if current:
            chunks.append(current)
            current = ""
        while len(line) > limit:
            chunks.append(line[:limit])
            line = line[limit:]
        current = line
    if current:
        chunks.append(current)
    return chunks
