from __future__ import annotations

from datetime import datetime
from pathlib import Path

from tiki_crawler.models import CheckpointState
from tiki_crawler.writer import read_json, write_json


def load_checkpoint(path: Path) -> CheckpointState:
    if not path.exists():
        return CheckpointState()

    payload = read_json(path)
    return CheckpointState(
        last_completed_batch=payload.get("last_completed_batch", 0),
        completed_batches=payload.get("completed_batches", []),
        processed_ids=payload.get("processed_ids", 0),
        success_count=payload.get("success_count", 0),
        error_count=payload.get("error_count", 0),
        updated_at=payload.get("updated_at"),
    )


def save_checkpoint(path: Path, state: CheckpointState) -> None:
    state.updated_at = datetime.now().isoformat(timespec="seconds")
    write_json(path, state.to_dict())
