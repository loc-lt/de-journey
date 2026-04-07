from __future__ import annotations

from tiki_crawler.models import InputValidationReport, OutputValidationReport, RetrySummary


def format_duration(total_seconds: float) -> str:
    total_seconds = int(round(total_seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def print_input_report(report: InputValidationReport) -> None:
    print("Input validation")
    print(f"  Source file: {report.source_file}")
    print(f"  Total rows: {report.total_rows}")
    print(f"  Valid rows: {report.valid_rows}")
    print(f"  Invalid rows: {report.invalid_rows}")
    print(f"  Duplicate rows: {report.duplicate_rows}")
    print(f"  Unique product IDs: {report.unique_product_ids}")
    if report.sample_invalid_values:
        print(f"  Sample invalid values: {report.sample_invalid_values}")
    if report.sample_duplicate_ids:
        print(f"  Sample duplicate IDs: {report.sample_duplicate_ids}")


def print_retry_report(summary: RetrySummary) -> None:
    print("\nRetry pipeline")
    print(f"  Failed IDs from main crawl: {summary.total_failed_ids}")
    print(f"  Retried IDs: {summary.retried_ids}")
    print(f"  Recovered IDs: {summary.recovered_count}")
    print(f"  Confirmed 404 IDs: {summary.confirmed_404_count}")
    print(f"  Still unstable IDs: {summary.unstable_count}")
    print(f"  Still failed total: {summary.still_failed_count}")
    print(f"  Recheck rounds: {summary.rounds_run}")
    print(f"  Retry elapsed: {summary.elapsed_s:.2f}s ({format_duration(summary.elapsed_s)})")
    if summary.error_breakdown:
        print("  Retry error breakdown:")
        for error_name, count in sorted(summary.error_breakdown.items()):
            print(f"    - {error_name}: {count}")


def print_output_validation(report: OutputValidationReport) -> None:
    print("\nOutput validation")
    print(f"  Checked files: {report.checked_files}")
    print(f"  Checked records: {report.checked_records}")
    print(f"  Duplicate output IDs: {report.duplicate_output_ids}")
    print(f"  Empty descriptions: {report.empty_description_count}")
    print(f"  Empty images: {report.empty_images_count}")
    print(f"  Missing required fields: {report.missing_required_field_count}")
    if report.duplicate_output_id_samples:
        print(f"  Duplicate output ID samples: {report.duplicate_output_id_samples}")


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
