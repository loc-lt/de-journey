from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class FetchResult:
    product_id: int
    ok: bool
    status_code: int | None
    elapsed_s: float
    payload: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class InputValidationReport:
    source_file: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    unique_product_ids: int
    sample_invalid_values: list[str] = field(default_factory=list)
    sample_duplicate_ids: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BatchSummary:
    batch_index: int
    output_file: str
    failed_file: str
    requested: int
    saved: int
    failed: int
    elapsed_s: float
    req_per_sec: float
    error_breakdown: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RetrySummary:
    total_failed_ids: int
    retried_ids: int
    recovered_count: int
    still_failed_count: int
    elapsed_s: float
    concurrency: int
    error_breakdown: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OutputValidationReport:
    checked_files: int
    checked_records: int
    duplicate_output_ids: int
    duplicate_output_id_samples: list[int] = field(default_factory=list)
    empty_description_count: int = 0
    empty_images_count: int = 0
    missing_required_field_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CheckpointState:
    last_completed_batch: int = 0
    completed_batches: list[int] = field(default_factory=list)
    processed_ids: int = 0
    success_count: int = 0
    error_count: int = 0
    updated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
