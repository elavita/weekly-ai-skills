from __future__ import annotations

import json
from typing import Any

import requests


REQUIRED_KEYS = {"summary", "highlights", "use_cases", "xiaohongshu", "xiaoheihe"}


def fallback_copy(repo: dict[str, Any]) -> dict[str, Any]:
    description = repo.get("description")
    original_description = f"原始简介：{description}" if description else "仓库暂未提供简介。"
    summary = f"这是一个值得进一步了解的 AI 项目；{original_description}"
    return {
        "summary": summary,
        "highlights": [
            f"GitHub Stars：{repo.get('stargazers_count', 0):,}",
            f"主要语言：{repo.get('language') or '未标注'}",
            "内容来自公开仓库元数据，发布前建议人工核对 README。",
        ],
        "use_cases": ["评估其在 AI Agent、MCP 或开发工具工作流中的适用性"],
        "xiaohongshu": f"{summary}\n\n项目：{repo['full_name']}。发布前请先核对许可证和数据安全要求。",
        "xiaoheihe": f"{summary}\n\n项目：{repo['full_name']}（{repo.get('stargazers_count', 0):,} Stars）。",
        "generation": "fallback",
    }


def _validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or not REQUIRED_KEYS.issubset(data):
        raise ValueError("模型返回缺少必需字段")
    for field in ("summary", "xiaohongshu", "xiaoheihe"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError("模型返回字段类型或内容错误")
    for field in ("highlights", "use_cases"):
        values = data[field]
        if not isinstance(values, list) or not values:
            raise ValueError("模型返回字段类型或内容错误")
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("模型返回列表内容错误")
    data["generation"] = "zen"
    return data


def generate_copy(
    repo: dict[str, Any],
    config: dict[str, Any],
    api_key: str | None,
    content_config: dict[str, Any] | None = None,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    if not api_key:
        return fallback_copy(repo)
    session = session or requests.Session()
    content_config = content_config or {}
    endpoint = config["endpoint"].rstrip("/") + "/chat/completions"
    language = content_config.get("language", "zh-CN")
    audience = content_config.get("audience", "关注 AI Agent、MCP 与效率工具的中文开发者")
    schema_instruction = (
        "只输出严格 JSON 对象，不要 Markdown。字段必须为 summary:string, highlights:string[], "
        "use_cases:string[], xiaohongshu:string, xiaoheihe:string。"
        f"面向{audience}，使用 {language} 简体中文加工所有解释性内容。"
        "将英文 description 和 topics 翻译、归纳并润色为自然中文，不要直接照抄；"
        "项目名、技术名、API 名称和代码标识可以保留原文。"
        "summary 用一到两句话直接说明这个项目是做什么的、解决什么问题，不要只复述仓库名。"
        "xiaohongshu 和 xiaoheihe 的开头都必须先给出项目用途摘要，再介绍亮点和适用场景；"
        "语气客观、简洁，避免‘姐妹们’、‘白嫖’等过度网感或夸张措辞。"
        "不得编造未给出的功能、效果或使用数据。"
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
