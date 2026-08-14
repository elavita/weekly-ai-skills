from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import requests


API_URL = "https://api.github.com/search/repositories"


def parse_github_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_eligible(repo: dict[str, Any], min_stars: int, since: datetime) -> bool:
    try:
        created = parse_github_time(repo["created_at"])
    except (KeyError, TypeError, ValueError):
        return False
    return (
        not repo.get("fork", False)
        and not repo.get("archived", False)
        and not repo.get("private", False)
        and int(repo.get("stargazers_count", 0)) >= min_stars
        and created >= since
    )


def choose_window(
    windows: list[int],
    fetch_for_window: Callable[[int], list[dict[str, Any]]],
    max_projects: int,
) -> tuple[int, list[dict[str, Any]]]:
    """逐级扩大窗口，达到目标数即停止；不足时返回最大窗口结果。"""
    selected: list[dict[str, Any]] = []
    used_window = windows[-1]
    for window in windows:
        used_window = window
        selected = fetch_for_window(window)
        if len(selected) >= max_projects:
            break
    return used_window, selected[:max_projects]


class GitHubSearcher:
    def __init__(self, config: dict[str, Any], token: str | None = None, session: requests.Session | None = None):
        self.config = config
        self.session = session or requests.Session()
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ai-skill-weekly/1.0",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _request(self, params: dict[str, Any]) -> requests.Response:
        response = self.session.get(
            API_URL,
            headers=self.headers,
            params=params,
            timeout=self.config["request_timeout_seconds"],
        )
        if response.status_code in (403, 429):
            reset = response.headers.get("X-RateLimit-Reset")
            if reset:
                wait = max(0, min(60, int(reset) - int(time.time()) + 1))
                if wait:
                    time.sleep(wait)
                response = self.session.get(
                    API_URL,
                    headers=self.headers,
                    params=params,
                    timeout=self.config["request_timeout_seconds"],
                )
        response.raise_for_status()
        return response

    def search_window(self, days: int, published_ids: set[str], now: datetime) -> list[dict[str, Any]]:
        since = now - timedelta(days=days)
        since_date = since.date().isoformat()
        found: dict[str, dict[str, Any]] = {}
        for term in self.config["search_terms"]:
            query = f'"{term}" stars:>={self.config["min_stars"]} created:>={since_date} fork:false archived:false is:public'
            for page in range(1, self.config["max_pages_per_query"] + 1):
                response = self._request({
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": self.config["per_page"],
                    "page": page,
                })
                items = response.json().get("items", [])
                for repo in items:
                    node_id = repo.get("node_id")
                    if node_id and node_id not in published_ids and is_eligible(repo, self.config["min_stars"], since):
                        found[node_id] = repo
                if len(items) < self.config["per_page"]:
                    break
        return sorted(found.values(), key=lambda item: (-int(item["stargazers_count"]), item["full_name"].lower()))

    def discover(self, published_ids: set[str], now: datetime | None = None) -> tuple[int, list[dict[str, Any]]]:
        now = now or datetime.now(timezone.utc)
        return choose_window(
            self.config["windows_days"],
            lambda days: self.search_window(days, published_ids, now),
            self.config["max_projects"],
        )
