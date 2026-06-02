from __future__ import annotations

import hashlib
import hmac
import logging

from flask import Flask, Response, jsonify, request

from .config import Settings, load_settings

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SETTINGS"] = settings or load_settings()

    @app.get("/")
    def index() -> Response:
        return jsonify(
            {
                "name": "Kovan personal growth WeChat webhook",
                "status": "ok",
                "wechat_route": "/wechat",
            }
        )

    @app.get("/health")
    def health() -> Response:
        current: Settings = app.config["SETTINGS"]
        return jsonify(
            {
                "status": "ok",
                "wechat_token_configured": bool(current.wechat_verify_token),
                "wechat_push_configured": current.wechat_enabled,
                "timezone": current.timezone,
            }
        )

    @app.route("/wechat", methods=["GET", "POST"])
    def wechat() -> Response | tuple[str, int]:
        current: Settings = app.config["SETTINGS"]
        if request.method == "GET":
            signature = request.args.get("signature", "")
            timestamp = request.args.get("timestamp", "")
            nonce = request.args.get("nonce", "")
            echostr = request.args.get("echostr", "")

            if verify_wechat_signature(
                token=current.wechat_verify_token,
                signature=signature,
                timestamp=timestamp,
                nonce=nonce,
            ):
                return Response(echostr, mimetype="text/plain")

            logger.warning("Invalid WeChat signature from %s", request.remote_addr)
            return "forbidden", 403

        # The current system only needs URL verification. Returning "success"
        # prevents WeChat from retrying if a test message reaches this endpoint.
        return Response("success", mimetype="text/plain")

    return app


def verify_wechat_signature(
    *, token: str, signature: str, timestamp: str, nonce: str
) -> bool:
    if not token or not signature or not timestamp or not nonce:
        return False
    raw = "".join(sorted([token, timestamp, nonce]))
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return hmac.compare_digest(digest, signature)
