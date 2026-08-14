from __future__ import annotations

import json
from datetime import datetime, timezone

from src import main as main_module


def test_dry_run_does_not_modify_state(tmp_path, monkeypatch):
    config = {
        "github": {
            "min_stars": 500,
            "windows_days": [7, 30, 90, 180, 365],
            "max_projects": 5,
            "search_terms": ["AI agent"],
            "per_page": 100,
            "max_pages_per_query": 1,
            "request_timeout_seconds": 10,
        },
        "zen": {
            "endpoint": "https://opencode.ai/zen/v1",
            "model": "deepseek-v4-flash-free",
            "auth_header": "Authorization",
            "auth_scheme": "Bearer",
            "timeout_seconds": 10,
        },
        "content": {},
        "images": {
            "width": 1200,
            "height": 630,
            "max_bytes": 100000,
            "timeout_seconds": 5,
            "allowed_content_types": ["image/png"],
            "readme_keywords": ["demo"],
            "badge_markers": ["badge"],
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    state_path = tmp_path / "state" / "published.json"
    state_path.parent.mkdir()
    original = '{"node_ids": ["OLD"]}\n'
    state_path.write_text(original, encoding="utf-8")

    class FakeSearcher:
        def __init__(self, config, token):
            pass

        def discover(self, published_ids, now):
            assert published_ids == {"OLD"}
            return 365, []

    monkeypatch.setattr(main_module, "GitHubSearcher", FakeSearcher)
    output = main_module.run(config_path, dry_run=True, now=datetime(2026, 8, 14, tzinfo=timezone.utc))

    assert output.name == "2026-W33"
def test_prepare_project_passes_content_config_to_model(tmp_path, monkeypatch):
    repo = {
        "node_id": "R_2",
        "full_name": "owner/project",
        "html_url": "https://github.com/owner/project",
        "url": "https://api.github.com/repos/owner/project",
        "description": "An AI agent",
        "stargazers_count": 900,
        "language": "Python",
        "created_at": "2026-08-10T00:00:00Z",
        "topics": [],
    }
    config = {
        "github": {"request_timeout_seconds": 10},
        "content": {"language": "zh-CN", "audience": "中文开发者"},
        "images": {
            "width": 1200,
            "height": 630,
            "max_bytes": 100000,
            "timeout_seconds": 5,
            "allowed_content_types": ["image/png"],
            "readme_keywords": ["demo"],
            "badge_markers": ["badge"],
        },
        "zen": {"endpoint": "https://example.test", "model": "test", "timeout_seconds": 5},
    }
    captured = {}

    monkeypatch.setattr(main_module, "fetch_readme", lambda *args: "")
    monkeypatch.setattr(main_module, "download_image", lambda *args: False)
    monkeypatch.setattr(main_module, "make_info_card", lambda *args: None)

    def fake_generate(repo, zen_config, key, content_config):
        captured["content"] = content_config
        return {
            "summary": "项目用途",
            "highlights": ["亮点"],
            "use_cases": ["场景"],
            "xiaohongshu": "小红书",
            "xiaoheihe": "小黑盒",
            "generation": "fallback",
        }

    monkeypatch.setattr(main_module, "generate_copy", fake_generate)
    main_module.prepare_project(repo, tmp_path, config, None, None)

    assert captured["content"] == config["content"]
