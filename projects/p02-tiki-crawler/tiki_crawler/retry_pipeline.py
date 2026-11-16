from __future__ import annotations

import time
from pathlib import Path

from tiki_crawler.client import create_sync_client, fetch_product_sync
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


def recheck_failed_ids_once(
    failed_ids: list[int],
    timeout_s: float,
    max_retries: int,
) -> list:
    """
    Re-run one screening round on the current failed IDs.

    This round is intentionally sequential. We inspect one failed ID at a time
    so the retry stage prioritizes correctness over speed.
    """
    results = []
    with create_sync_client() as client:
        for product_id in failed_ids:
            results.append(
                fetch_product_sync(
                    product_id=product_id,
                    client=client,
                    timeout_s=timeout_s,
                    max_retries=max_retries,
                )
            )
    return results


def classify_failed_attempts(
    attempt_history: dict[int, list[dict[str, int | str | None]]],
) -> tuple[list[dict], list[dict], dict[str, int]]:
    """
    Split unresolved IDs into:
    - confirmed_404: every round consistently returned http_404
    - unstable: errors changed across rounds, so the ID deserves extra review
    """
    confirmed_404: list[dict] = []
    unstable: list[dict] = []
    error_breakdown: dict[str, int] = {}

    for product_id, attempts in attempt_history.items():
        error_names = [str(item.get("error") or "unknown_error") for item in attempts]
        final_status_code = attempts[-1].get("status_code")
        final_error = error_names[-1]
        final_record = {
            "product_id": product_id,
            "status_code": final_status_code,
            "error": final_error,
            "attempts": attempts,
        }

        error_breakdown[final_error] = error_breakdown.get(final_error, 0) + 1
        if error_names and all(error_name == "http_404" for error_name in error_names):
            confirmed_404.append(final_record)
        else:
            unstable.append(final_record)

    return confirmed_404, unstable, error_breakdown


def run_retry_pipeline(
    output_dir: Path,
    batch_size: int,
    timeout_s: float = SETTINGS.retry.timeout_s,
    max_retries: int = SETTINGS.retry.retries,
) -> RetrySummary:
    """
    Retry failed product IDs sequentially after the main crawl finishes.

    This matches the Coach's guidance: once the failed set is small, stop using
    async/full-speed execution and recheck each ID slowly to prove whether the
    failures are real.
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
            confirmed_404_count=0,
            unstable_count=0,
            rounds_run=0,
        )
        write_json(retry_dir / SETTINGS.reports.retry_summary, summary.to_dict())
        write_json(retry_dir / SETTINGS.reports.retry_failed, [])
        write_json(retry_dir / "confirmed_404.json", [])
        write_json(retry_dir / "still_unstable.json", [])
        return summary

    started = time.perf_counter()
    recovered_products: list[dict] = []
    attempt_history: dict[int, list[dict[str, int | str | None]]] = {product_id: [] for product_id in failed_ids}
    remaining_failed_ids = list(failed_ids)
    rounds_run = 0

    for round_index in range(1, SETTINGS.retry.recheck_rounds + 1):
        if not remaining_failed_ids:
            break

        rounds_run = round_index
        results = recheck_failed_ids_once(
            failed_ids=remaining_failed_ids,
            timeout_s=timeout_s,
            max_retries=max_retries,
        )

        next_remaining_failed_ids: list[int] = []
        round_report = {
            "round": round_index,
            "requested": len(remaining_failed_ids),
            "recovered": 0,
            "still_failed": 0,
            "error_breakdown": {},
        }

        for result in results:
            if result.ok and result.payload:
                recovered_products.append(transform_product(result.payload))
                round_report["recovered"] += 1
                continue

            error_name = result.error or "unknown_error"
            attempt_history[result.product_id].append(
                {
                    "round": round_index,
                    "status_code": result.status_code,
                    "error": error_name,
                    "elapsed_s": round(result.elapsed_s, 4),
                }
            )
            round_report["still_failed"] += 1
            round_report["error_breakdown"][error_name] = round_report["error_breakdown"].get(error_name, 0) + 1
            next_remaining_failed_ids.append(result.product_id)

        write_json(retry_dir / f"round_{round_index:02d}_report.json", round_report)
        remaining_failed_ids = next_remaining_failed_ids

        if remaining_failed_ids and round_index < SETTINGS.retry.recheck_rounds:
            time.sleep(SETTINGS.retry.round_delay_s)

    unresolved_history = {
        product_id: attempts
        for product_id, attempts in attempt_history.items()
        if attempts
    }
    confirmed_404, unstable, error_breakdown = classify_failed_attempts(unresolved_history)
    still_failed = confirmed_404 + unstable

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
        confirmed_404_count=len(confirmed_404),
        unstable_count=len(unstable),
        rounds_run=rounds_run,
        error_breakdown=error_breakdown,
    )
    write_json(retry_dir / SETTINGS.reports.retry_summary, summary.to_dict())
    write_json(retry_dir / SETTINGS.reports.retry_failed, still_failed)
    write_json(retry_dir / "confirmed_404.json", confirmed_404)
    write_json(retry_dir / "still_unstable.json", unstable)
    return summary
