from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path("config.example.json")


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    required = ("github", "zen", "content", "images")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"配置缺少字段: {', '.join(missing)}")
    windows = data["github"].get("windows_days", [])
    if not windows or windows != sorted(set(windows)):
        raise ValueError("github.windows_days 必须是递增且不重复的正整数数组")
    if any(not isinstance(day, int) or day <= 0 for day in windows):
        raise ValueError("检索窗口必须是正整数")
    return data
