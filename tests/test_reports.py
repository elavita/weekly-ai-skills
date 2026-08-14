from __future__ import annotations

import json
from datetime import datetime, timezone

from src.reports import write_outputs


def test_writes_all_report_artifacts(tmp_path):
    now = datetime(2026, 8, 14, 1, 17, tzinfo=timezone.utc)
    projects = [{
        "repository": {
            "node_id": "R_1",
            "full_name": "owner/project",
            "html_url": "https://github.com/owner/project",
            "description": "AI agent",
            "stargazers_count": 800,
            "language": "Python",
            "created_at": "2026-08-01T00:00:00Z",
        },
        "copy": {
            "summary": "项目摘要",
            "highlights": ["亮点"],
            "use_cases": ["场景"],
            "xiaohongshu": "小红书正文",
            "xiaoheihe": "小黑盒正文",
            "generation": "fallback",
        },
        "image": {
            "path": "images/project.png",
            "source": "本地信息卡",
            "source_url": None,
        },
    }]

    period, output = write_outputs(tmp_path, projects, 30, now)

    assert period == "2026-W33"
    expected = {"report.md", "data.json", "xiaohongshu.md", "xiaoheihe.md", "manifest.json"}
    assert expected.issubset({path.name for path in output.iterdir()})
    assert "近 13 天创建" in (output / "report.md").read_text(encoding="utf-8")
    data = json.loads((output / "data.json").read_text(encoding="utf-8"))
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert data["projects"][0]["repository"]["node_id"] == "R_1"
    assert manifest["project_count"] == 1
    assert manifest["images"][0]["source"] == "本地信息卡"
