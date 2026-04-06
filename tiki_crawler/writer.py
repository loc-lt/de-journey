from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def chunked(items: list[int], size: int) -> Iterable[list[int]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def prepare_output_dirs(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    failed_dir = output_dir / "_failed"
    failed_dir.mkdir(parents=True, exist_ok=True)
    return failed_dir


def prepare_retry_dirs(output_dir: Path) -> Path:
    retry_dir = output_dir / "retry"
    retry_dir.mkdir(parents=True, exist_ok=True)
    return retry_dir


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
