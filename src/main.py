from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from .config import load_config
from .github_search import GitHubSearcher
from .images import download_image, extract_readme_image, image_filename, make_info_card
from .reports import write_outputs
from .zen import generate_copy


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"node_ids": [], "issues": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_readme(repo: dict[str, Any], token: str | None, timeout: int) -> str:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ai-skill-weekly/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(repo["url"] + "/readme", headers=headers, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        return base64.b64decode(payload.get("content", "")).decode("utf-8", errors="replace")
    except (requests.RequestException, ValueError, KeyError):
        return ""


def load_period_projects(path: Path, period: str) -> tuple[int, list[dict[str, Any]]]:
    if not path.exists():
        raise ValueError(f"无法强制刷新：找不到本期数据文件 {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取本期数据文件: {path}") from exc
    if not isinstance(data, dict) or data.get("period") != period or not isinstance(data.get("projects"), list):
        raise ValueError(f"本期数据文件格式不匹配: {path}")
    seen: set[str] = set()
    for item in data["projects"]:
        repository = item.get("repository") if isinstance(item, dict) else None
        node_id = repository.get("node_id") if isinstance(repository, dict) else None
        if not node_id or node_id in seen:
            raise ValueError("本期数据文件包含缺失或重复的项目 node_id")
        if not isinstance(item.get("image"), dict):
            raise ValueError("本期数据文件缺少项目图片信息")
        seen.add(node_id)
    window_days = data.get("window_days")
    if not isinstance(window_days, int) or window_days <= 0:
        raise ValueError("本期数据文件缺少有效的检索窗口")
    return window_days, data["projects"]


def refresh_projects(
    items: list[dict[str, Any]],
    config: dict[str, Any],
    zen_key: str | None,
) -> list[dict[str, Any]]:
    refreshed: list[dict[str, Any]] = []
    for item in items:
        repository = item["repository"]
        refreshed.append({
            "repository": repository,
            "copy": generate_copy(repository, config["zen"], zen_key, config["content"]),
            "image": item["image"],
        })
    return refreshed


def prepare_project(repo: dict[str, Any], output: Path, config: dict[str, Any], token: str | None, zen_key: str | None) -> dict[str, Any]:
    image_config = config["images"]
    readme = fetch_readme(repo, token, config["github"]["request_timeout_seconds"])
    source_url = extract_readme_image(readme, repo, image_config) if readme else None
    source = "README"
    filename = image_filename(repo)
    target = output / "images" / filename
    downloaded = bool(source_url and download_image(source_url, target, image_config))
    if not downloaded:
        source = "GitHub Open Graph"
        source_url = f"https://opengraph.githubassets.com/ai-skill-weekly/{repo['full_name']}"
        downloaded = download_image(source_url, target, image_config)
    if not downloaded:
        source = "本地信息卡"
        source_url = None
        make_info_card(repo, target, image_config)
    return {
        "repository": {
            key: repo.get(key)
            for key in (
                "node_id", "full_name", "html_url", "description", "stargazers_count",
                "language", "created_at", "updated_at", "topics", "license",
            )
        },
        "copy": generate_copy(repo, config["zen"], zen_key, config["content"]),
        "image": {
            "path": f"images/{filename}",
            "source": source,
            "source_url": source_url,
        },
    }


def run(
    config_path: Path,
    dry_run: bool = False,
    force_refresh: bool = False,
    now: datetime | None = None,
) -> Path:
    root = config_path.resolve().parent
    config = load_config(config_path)
    state_path = root / "state" / "published.json"
    state = load_state(state_path)
    token = os.getenv("GITHUB_TOKEN") or None
    zen_key = os.getenv("ZEN_API_KEY") or None
    now = now or datetime.now(timezone.utc)
    year, week, _ = now.isocalendar()
    output = root / "reports" / f"{year}-W{week:02d}"
    if not force_refresh and not dry_run and state.get("last_period") == output.name and (output / "report.md").exists():
        return output

    repos: list[dict[str, Any]] = []
    if force_refresh:
        window_days, existing_projects = load_period_projects(output / "data.json", output.name)
        projects = refresh_projects(existing_projects, config, zen_key)
    else:
        searcher = GitHubSearcher(config["github"], token)
        window_days, repos = searcher.discover(set(state.get("node_ids", [])), now)
        projects = [prepare_project(repo, output, config, token, zen_key) for repo in repos]
    _, output = write_outputs(root, projects, window_days, now)

    if not dry_run:
        state.setdefault("node_ids", [])
        if not force_refresh:
            state["node_ids"] = list(dict.fromkeys(state["node_ids"] + [repo["node_id"] for repo in repos]))
        state["last_period"] = output.name
        state["updated_at"] = now.isoformat()
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 AI 技能周报")
    parser.add_argument("--config", default="config.example.json", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="生成报告但不更新 state，也不进行远程操作")
    parser.add_argument("--force-refresh", action="store_true", help="重新加工本期已有项目并覆盖本期报告")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output = run(args.config, dry_run=args.dry_run, force_refresh=args.force_refresh)
    except (OSError, ValueError, requests.RequestException) as exc:
        print(f"生成失败: {exc}", file=sys.stderr)
        return 1
    print(f"已生成: {output}")
    if args.dry_run:
        print("dry-run：未更新 state，未执行任何远程提交或发布。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
