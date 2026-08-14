from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from src import main as main_module


def make_config(tmp_path):
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
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "model": "minimaxai/minimax-m3",
            "auth_header": "Authorization",
            "auth_scheme": "Bearer",
            "timeout_seconds": 10,
        },
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
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config, config_path


def make_period_data(tmp_path, period="2026-W33", duplicate=False):
    output = tmp_path / "reports" / period
    images = output / "images"
    images.mkdir(parents=True)
    (images / "project.png").write_bytes(b"existing image")
    project = {
        "repository": {
            "node_id": "R_1",
            "full_name": "owner/project",
            "html_url": "https://github.com/owner/project",
            "description": "An AI agent",
            "stargazers_count": 900,
            "language": "Python",
            "created_at": "2026-08-10T00:00:00Z",
            "topics": ["agent"],
        },
        "copy": {
            "summary": "旧摘要",
            "highlights": ["旧亮点"],
            "use_cases": ["旧场景"],
            "xiaohongshu": "旧小红书",
            "xiaoheihe": "旧小黑盒",
            "generation": "zen",
        },
        "image": {
            "path": "images/project.png",
            "source": "GitHub Open Graph",
            "source_url": "https://example.test/project.png",
        },
    }
    projects = [project, json.loads(json.dumps(project))] if duplicate else [project]
    data = {"period": period, "generated_at": "old", "window_days": 30, "projects": projects}
    (output / "data.json").write_text(json.dumps(data), encoding="utf-8")
    (output / "report.md").write_text("old report", encoding="utf-8")
    return output, project


def test_dry_run_does_not_modify_state(tmp_path, monkeypatch):
    _, config_path = make_config(tmp_path)
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


def test_prepare_project_passes_content_config_to_model(tmp_path, monkeypatch):
    config, _ = make_config(tmp_path)
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


def test_force_refresh_reuses_projects_and_images_without_search(tmp_path, monkeypatch):
    _, config_path = make_config(tmp_path)
    output, old_project = make_period_data(tmp_path)
    state_path = tmp_path / "state" / "published.json"
    state_path.parent.mkdir()
    original_ids = ["OLD", "R_1"]
    state_path.write_text(json.dumps({"node_ids": original_ids, "last_period": "2026-W33"}), encoding="utf-8")

    class ForbiddenSearcher:
        def __init__(self, *args):
            raise AssertionError("force refresh must not search GitHub")

    monkeypatch.setattr(main_module, "GitHubSearcher", ForbiddenSearcher)
    monkeypatch.setattr(main_module, "download_image", lambda *args: (_ for _ in ()).throw(AssertionError("must not download image")))
    monkeypatch.setattr(main_module, "make_info_card", lambda *args: (_ for _ in ()).throw(AssertionError("must not rebuild image")))
    monkeypatch.setattr(main_module, "generate_copy", lambda *args: {
        "summary": "新的中文用途摘要",
        "highlights": ["新亮点"],
        "use_cases": ["新场景"],
        "xiaohongshu": "新的小红书文案",
        "xiaoheihe": "新的小黑盒文案",
        "generation": "zen",
    })

    result = main_module.run(
        config_path,
        force_refresh=True,
        now=datetime(2026, 8, 14, tzinfo=timezone.utc),
    )

    data = json.loads((result / "data.json").read_text(encoding="utf-8"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert data["projects"][0]["repository"] == old_project["repository"]
    assert data["projects"][0]["image"] == old_project["image"]
    assert data["projects"][0]["copy"]["summary"] == "新的中文用途摘要"
    assert state["node_ids"] == original_ids
    assert (output / "images" / "project.png").read_bytes() == b"existing image"


def test_force_refresh_dry_run_does_not_modify_state(tmp_path, monkeypatch):
    _, config_path = make_config(tmp_path)
    make_period_data(tmp_path)
    state_path = tmp_path / "state" / "published.json"
    state_path.parent.mkdir()
    original = '{"node_ids": ["R_1"], "last_period": "2026-W33"}\n'
    state_path.write_text(original, encoding="utf-8")
    monkeypatch.setattr(main_module, "generate_copy", lambda *args: {
        "summary": "新摘要",
        "highlights": ["亮点"],
        "use_cases": ["场景"],
        "xiaohongshu": "小红书",
        "xiaoheihe": "小黑盒",
        "generation": "zen",
    })

    main_module.run(
        config_path,
        dry_run=True,
        force_refresh=True,
        now=datetime(2026, 8, 14, tzinfo=timezone.utc),
    )

    assert state_path.read_text(encoding="utf-8") == original


def test_force_refresh_rejects_missing_or_invalid_period_data(tmp_path):
    _, config_path = make_config(tmp_path)
    now = datetime(2026, 8, 14, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="找不到本期数据文件"):
        main_module.run(config_path, force_refresh=True, now=now)

    make_period_data(tmp_path, duplicate=True)
    with pytest.raises(ValueError, match="重复"):
        main_module.run(config_path, force_refresh=True, now=now)


def test_parse_args_accepts_force_refresh():
    args = main_module.parse_args(["--config", "config.json", "--force-refresh"])

    assert args.force_refresh is True
    assert args.config.name == "config.json"
