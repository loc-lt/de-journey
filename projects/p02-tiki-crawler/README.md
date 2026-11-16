# Tiki Product Crawler

This project downloads product details from Tiki in batches and stores the results as JSON files.

## Project Structure

```text
project02/
  data/
    input/
      products-0-200000.csv
    output/
      input_validation_report.json
      checkpoint.json
      output_validation_report.json
      retry/
  requirements.txt
  README.md
  settings.yaml
  MEETING_NOTES_VI.md
  PIPELINE_GUIDE_VI.md
  PRODUCTION_READY_CHECKLIST.md
  product_sample.json
  tiki_crawler/
    __init__.py
    checkpoint.py
    cli.py
    config.py
    client.py
    input_loader.py
    normalize.py
    reporter.py
    retry_pipeline.py
    writer.py
    models.py
    probe.py
    validators.py
```

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The crawler reads its default runtime configuration from:

```text
settings.yaml
```

This file is used for:

- input and output paths
- crawl batch size
- crawl concurrency
- timeout and retry values
- retry pipeline settings
- auto-restart runner settings
- report file names

If `.venv` already exists, just reinstall the dependencies after pulling new changes:

```bash
pip install -r requirements.txt
```

## Input File

The crawler currently reads product IDs from a CSV file only.

Requirements:
- the file must be a `.csv`
- it must contain a header row
- the current implementation reads the `id` column

Default input file:

```text
data/input/products-0-200000.csv
```

## Probe Before Crawling

`batch_size` controls how many products are written to each output file.  
For this assignment, `1000` is a reasonable default because the expected output is about 1000 products per file.

`concurrency` controls how many HTTP requests are sent in parallel.  
Run `probe` first to measure a reasonable value:

```bash
python3 -m tiki_crawler.cli probe
```

By default, the probe tests these concurrency levels:

- `5`
- `10`
- `20`
- `40`
- `60`

It prints metrics such as:

- `success_rate`
- `req_per_sec`
- `avg_latency_s`
- `p95_latency_s`
- error counts such as `http_404`, `http_429`, timeouts, or `5xx`
- duplicate/invalid row counts from the input CSV

## Crawl Data

Run the crawler:

```bash
python3 -m tiki_crawler.cli crawl --concurrency 20 --batch-size 1000
```

By default, the `crawl` command now runs with auto-restart enabled. If the
process crashes because of an unexpected runtime or network-related error, the
runner sleeps for a short delay, starts the crawl again, and resumes from the
batches that already exist on disk.

Useful options:

- `--no-auto-restart`: stop immediately when the process crashes
- `--restart-delay 10`: wait 10 seconds before trying again
- `--max-restarts 5`: allow at most 5 automatic restart attempts

The command-line options can override the defaults defined in `settings.yaml`.

If you want to use another CSV file:

```bash
python3 -m tiki_crawler.cli crawl --ids-file another_products.csv --concurrency 20 --batch-size 1000
```

## Output

The crawler writes data to the `data/output/` directory:

- `data/output/products_00001.json`, `data/output/products_00002.json`, ...
- `data/output/_failed/failed_00001.json`, ...
- `data/output/summary.json`
- `data/output/input_validation_report.json`
- `data/output/output_validation_report.json`
- `data/output/checkpoint.json`
- `data/output/retry/retry_summary.json`
- `data/output/retry/confirmed_404.json`
- `data/output/retry/still_unstable.json`

Each product output file contains normalized records with these fields:

- `id`
- `name`
- `url_key`
- `price`
- `description`
- `images`

Each failed record contains:

- `product_id`
- `status_code`
- `error`
- `elapsed_s`

The retry pipeline now rechecks failed IDs in multiple slow sequential rounds and splits
the unresolved set into:

- `confirmed_404`: IDs that consistently returned `404` in every recheck round
- `still_unstable`: IDs that kept failing, but not always in the same way

## Description Normalization

The `description` field returned by the API is HTML.  
The crawler normalizes it into plain text by:

- extracting readable text from HTML
- cleaning repeated whitespace
- preserving simple line breaks and list items
- removing the repeated Tiki disclaimer at the end
- extracting image URLs embedded inside the description

## Final Crawl Summary

After the crawl finishes, the program prints a final summary in the terminal, including:

- total IDs
- processed IDs
- success count
- error count
- success rate
- total elapsed time
- average request rate
- completed batches
- skipped batches
- error breakdown
- summary file location

## Pipeline Stages

The crawler follows a data-first pipeline:

1. Validate and deduplicate the input CSV
2. Crawl product details in batches
3. Write successful and failed records to disk immediately
4. Save a checkpoint after each completed batch
5. Auto-restart and resume safely if the crawl process crashes
6. Run a slower sequential retry pipeline for failed IDs
7. Validate the generated output
8. Write final reports and summary files

For more detail, see:

- `MEETING_NOTES_VI.md`
- `PIPELINE_GUIDE_VI.md`
- `PRODUCTION_READY_CHECKLIST.md`
