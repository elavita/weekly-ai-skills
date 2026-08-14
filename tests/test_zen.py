from __future__ import annotations

from src.zen import fallback_copy, generate_copy


REPO = {
    "full_name": "owner/project",
    "html_url": "https://github.com/owner/project",
    "description": "An AI agent",
    "stargazers_count": 900,
    "language": "Python",
    "created_at": "2026-08-10T00:00:00Z",
    "topics": ["agent"],
}
CONFIG = {
    "endpoint": "https://opencode.ai/zen/v1",
    "model": "deepseek-v4-flash-free",
    "auth_header": "Authorization",
    "auth_scheme": "Bearer",
    "timeout_seconds": 10,
}


def test_missing_key_uses_fallback_without_network():
    result = generate_copy(REPO, CONFIG, None)
    assert result == fallback_copy(REPO)
    assert result["generation"] == "fallback"
    assert "owner/project" in result["summary"]


class BrokenSession:
    def post(self, *args, **kwargs):
        raise ValueError("invalid response")


def test_invalid_zen_response_uses_fallback():
    result = generate_copy(REPO, CONFIG, "secret", session=BrokenSession())
    assert result["generation"] == "fallback"
