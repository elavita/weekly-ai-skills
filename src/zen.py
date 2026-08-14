from __future__ import annotations

import json
from typing import Any

import requests


REQUIRED_KEYS = {"summary", "highlights", "use_cases", "xiaohongshu", "xiaoheihe"}


def fallback_copy(repo: dict[str, Any]) -> dict[str, Any]:
    description = repo.get("description") or "仓库暂未提供简介。"
    return {
        "summary": f"{repo['full_name']}：{description}",
        "highlights": [
            f"GitHub Stars：{repo.get('stargazers_count', 0):,}",
            f"主要语言：{repo.get('language') or '未标注'}",
            "内容来自公开仓库元数据，发布前建议人工核对 README。",
        ],
        "use_cases": ["评估其在 AI Agent、MCP 或开发工具工作流中的适用性"],
        "xiaohongshu": f"发现一个值得关注的 AI 项目：{repo['full_name']}。{description} 发布前请先核对许可证和数据安全要求。",
        "xiaoheihe": f"本期项目：{repo['full_name']}（{repo.get('stargazers_count', 0):,} Stars）。{description}",
        "generation": "fallback",
    }


def _validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or not REQUIRED_KEYS.issubset(data):
        raise ValueError("Zen 返回缺少必需字段")
    if not isinstance(data["summary"], str) or not isinstance(data["highlights"], list):
        raise ValueError("Zen 返回字段类型错误")
    if not isinstance(data["use_cases"], list) or not isinstance(data["xiaohongshu"], str) or not isinstance(data["xiaoheihe"], str):
        raise ValueError("Zen 返回字段类型错误")
    data["generation"] = "zen"
    return data


def generate_copy(
    repo: dict[str, Any],
    config: dict[str, Any],
    api_key: str | None,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    if not api_key:
        return fallback_copy(repo)
    session = session or requests.Session()
    endpoint = config["endpoint"].rstrip("/") + "/chat/completions"
    schema_instruction = (
        "只输出严格 JSON 对象，不要 Markdown。字段必须为 summary:string, highlights:string[], "
        "use_cases:string[], xiaohongshu:string, xiaoheihe:string。不得编造未给出的功能。"
    )
    metadata = {
        "name": repo["full_name"],
        "description": repo.get("description"),
        "url": repo["html_url"],
        "stars": repo.get("stargazers_count"),
        "language": repo.get("language"),
        "created_at": repo.get("created_at"),
        "topics": repo.get("topics", []),
    }
    auth_value = f"{config.get('auth_scheme', 'Bearer')} {api_key}".strip()
    headers = {config.get("auth_header", "Authorization"): auth_value, "Content-Type": "application/json"}
    payload = {
        "model": config["model"],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": schema_instruction},
            {"role": "user", "content": json.dumps(metadata, ensure_ascii=False)},
        ],
    }
    try:
        response = session.post(endpoint, headers=headers, json=payload, timeout=config["timeout_seconds"])
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return _validate(json.loads(content))
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return fallback_copy(repo)
