from __future__ import annotations

import argparse
import asyncio
import time
from datetime import datetime
from pathlib import Path

from tiki_crawler.client import create_client, fetch_product, load_product_ids
from tiki_crawler.normalize import transform_product
from tiki_crawler.probe import run_probe
from tiki_crawler.writer import chunked, prepare_output_dirs, write_json


DEFAULT_IDS_FILE = "data/input/products-0-200000.csv"
DEFAULT_OUTPUT_DIR = "data/output"


def format_duration(total_seconds: float) -> str:
    total_seconds = int(round(total_seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def print_final_report(summary: dict) -> None:
    print("\nFinished crawl")
    print(f"Total IDs: {summary['total_ids']}")
    print(f"Processed IDs: {summary['processed_ids']}")
    print(f"Success: {summary['success_count']}")
    print(f"Errors: {summary['error_count']}")
    print(f"Success rate: {summary['success_rate']:.2%}")
    print(f"Elapsed: {summary['total_elapsed_s']:.2f}s ({format_duration(summary['total_elapsed_s'])})")
    print(f"Average rate: {summary['avg_req_per_sec']:.2f} req/s")
    print(f"Completed batches: {summary['completed_batches']}/{summary['total_batches']}")
    print(f"Skipped batches: {summary['skipped_batches']}")
    if summary["error_breakdown"]:
        print("Error breakdown:")
        for error_name, count in sorted(summary["error_breakdown"].items()):
            print(f"  - {error_name}: {count}")
    print(f"Summary file: {summary['summary_file']}")


async def run_crawl(args: argparse.Namespace) -> None:
    ids = load_product_ids(Path(args.ids_file))
    if not ids:
        raise ValueError("No product ids found in ids-file")

    started_at = datetime.now().isoformat(timespec="seconds")
    crawl_started = time.perf_counter()
    output_dir = Path(args.output_dir)
    failed_dir = prepare_output_dirs(output_dir)
    total_batches = (len(ids) + args.batch_size - 1) // args.batch_size
    summary = {
        "total_ids": len(ids),
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
    }

    async with create_client() as client:
        for batch_idx, batch_ids in enumerate(chunked(ids, args.batch_size), start=1):
            output_path = output_dir / f"products_{batch_idx:05d}.json"
            failed_path = failed_dir / f"failed_{batch_idx:05d}.json"

            if output_path.exists() and not args.overwrite:
                print(f"[skip] batch {batch_idx}/{total_batches} already exists: {output_path.name}")
                summary["skipped_batches"] += 1
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
            failed_ids = [item.product_id for item in results if not item.ok]
            error_breakdown: dict[str, int] = {}
            for item in results:
                if item.ok:
                    continue
                error_name = item.error or "unknown_error"
                error_breakdown[error_name] = error_breakdown.get(error_name, 0) + 1
                summary["error_breakdown"][error_name] = summary["error_breakdown"].get(error_name, 0) + 1

            write_json(output_path, transformed)
            write_json(failed_path, failed_ids)

            batch_summary = {
                "batch_index": batch_idx,
                "output_file": output_path.name,
                "failed_file": failed_path.name,
                "requested": len(batch_ids),
                "saved": len(transformed),
                "failed": len(failed_ids),
                "elapsed_s": round(batch_elapsed, 2),
                "req_per_sec": round(len(transformed) / batch_elapsed, 2) if batch_elapsed else 0.0,
                "error_breakdown": error_breakdown,
            }
            summary["batches"].append(batch_summary)
            summary["processed_ids"] += len(batch_ids)
            summary["success_count"] += len(transformed)
            summary["error_count"] += len(failed_ids)
            summary["completed_batches"] += 1
            print(batch_summary)

    total_elapsed = time.perf_counter() - crawl_started
    summary["finished_at"] = datetime.now().isoformat(timespec="seconds")
    summary["total_elapsed_s"] = round(total_elapsed, 2)
    summary["success_rate"] = (
        round(summary["success_count"] / summary["processed_ids"], 4) if summary["processed_ids"] else 0.0
    )
    summary["avg_req_per_sec"] = (
        round(summary["success_count"] / total_elapsed, 2) if total_elapsed else 0.0
    )
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
        default=DEFAULT_IDS_FILE,
        help=f"Path to CSV file containing product ids (default: {DEFAULT_IDS_FILE})",
    )
    probe.add_argument("--sample-size", type=int, default=100, help="Number of ids to test")
    probe.add_argument(
        "--candidates",
        type=int,
        nargs="+",
        default=[5, 10, 20, 40, 60],
        help="Concurrency values to benchmark",
    )
    probe.add_argument("--timeout", type=float, default=15.0, help="Request timeout in seconds")
    probe.add_argument("--retries", type=int, default=2, help="Retry count for transient failures")
    probe.set_defaults(func=run_probe)

    crawl = subparsers.add_parser("crawl", help="Fetch products and write one JSON file per batch")
    crawl.add_argument(
        "--ids-file",
        default=DEFAULT_IDS_FILE,
        help=f"Path to CSV file containing product ids (default: {DEFAULT_IDS_FILE})",
    )
    crawl.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory to write JSON files")
    crawl.add_argument("--batch-size", type=int, default=1000, help="Products per output file")
    crawl.add_argument("--concurrency", type=int, default=20, help="Concurrent requests per batch")
    crawl.add_argument("--timeout", type=float, default=15.0, help="Request timeout in seconds")
    crawl.add_argument("--retries", type=int, default=2, help="Retry count for transient failures")
    crawl.add_argument("--overwrite", action="store_true", help="Overwrite existing batch files")
    crawl.set_defaults(func=run_crawl)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
