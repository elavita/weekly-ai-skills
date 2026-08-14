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
    assert state_path.read_text(encoding="utf-8") == original
