# Linux CMD Project 1

This project solves basic movie-data analysis tasks on `tmdb-movies.csv` using Linux command line tools only.

## Tools

- `bash`
- `awk`
- `gawk`
- `sort`
- `head`
- `tail`
- `cut`

## Main idea

The dataset contains CSV records with embedded newlines inside quoted fields.  
To handle that safely:

1. `awk` is used first to merge physical lines into one logical CSV record.
2. `gawk` is then used with `FPAT` to parse CSV fields and run each analysis.

## Project structure

```text
project1/
├── README.md
├── run_all.sh
└── tmdb-movies.csv
```

Generated outputs:

```text
output/
├── question_1.csv
├── question_2.csv
├── question_3.txt
├── question_4.txt
├── question_5.tsv
├── question_6.txt
├── question_7.csv
└── question_8_ideas.md
```

## Requirements

- Linux environment
- `gawk` installed
- input file: `tmdb-movies.csv`

## How to run

Place `tmdb-movies.csv` in the same directory as `run_all.sh`, then run:

```bash
bash run_all.sh
```

Or pass the input path manually:

```bash
bash run_all.sh /path/to/tmdb-movies.csv
```

You can also pass a custom output directory:

```bash
bash run_all.sh /path/to/tmdb-movies.csv /path/to/output
```

## Tasks covered

1. Sort movies by release date in descending order
2. Filter movies with average vote above `7.5`
3. Find the highest-revenue and lowest-revenue movies
4. Compute total revenue of all movies
5. Get the top 10 most profitable movies
6. Find the director with the most movies and the actor appearing in the most movies
7. Count movies by genre
8. Provide additional analysis ideas

## Output files

- `question_1.csv`: movies sorted by release date descending
- `question_2.csv`: movies with `vote_average > 7.5`
- `question_3.txt`: highest and lowest revenue movies
- `question_4.txt`: total revenue
- `question_5.tsv`: top 10 highest-profit movies
- `question_6.txt`: most prolific director and actor
- `question_7.csv`: movie counts by genre
- `question_8_ideas.md`: extra analysis suggestions

## Notes

- The script assumes the column positions match the provided `tmdb-movies.csv` file.
- If the CSV schema changes, field indexes in `run_all.sh` must be updated.
- `tmdb-movies.csv` is ignored in `.gitignore`, so it does not need to be pushed to GitHub.
