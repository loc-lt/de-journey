from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_FILE = PROJECT_ROOT / "settings.yaml"


@dataclass(frozen=True)
class InputSettings:
    file: Path


@dataclass(frozen=True)
class OutputSettings:
    directory: Path


@dataclass(frozen=True)
class CrawlSettings:
    batch_size: int
    concurrency: int
    timeout_s: float
    retries: int


@dataclass(frozen=True)
class RetrySettings:
    enabled: bool
    timeout_s: float
    retries: int
    recheck_rounds: int
    round_delay_s: float


@dataclass(frozen=True)
class ReportSettings:
    input_validation: str
    output_validation: str
    checkpoint: str
    retry_summary: str
    retry_failed: str


@dataclass(frozen=True)
class AppSettings:
    input: InputSettings
    output: OutputSettings
    crawl: CrawlSettings
    retry: RetrySettings
    reports: ReportSettings


def _read_settings_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Settings file not found: {path}")

    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("settings.yaml must contain a top-level mapping")
    return payload


def load_settings(path: Path = SETTINGS_FILE) -> AppSettings:
    """
    Load the crawler configuration from a YAML file and map it into typed
    settings objects so the rest of the code can access config safely.
    """
    payload = _read_settings_file(path)

    input_payload = payload.get("input", {})
    output_payload = payload.get("output", {})
    crawl_payload = payload.get("crawl", {})
    retry_payload = payload.get("retry", {})
    reports_payload = payload.get("reports", {})

    return AppSettings(
        input=InputSettings(file=Path(input_payload["file"])),
        output=OutputSettings(directory=Path(output_payload["directory"])),
        crawl=CrawlSettings(
            batch_size=int(crawl_payload["batch_size"]),
            concurrency=int(crawl_payload["concurrency"]),
            timeout_s=float(crawl_payload["timeout_s"]),
            retries=int(crawl_payload["retries"]),
        ),
        retry=RetrySettings(
            enabled=bool(retry_payload["enabled"]),
            timeout_s=float(retry_payload["timeout_s"]),
            retries=int(retry_payload["retries"]),
            recheck_rounds=int(retry_payload["recheck_rounds"]),
            round_delay_s=float(retry_payload["round_delay_s"]),
        ),
        reports=ReportSettings(
            input_validation=str(reports_payload["input_validation"]),
            output_validation=str(reports_payload["output_validation"]),
            checkpoint=str(reports_payload["checkpoint"]),
            retry_summary=str(reports_payload["retry_summary"]),
            retry_failed=str(reports_payload["retry_failed"]),
        ),
    )


SETTINGS = load_settings()
