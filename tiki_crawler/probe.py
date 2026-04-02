from __future__ import annotations

import asyncio
import json
import statistics
import time
from pathlib import Path
from typing import Any

from tiki_crawler.client import create_client, fetch_product, load_product_ids


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def recommend_concurrency(results_summary: list[dict[str, Any]]) -> dict[str, Any]:
    if not results_summary:
        return {"recommended_concurrency": 10, "reason": "fallback_default"}

    safe_options = [r for r in results_summary if r["success_rate"] >= 0.98]
    if safe_options:
        best = max(safe_options, key=lambda x: (x["req_per_sec"], -x["p95_latency_s"]))
        return {
            "recommended_concurrency": best["concurrency"],
            "reason": "best_throughput_with_success_rate_at_least_98pct",
            "probe_result": best,
        }

    best = max(results_summary, key=lambda x: (x["success_rate"], x["req_per_sec"]))
    return {
        "recommended_concurrency": best["concurrency"],
        "reason": "highest_success_rate_then_throughput",
        "probe_result": best,
    }


async def run_probe(args: Any) -> None:
    ids = load_product_ids(Path(args.ids_file))
    sample_ids = ids[: args.sample_size]
    if not sample_ids:
        raise ValueError("No product ids found in ids-file")

    print(f"Loaded {len(ids)} ids. Probe sample size: {len(sample_ids)}")
    print(f"Concurrency candidates: {args.candidates}")

    results_summary = []
    async with create_client() as client:
        for concurrency in args.candidates:
            semaphore = asyncio.Semaphore(concurrency)
            started = time.perf_counter()
            results = await asyncio.gather(
                *[
                    fetch_product(
                        product_id=product_id,
                        client=client,
                        semaphore=semaphore,
                        timeout_s=args.timeout,
                        max_retries=args.retries,
                    )
                    for product_id in sample_ids
                ]
            )
            elapsed = time.perf_counter() - started

            successes = [r for r in results if r.ok]
            failures = [r for r in results if not r.ok]
            latencies = [r.elapsed_s for r in successes]
            success_rate = len(successes) / len(results)
            req_per_sec = len(successes) / elapsed if elapsed else 0.0
            avg_latency = statistics.mean(latencies) if latencies else 0.0
            p95_latency = percentile(latencies, 0.95)

            error_counts: dict[str, int] = {}
            for item in failures:
                key = item.error or "unknown_error"
                error_counts[key] = error_counts.get(key, 0) + 1

            probe_result = {
                "concurrency": concurrency,
                "total": len(results),
                "success": len(successes),
                "failed": len(failures),
                "success_rate": round(success_rate, 4),
                "elapsed_s": round(elapsed, 2),
                "req_per_sec": round(req_per_sec, 2),
                "avg_latency_s": round(avg_latency, 3),
                "p95_latency_s": round(p95_latency, 3),
                "errors": error_counts,
            }
            results_summary.append(probe_result)
            print(json.dumps(probe_result, ensure_ascii=False))

    recommended = recommend_concurrency(results_summary)
    print("\nRecommended settings")
    print(json.dumps(recommended, ensure_ascii=False, indent=2))
