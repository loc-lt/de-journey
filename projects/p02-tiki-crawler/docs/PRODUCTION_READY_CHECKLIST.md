# Production-Ready Checklist For This Project

## 1. Input Stage

- [ ] The input file is a CSV with a valid header row.
- [ ] The `id` column exists.
- [ ] Invalid rows are counted and reported.
- [ ] Duplicate input IDs are removed.
- [ ] The number of unique IDs is reported before crawling starts.
- [ ] Input validation output is written to `data/output/input_validation_report.json`.

## 2. Main Crawl Stage

- [ ] The crawler uses one shared HTTP client.
- [ ] Request headers are set to reduce the chance of `403`.
- [ ] Each request has its own retry logic.
- [ ] Transient errors such as `429` and `5xx` are retried.
- [ ] Concurrency is limited by a semaphore.
- [ ] Data is processed batch by batch.
- [ ] Each batch is written to disk immediately.
- [ ] Failed records are written to `_failed/` with error details.

## 3. Memory Safety

- [ ] The program does not keep all `200000` product details in RAM.
- [ ] Only one batch is held in memory at a time.
- [ ] Output is flushed to disk before the next batch starts.

## 4. Resume / Checkpoint

- [ ] The crawler stores checkpoint information after each completed batch.
- [ ] If the program stops unexpectedly, rerun should skip completed batches safely.
- [ ] Restarting the job should not require crawling from the beginning.
- [ ] The crawl runner can auto-restart after an unexpected crash and continue from existing outputs.

## 5. Retry Pipeline

- [ ] Failed IDs are collected into a second-pass retry pipeline.
- [ ] Failed IDs are rechecked sequentially, one by one.
- [ ] Retry summary is written to `data/output/retry/retry_summary.json`.
- [ ] IDs that still fail after retry are stored separately.

## 6. Output Validation

- [ ] Output files are checked for duplicate product IDs.
- [ ] Missing required fields are counted.
- [ ] Empty descriptions are counted.
- [ ] Empty image lists are counted.
- [ ] Validation results are written to `data/output/output_validation_report.json`.

## 7. Reporting

- [ ] Final summary includes total IDs, success count, error count, and success rate.
- [ ] Final summary includes total elapsed time and average request rate.
- [ ] Final summary includes error breakdown.
- [ ] Final summary includes retry pipeline results.

## 8. Testing

- [ ] Unit tests exist for input validation.
- [ ] Unit tests exist for description normalization.
- [ ] Unit tests exist for duplicate detection.
- [ ] Unit tests exist for checkpoint load/save behavior.

## 9. Engineering Quality

- [ ] Code is split by responsibility.
- [ ] Important functions use type hints.
- [ ] Core pipeline stages are documented.
- [ ] Logs and reports help explain what happened during the crawl.

## 10. Minimum Acceptance For A Trustworthy Submission

At a minimum, the project should be able to prove:

- the input was validated
- duplicates were checked
- failed IDs were retried
- output was validated
- the final numbers in the report are explainable

If these conditions are not met, the result may still be a working crawler, but it is not yet trustworthy as a production-style data pipeline.
