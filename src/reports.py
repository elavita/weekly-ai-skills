from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DISCLAIMER = "本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。"


def period_id(now: datetime) -> str:
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"


def _age_label(created_at: str, now: datetime) -> str:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    days = max(0, (now - created).days)
    return "本周新增" if days <= 7 else f"近 {days} 天创建"


def build_report(period: str, projects: list[dict[str, Any]], window_days: int, now: datetime) -> str:
    lines = [f"# AI 技能周报 {period}", "", f"检索窗口：近 {window_days} 天。精选 {len(projects)} 个未发布项目。", ""]
    if not projects:
        lines.extend(["本期在配置的窗口和历史去重条件下没有找到合适的新项目。", ""])
    for index, item in enumerate(projects, 1):
        repo, copy = item["repository"], item["copy"]
        lines.extend([
            f"## {index}. [{repo['full_name']}]({repo['html_url']})",
            "",
            f"![{repo['full_name']}]({item['image']['path']})",
            "",
            f"**{_age_label(repo['created_at'], now)}** · {repo.get('stargazers_count', 0):,} Stars · {repo.get('language') or '语言未标注'}",
            "",
            copy["summary"],
            "",
            "亮点：",
        ])
        lines.extend(f"- {value}" for value in copy["highlights"])
        lines.extend(["", "适用场景："])
        lines.extend(f"- {value}" for value in copy["use_cases"])
        lines.extend(["", f"图片来源：{item['image']['source']} ({item['image'].get('source_url') or '本地生成'})", ""])
    lines.extend(["---", "", DISCLAIMER, ""])
    return "\n".join(lines)


def build_social(title: str, projects: list[dict[str, Any]], field: str, period: str) -> str:
    lines = [f"# {title} {period}", ""]
    for item in projects:
        lines.extend([f"## {item['repository']['full_name']}", "", item["copy"][field], ""])
    lines.extend([DISCLAIMER, ""])
    return "\n".join(lines)


def write_outputs(
    root: Path,
    projects: list[dict[str, Any]],
    window_days: int,
    now: datetime | None = None,
) -> tuple[str, Path]:
    now = now or datetime.now(timezone.utc)
    period = period_id(now)
    output = root / "reports" / period
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.md").write_text(build_report(period, projects, window_days, now), encoding="utf-8")
    (output / "xiaohongshu.md").write_text(build_social("小红书文案", projects, "xiaohongshu", period), encoding="utf-8")
    (output / "xiaoheihe.md").write_text(build_social("小黑盒文案", projects, "xiaoheihe", period), encoding="utf-8")
    data = {
        "period": period,
        "generated_at": now.isoformat(),
        "window_days": window_days,
        "projects": projects,
    }
    (output / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files = ["report.md", "data.json", "xiaohongshu.md", "xiaoheihe.md"]
    manifest = {
        "period": period,
        "generated_at": now.isoformat(),
        "project_count": len(projects),
        "files": files,
        "images": [item["image"] for item in projects],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return period, output
