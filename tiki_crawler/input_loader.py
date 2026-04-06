from __future__ import annotations

import csv
from pathlib import Path

from tiki_crawler.models import InputValidationReport


def load_and_validate_product_ids(path: Path) -> tuple[list[int], InputValidationReport]:
    """
    Read the course CSV, validate each row, and deduplicate product IDs while
    preserving their first-seen order.
    """
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV input file, got: {path.suffix}")

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV ids-file must include a header row")
        if "id" not in reader.fieldnames:
            raise ValueError("CSV ids-file must contain an 'id' column")

        unique_ids: list[int] = []
        seen_ids: set[int] = set()
        invalid_values: list[str] = []
        duplicate_ids: list[int] = []
        total_rows = 0
        valid_rows = 0
        invalid_rows = 0
        duplicate_rows = 0

        for row in reader:
            total_rows += 1
            raw_value = (row.get("id") or "").strip()
            if not raw_value or not raw_value.isdigit():
                invalid_rows += 1
                if raw_value and len(invalid_values) < 10:
                    invalid_values.append(raw_value)
                continue

            valid_rows += 1
            product_id = int(raw_value)
            if product_id in seen_ids:
                duplicate_rows += 1
                if len(duplicate_ids) < 10:
                    duplicate_ids.append(product_id)
                continue

            seen_ids.add(product_id)
            unique_ids.append(product_id)

    report = InputValidationReport(
        source_file=str(path),
        total_rows=total_rows,
        valid_rows=valid_rows,
        invalid_rows=invalid_rows,
        duplicate_rows=duplicate_rows,
        unique_product_ids=len(unique_ids),
        sample_invalid_values=invalid_values,
        sample_duplicate_ids=duplicate_ids,
    )
    return unique_ids, report
