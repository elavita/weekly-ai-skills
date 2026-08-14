from __future__ import annotations

from datetime import datetime, timezone

from src.images import extract_readme_image, resolve_readme_url


IMAGE_CONFIG = {
    "readme_keywords": ["screenshot", "demo", "preview", "showcase"],
    "badge_markers": ["shields.io", "badge", "badgen.net"],
}
REPO = {"full_name": "owner/project", "default_branch": "main"}


def test_readme_prefers_effect_image_and_filters_badge():
    readme = """
    ![build badge](https://img.shields.io/build.svg)
    ![demo screenshot](docs/demo.png)
    """

    assert extract_readme_image(readme, REPO, IMAGE_CONFIG) == (
        "https://raw.githubusercontent.com/owner/project/main/docs/demo.png"
    )


def test_readme_html_image_and_absolute_url():
    readme = '<img src="https://example.com/showcase.webp" alt="showcase">'
    assert extract_readme_image(readme, REPO, IMAGE_CONFIG) == "https://example.com/showcase.webp"


def test_unsafe_readme_urls_are_rejected():
    assert resolve_readme_url("javascript:alert(1)", REPO) is None
    assert resolve_readme_url("data:image/png;base64,AAAA", REPO) is None
