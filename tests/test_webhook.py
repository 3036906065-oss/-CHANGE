from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from personal_growth_push.webhook import verify_wechat_signature


def test_wechat_signature_verification():
    token = "test_token"
    timestamp = "1710000000"
    nonce = "abc123"
    signature = hashlib.sha1("".join(sorted([token, timestamp, nonce])).encode()).hexdigest()

    assert verify_wechat_signature(
        token=token,
        signature=signature,
        timestamp=timestamp,
        nonce=nonce,
    )


def test_wechat_signature_rejects_invalid_signature():
    assert not verify_wechat_signature(
        token="test_token",
        signature="wrong",
        timestamp="1710000000",
        nonce="abc123",
    )
