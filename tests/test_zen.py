from __future__ import annotations

import json

import pytest

from src.zen import _validate, fallback_copy, generate_copy


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
    "endpoint": "https://integrate.api.nvidia.com/v1",
    "model": "minimaxai/minimax-m3",
    "auth_header": "Authorization",
    "auth_scheme": "Bearer",
    "timeout_seconds": 10,
}
CONTENT_CONFIG = {
    "language": "zh-CN",
    "audience": "关注 AI Agent 的中文开发者",
}


def test_missing_key_uses_fallback_without_network():
    result = generate_copy(REPO, CONFIG, None, CONTENT_CONFIG)
    assert result == fallback_copy(REPO)
    assert result["generation"] == "fallback"
    assert "原始简介：An AI agent" in result["summary"]
    assert result["xiaohongshu"].startswith(result["summary"])


class BrokenSession:
    def post(self, *args, **kwargs):
        raise ValueError("invalid response")


def test_invalid_model_response_uses_fallback():
    result = generate_copy(REPO, CONFIG, "secret", CONTENT_CONFIG, session=BrokenSession())
    assert result["generation"] == "fallback"


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        content = {
            "summary": "这是一个帮助开发者编排 AI 任务的智能体项目。",
            "highlights": ["提供任务编排能力"],
            "use_cases": ["构建自动化开发流程"],
            "xiaohongshu": "这是一个用于编排 AI 任务的项目。适合关注开发效率的用户。",
            "xiaoheihe": "这是一个用于编排 AI 任务的项目，可用于自动化开发流程。",
        }
        return {"choices": [{"message": {"content": json.dumps(content, ensure_ascii=False)}}]}


class CapturingSession:
    def __init__(self):
        self.payload = None

    def post(self, *args, **kwargs):
        self.payload = kwargs["json"]
        return FakeResponse()


def test_prompt_requests_chinese_processing_and_purpose_summary():
    session = CapturingSession()

    result = generate_copy(REPO, CONFIG, "secret", CONTENT_CONFIG, session=session)

    prompt = session.payload["messages"][0]["content"]
    assert "简体中文" in prompt
    assert "翻译、归纳并润色" in prompt
    assert "这个项目是做什么的" in prompt
    assert CONTENT_CONFIG["audience"] in prompt
    assert result["generation"] == "zen"


@pytest.mark.parametrize(
    "field,value",
    [
        ("summary", ""),
        ("highlights", []),
        ("highlights", [""]),
        ("use_cases", [1]),
        ("xiaohongshu", "   "),
    ],
)
def test_validate_rejects_empty_or_invalid_content(field, value):
    data = {
        "summary": "项目用途",
        "highlights": ["亮点"],
        "use_cases": ["场景"],
        "xiaohongshu": "小红书正文",
        "xiaoheihe": "小黑盒正文",
    }
    data[field] = value

    with pytest.raises(ValueError):
        _validate(data)
