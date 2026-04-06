from __future__ import annotations

from pathlib import Path

from tiki_crawler.models import OutputValidationReport
from tiki_crawler.writer import read_json


def validate_output_directory(output_dir: Path) -> OutputValidationReport:
    """
    Validate the generated dataset after the crawl finishes.

    The goal is not to prove perfect correctness, but to catch the most common
    pipeline mistakes: duplicate output IDs, missing fields, or suspiciously
    empty normalized content.
    """
    product_files = sorted(output_dir.glob("products_*.json"))
    retry_files = sorted((output_dir / "retry").glob("recovered_*.json")) if (output_dir / "retry").exists() else []
    files_to_check = product_files + retry_files
    seen_ids: set[int] = set()
    duplicate_samples: list[int] = []

    report = OutputValidationReport(
        checked_files=len(files_to_check),
        checked_records=0,
        duplicate_output_ids=0,
    )

    required_fields = ("id", "name", "url_key", "price", "description", "images")

    for file_path in files_to_check:
        products = read_json(file_path)
        for product in products:
            report.checked_records += 1

            if any(field not in product for field in required_fields):
                report.missing_required_field_count += 1

            product_id = product.get("id")
            if isinstance(product_id, int):
                if product_id in seen_ids:
                    report.duplicate_output_ids += 1
                    if len(duplicate_samples) < 10:
                        duplicate_samples.append(product_id)
                else:
                    seen_ids.add(product_id)

            if not str(product.get("description") or "").strip():
                report.empty_description_count += 1

            images = product.get("images")
            if not isinstance(images, list) or len(images) == 0:
                report.empty_images_count += 1

    report.duplicate_output_id_samples = duplicate_samples
    return report
