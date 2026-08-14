from __future__ import annotations

import hashlib
import io
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from PIL import Image, ImageDraw, ImageFont


MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((?:<)?([^\s)>]+)(?:>)?(?:\s+[\"'][^\"']*[\"'])?\)", re.I)
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*?src=[\"']([^\"']+)[\"'][^>]*?(?:alt=[\"']([^\"']*)[\"'])?[^>]*>", re.I)


def safe_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"https", "http"} and bool(parsed.netloc) and not parsed.username and not parsed.password


def resolve_readme_url(url: str, repo: dict[str, Any]) -> str | None:
    if url.startswith("data:") or url.startswith("javascript:"):
        return None
    if url.startswith("//"):
        return "https:" + url
    if safe_http_url(url):
        return url
    owner_repo = repo["full_name"]
    branch = repo.get("default_branch", "main")
    base = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/"
    return urljoin(base, url.lstrip("./"))


def extract_readme_image(readme: str, repo: dict[str, Any], config: dict[str, Any]) -> str | None:
    candidates: list[tuple[int, str]] = []
    for alt, url in MARKDOWN_IMAGE_RE.findall(readme):
        candidates.append((_image_score(alt, url, config), url))
    for url, alt in HTML_IMAGE_RE.findall(readme):
        candidates.append((_image_score(alt, url, config), url))
    for score, url in sorted(candidates, key=lambda item: item[0], reverse=True):
        lowered = url.lower()
        if score > 0 and not any(marker.lower() in lowered for marker in config["badge_markers"]):
            resolved = resolve_readme_url(url, repo)
            if resolved and safe_http_url(resolved):
                return resolved
    return None


def _image_score(alt: str, url: str, config: dict[str, Any]) -> int:
    text = f"{alt} {url}".lower()
    if any(marker.lower() in text for marker in config["badge_markers"]):
        return -100
    return sum(10 for keyword in config["readme_keywords"] if keyword.lower() in text)


def download_image(url: str, target: Path, config: dict[str, Any], session: requests.Session | None = None) -> bool:
    if not safe_http_url(url):
        return False
    session = session or requests.Session()
    try:
        response = session.get(
            url,
            timeout=config["timeout_seconds"],
            stream=True,
            allow_redirects=True,
            headers={"User-Agent": "ai-skill-weekly/1.0"},
        )
        response.raise_for_status()
        if not safe_http_url(response.url):
            return False
        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if content_type not in config["allowed_content_types"]:
            return False
        declared = int(response.headers.get("Content-Length", 0) or 0)
        if declared > config["max_bytes"]:
            return False
        chunks: list[bytes] = []
        size = 0
        for chunk in response.iter_content(65536):
            size += len(chunk)
            if size > config["max_bytes"]:
                return False
            chunks.append(chunk)
        raw = b"".join(chunks)
        with Image.open(io.BytesIO(raw)) as image:
            image.verify()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return True
    except (requests.RequestException, OSError, ValueError):
        return False


def make_info_card(repo: dict[str, Any], target: Path, config: dict[str, Any]) -> None:
    width, height = config["width"], config["height"]
    image = Image.new("RGB", (width, height), "#f4f7f9")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.rectangle((0, 0, 22, height), fill="#167d6d")
    draw.text((70, 70), "AI SKILL WEEKLY", fill="#167d6d", font=font)
    draw.text((70, 170), repo["full_name"], fill="#17212b", font=font)
    description = (repo.get("description") or "No description")[:120]
    draw.text((70, 240), description, fill="#44515c", font=font)
    draw.text((70, 390), f"Stars: {repo.get('stargazers_count', 0):,}", fill="#17212b", font=font)
    draw.text((70, 450), f"Created: {repo.get('created_at', '')[:10]}", fill="#17212b", font=font)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, "PNG")


def image_filename(repo: dict[str, Any], extension: str = ".png") -> str:
    digest = hashlib.sha256(repo["node_id"].encode("utf-8")).hexdigest()[:10]
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", repo["full_name"])
    return f"{slug}-{digest}{extension}"
