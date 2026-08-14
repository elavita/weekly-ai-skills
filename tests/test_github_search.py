from datetime import datetime, timezone

from src.github_search import GitHubSearcher, choose_window, is_eligible


NOW = datetime(2026, 8, 14, tzinfo=timezone.utc)


def repo(**overrides):
    value = {
        "node_id": "R_1",
        "full_name": "owner/project",
        "created_at": "2026-08-10T00:00:00Z",
        "stargazers_count": 800,
        "fork": False,
        "archived": False,
        "private": False,
    }
    value.update(overrides)
    return value


def test_window_expands_until_enough_projects():
    calls = []

    def fetch(days):
        calls.append(days)
        return [repo(node_id=f"R_{index}") for index in range({7: 1, 30: 3, 90: 6}[days])]

    window, projects = choose_window([7, 30, 90], fetch, 5)

    assert window == 90
    assert len(projects) == 5
    assert calls == [7, 30, 90]


def test_star_fork_archive_private_and_exact_created_at_filters():
    since = datetime(2026, 8, 7, 12, tzinfo=timezone.utc)
    assert is_eligible(repo(created_at="2026-08-07T12:00:00Z"), 500, since)
    assert not is_eligible(repo(created_at="2026-08-07T11:59:59Z"), 500, since)
    assert not is_eligible(repo(stargazers_count=499), 500, since)
    assert not is_eligible(repo(fork=True), 500, since)
    assert not is_eligible(repo(archived=True), 500, since)
    assert not is_eligible(repo(private=True), 500, since)


class FakeResponse:
    status_code = 200
    headers = {}

    def __init__(self, items):
        self.items = items

    def raise_for_status(self):
        return None

    def json(self):
        return {"items": self.items}


class FakeSession:
    def __init__(self, items):
        self.items = items
        self.calls = []

    def get(self, *args, **kwargs):
        self.calls.append(kwargs["params"])
        return FakeResponse(self.items)


def test_history_and_cross_query_duplicates_are_removed():
    items = [repo(node_id="OLD"), repo(node_id="NEW", full_name="owner/new")]
    config = {
        "search_terms": ["AI skill", "MCP"],
        "min_stars": 500,
        "per_page": 100,
        "max_pages_per_query": 2,
        "request_timeout_seconds": 10,
    }
    searcher = GitHubSearcher(config, session=FakeSession(items))

    projects = searcher.search_window(7, {"OLD"}, NOW)

    assert [project["node_id"] for project in projects] == ["NEW"]
    assert len(searcher.session.calls) == 2
    assert all("fork:false archived:false is:public" in call["q"] for call in searcher.session.calls)
