from __future__ import annotations

import argparse
import asyncio
import time
from datetime import datetime
from pathlib import Path

from tiki_crawler.checkpoint import load_checkpoint, save_checkpoint
from tiki_crawler.client import create_client, fetch_product
from tiki_crawler.config import SETTINGS
from tiki_crawler.input_loader import load_and_validate_product_ids
from tiki_crawler.models import BatchSummary
from tiki_crawler.normalize import transform_product
from tiki_crawler.probe import run_probe
from tiki_crawler.reporter import (
    print_final_report,
    print_input_report,
    print_output_validation,
    print_retry_report,
)
from tiki_crawler.retry_pipeline import run_retry_pipeline
from tiki_crawler.validators import validate_output_directory
from tiki_crawler.writer import chunked, prepare_output_dirs, read_json, write_json


def build_summary(args: argparse.Namespace, total_ids: int, total_batches: int, started_at: str) -> dict:
    return {
        "total_ids": total_ids,
        "batch_size": args.batch_size,
        "concurrency": args.concurrency,
        "timeout": args.timeout,
        "retries": args.retries,
        "started_at": started_at,
        "finished_at": None,
        "total_elapsed_s": 0.0,
        "processed_ids": 0,
        "success_count": 0,
        "error_count": 0,
        "success_rate": 0.0,
        "avg_req_per_sec": 0.0,
        "total_batches": total_batches,
        "completed_batches": 0,
        "skipped_batches": 0,
        "error_breakdown": {},
        "batches": [],
        "retry_summary": None,
        "output_validation_report": None,
    }


def build_failed_records(results: list) -> tuple[list[int], list[dict[str, object]], dict[str, int]]:
    failed_ids: list[int] = []
    failed_records: list[dict[str, object]] = []
    error_breakdown: dict[str, int] = {}

    for item in results:
        if item.ok:
            continue

        error_name = item.error or "unknown_error"
        failed_ids.append(item.product_id)
        failed_records.append(
            {
                "product_id": item.product_id,
                "status_code": item.status_code,
                "error": error_name,
                "elapsed_s": round(item.elapsed_s, 4),
            }
        )
        error_breakdown[error_name] = error_breakdown.get(error_name, 0) + 1

    return failed_ids, failed_records, error_breakdown


def load_existing_batch_summary(batch_idx: int, output_path: Path, failed_path: Path) -> BatchSummary:
    """
    Resume safely by rebuilding summary information from files that already
    exist on disk. This keeps the summary consistent even after interruptions.
    """
    saved_products = read_json(output_path) if output_path.exists() else []
    failed_payload = read_json(failed_path) if failed_path.exists() else []
    error_breakdown: dict[str, int] = {}

    for item in failed_payload:
        if isinstance(item, dict):
            error_name = item.get("error", "unknown_error")
            error_breakdown[error_name] = error_breakdown.get(error_name, 0) + 1

    return BatchSummary(
        batch_index=batch_idx,
        output_file=output_path.name,
        failed_file=failed_path.name,
        requested=len(saved_products) + len(failed_payload),
        saved=len(saved_products),
        failed=len(failed_payload),
        elapsed_s=0.0,
        req_per_sec=0.0,
        error_breakdown=error_breakdown,
    )


def update_summary_from_batch(summary: dict, batch_summary: BatchSummary, skipped: bool = False) -> None:
    summary["batches"].append(batch_summary.to_dict())
    summary["processed_ids"] += batch_summary.requested
    summary["success_count"] += batch_summary.saved
    summary["error_count"] += batch_summary.failed
    summary["completed_batches"] += 1
    if skipped:
        summary["skipped_batches"] += 1
    for error_name, count in batch_summary.error_breakdown.items():
        summary["error_breakdown"][error_name] = summary["error_breakdown"].get(error_name, 0) + count


def finalize_summary_metrics(summary: dict, total_elapsed: float) -> None:
    summary["finished_at"] = datetime.now().isoformat(timespec="seconds")
    summary["total_elapsed_s"] = round(total_elapsed, 2)
    summary["success_rate"] = (
        round(summary["success_count"] / summary["processed_ids"], 4) if summary["processed_ids"] else 0.0
    )
    summary["avg_req_per_sec"] = (
        round(summary["success_count"] / total_elapsed, 2) if total_elapsed else 0.0
    )


async def run_crawl(args: argparse.Namespace) -> None:
    # Stage 1: trust the input only after validating and deduplicating it.
    ids, input_report = load_and_validate_product_ids(Path(args.ids_file))
    if not ids:
        raise ValueError("No product ids found in ids-file")

    started_at = datetime.now().isoformat(timespec="seconds")
    crawl_started = time.perf_counter()
    output_dir = Path(args.output_dir)
    failed_dir = prepare_output_dirs(output_dir)
    input_report_path = output_dir / SETTINGS.reports.input_validation
    checkpoint_path = output_dir / SETTINGS.reports.checkpoint
    total_batches = (len(ids) + args.batch_size - 1) // args.batch_size
    summary = build_summary(args, len(ids), total_batches, started_at)
    checkpoint_state = load_checkpoint(checkpoint_path)

    write_json(input_report_path, input_report.to_dict())
    print_input_report(input_report)

    # Stage 2: main crawl pipeline.
    async with create_client() as client:
        for batch_idx, batch_ids in enumerate(chunked(ids, args.batch_size), start=1):
            output_path = output_dir / f"products_{batch_idx:05d}.json"
            failed_path = failed_dir / f"failed_{batch_idx:05d}.json"

            if output_path.exists() and not args.overwrite:
                # Existing batch files act as a simple resume mechanism.
                print(f"[skip] batch {batch_idx}/{total_batches} already exists: {output_path.name}")
                batch_summary = load_existing_batch_summary(batch_idx, output_path, failed_path)
                update_summary_from_batch(summary, batch_summary, skipped=True)
                continue

            print(f"[start] batch {batch_idx}/{total_batches} | ids={len(batch_ids)}")
            batch_started = time.perf_counter()
            semaphore = asyncio.Semaphore(args.concurrency)
            results = await asyncio.gather(
                *[
                    fetch_product(
                        product_id=product_id,
                        client=client,
                        semaphore=semaphore,
                        timeout_s=args.timeout,
                        max_retries=args.retries,
                    )
                    for product_id in batch_ids
                ]
            )
            batch_elapsed = time.perf_counter() - batch_started

            transformed = [transform_product(item.payload) for item in results if item.ok and item.payload]
            failed_ids, failed_records, error_breakdown = build_failed_records(results)

            write_json(output_path, transformed)
            write_json(failed_path, failed_records)

            batch_summary = BatchSummary(
                batch_index=batch_idx,
                output_file=output_path.name,
                failed_file=failed_path.name,
                requested=len(batch_ids),
                saved=len(transformed),
                failed=len(failed_ids),
                elapsed_s=round(batch_elapsed, 2),
                req_per_sec=round(len(transformed) / batch_elapsed, 2) if batch_elapsed else 0.0,
                error_breakdown=error_breakdown,
            )
            update_summary_from_batch(summary, batch_summary)
            print(batch_summary.to_dict())

            checkpoint_state.last_completed_batch = batch_idx
            if batch_idx not in checkpoint_state.completed_batches:
                checkpoint_state.completed_batches.append(batch_idx)
            checkpoint_state.processed_ids = summary["processed_ids"]
            checkpoint_state.success_count = summary["success_count"]
            checkpoint_state.error_count = summary["error_count"]
            save_checkpoint(checkpoint_path, checkpoint_state)

    # Stage 3: retry failed IDs slowly and carefully to reduce false negatives.
    retry_enabled = SETTINGS.retry.enabled and not args.skip_retry
    if retry_enabled:
        retry_summary = await run_retry_pipeline(
            output_dir=output_dir,
            batch_size=args.batch_size,
            concurrency=args.retry_concurrency,
        )
        summary["retry_summary"] = retry_summary.to_dict()
        summary["success_count"] += retry_summary.recovered_count
        summary["error_count"] = max(0, summary["error_count"] - retry_summary.recovered_count)
        summary["error_breakdown"] = dict(retry_summary.error_breakdown)
        print_retry_report(retry_summary)

    # Stage 4: validate the generated dataset before reporting success.
    output_validation = validate_output_directory(output_dir)
    write_json(output_dir / SETTINGS.reports.output_validation, output_validation.to_dict())
    summary["output_validation_report"] = output_validation.to_dict()
    print_output_validation(output_validation)

    total_elapsed = time.perf_counter() - crawl_started
    finalize_summary_metrics(summary, total_elapsed)
    summary_path = output_dir / "summary.json"
    summary["summary_file"] = str(summary_path)
    write_json(summary_path, summary)
    print(f"[done] wrote summary: {summary_path}")
    print_final_report(summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch crawler for Tiki product details")
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe = subparsers.add_parser("probe", help="Measure reasonable concurrency before full crawl")
    probe.add_argument(
        "--ids-file",
        default=str(SETTINGS.input.file),
        help=f"Path to CSV file containing product ids (default: {SETTINGS.input.file})",
    )
    probe.add_argument("--sample-size", type=int, default=100, help="Number of ids to test")
    probe.add_argument(
        "--candidates",
        type=int,
        nargs="+",
        default=[5, 10, 20, 40, 60],
        help="Concurrency values to benchmark",
    )
    probe.add_argument("--timeout", type=float, default=SETTINGS.crawl.timeout_s, help="Request timeout in seconds")
    probe.add_argument("--retries", type=int, default=SETTINGS.crawl.retries, help="Retry count for transient failures")
    probe.set_defaults(func=run_probe)

    crawl = subparsers.add_parser("crawl", help="Fetch products and write one JSON file per batch")
    crawl.add_argument(
        "--ids-file",
        default=str(SETTINGS.input.file),
        help=f"Path to CSV file containing product ids (default: {SETTINGS.input.file})",
    )
    crawl.add_argument("--output-dir", default=str(SETTINGS.output.directory), help="Directory to write JSON files")
    crawl.add_argument("--batch-size", type=int, default=SETTINGS.crawl.batch_size, help="Products per output file")
    crawl.add_argument("--concurrency", type=int, default=SETTINGS.crawl.concurrency, help="Concurrent requests per batch")
    crawl.add_argument("--timeout", type=float, default=SETTINGS.crawl.timeout_s, help="Request timeout in seconds")
    crawl.add_argument("--retries", type=int, default=SETTINGS.crawl.retries, help="Retry count for transient failures")
    crawl.add_argument(
        "--retry-concurrency",
        type=int,
        default=SETTINGS.retry.concurrency,
        help="Concurrency for the slower retry pipeline",
    )
    crawl.add_argument(
        "--skip-retry",
        action="store_true",
        help="Skip the second-pass retry pipeline",
    )
    crawl.add_argument("--overwrite", action="store_true", help="Overwrite existing batch files")
    crawl.set_defaults(func=run_crawl)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
