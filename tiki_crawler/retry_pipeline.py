from __future__ import annotations

import asyncio
import time
from pathlib import Path

from tiki_crawler.client import create_client, fetch_product
from tiki_crawler.config import SETTINGS
from tiki_crawler.models import RetrySummary
from tiki_crawler.normalize import transform_product
from tiki_crawler.writer import prepare_retry_dirs, read_json, write_json


def collect_failed_ids(failed_dir: Path) -> list[int]:
    """
    Read all failed batch files, merge them, and remove duplicates while keeping
    the first-seen order.
    """
    seen_ids: set[int] = set()
    merged_failed_ids: list[int] = []

    for file_path in sorted(failed_dir.glob("failed_*.json")):
        failed_payload = read_json(file_path)
        for item in failed_payload:
            if isinstance(item, dict):
                product_id = item.get("product_id")
            else:
                product_id = item

            if not isinstance(product_id, int) or product_id in seen_ids:
                continue

            seen_ids.add(product_id)
            merged_failed_ids.append(product_id)

    return merged_failed_ids


async def run_retry_pipeline(
    output_dir: Path,
    batch_size: int,
    concurrency: int = SETTINGS.retry.concurrency,
    timeout_s: float = SETTINGS.retry.timeout_s,
    max_retries: int = SETTINGS.retry.retries,
) -> RetrySummary:
    """
    Retry failed product IDs with a much smaller concurrency than the main crawl.

    This matches the Coach's "data first" mindset: once the failed set is small,
    the priority changes from speed to correctness and recoverability.
    """
    failed_dir = output_dir / "_failed"
    retry_dir = prepare_retry_dirs(output_dir)
    failed_ids = collect_failed_ids(failed_dir)

    if not failed_ids:
        summary = RetrySummary(
            total_failed_ids=0,
            retried_ids=0,
            recovered_count=0,
            still_failed_count=0,
            elapsed_s=0.0,
            concurrency=concurrency,
        )
        write_json(retry_dir / SETTINGS.reports.retry_summary, summary.to_dict())
        write_json(retry_dir / SETTINGS.reports.retry_failed, [])
        return summary

    started = time.perf_counter()
    recovered_products: list[dict] = []
    still_failed: list[dict] = []
    error_breakdown: dict[str, int] = {}

    async with create_client() as client:
        semaphore = asyncio.Semaphore(concurrency)
        results = await asyncio.gather(
            *[
                fetch_product(
                    product_id=product_id,
                    client=client,
                    semaphore=semaphore,
                    timeout_s=timeout_s,
                    max_retries=max_retries,
                )
                for product_id in failed_ids
            ]
        )

    for result in results:
        if result.ok and result.payload:
            recovered_products.append(transform_product(result.payload))
            continue

        error_name = result.error or "unknown_error"
        error_breakdown[error_name] = error_breakdown.get(error_name, 0) + 1
        still_failed.append(
            {
                "product_id": result.product_id,
                "status_code": result.status_code,
                "error": error_name,
            }
        )

    for index in range(0, len(recovered_products), batch_size):
        payload = recovered_products[index : index + batch_size]
        file_number = (index // batch_size) + 1
        write_json(retry_dir / f"recovered_{file_number:05d}.json", payload)

    elapsed_s = time.perf_counter() - started
    summary = RetrySummary(
        total_failed_ids=len(failed_ids),
        retried_ids=len(failed_ids),
        recovered_count=len(recovered_products),
        still_failed_count=len(still_failed),
        elapsed_s=round(elapsed_s, 2),
        concurrency=concurrency,
        error_breakdown=error_breakdown,
    )
    write_json(retry_dir / SETTINGS.reports.retry_summary, summary.to_dict())
    write_json(retry_dir / SETTINGS.reports.retry_failed, still_failed)
    return summary
