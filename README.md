# Tiki Product Crawler

This project downloads product details from Tiki in batches and stores the results as JSON files.

## Project Structure

```text
project02/
  data/
    input/
      products-0-200000.csv
    output/
  requirements.txt
  README.md
  product_sample.json
  tiki_crawler/
    __init__.py
    cli.py
    client.py
    normalize.py
    writer.py
    models.py
    probe.py
```

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

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

## Crawl Data

Run the crawler:

```bash
python3 -m tiki_crawler.cli crawl --concurrency 20 --batch-size 1000
```

If you want to use another CSV file:

```bash
python3 -m tiki_crawler.cli crawl --ids-file another_products.csv --concurrency 20 --batch-size 1000
```

## Output

The crawler writes data to the `data/output/` directory:

- `data/output/products_00001.json`, `data/output/products_00002.json`, ...
- `data/output/_failed/failed_00001.json`, ...
- `data/output/summary.json`

Each product output file contains normalized records with these fields:

- `id`
- `name`
- `url_key`
- `price`
- `description`
- `images`

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
