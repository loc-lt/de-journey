#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INPUT_CSV="${1:-$SCRIPT_DIR/tmdb-movies.csv}"
OUTPUT_DIR="${2:-$SCRIPT_DIR/output}"

check_requirements() {
    command -v awk >/dev/null 2>&1 || { echo "Missing command: awk" >&2; exit 1; }
    command -v gawk >/dev/null 2>&1 || { echo "Missing command: gawk" >&2; exit 1; }
    command -v sort >/dev/null 2>&1 || { echo "Missing command: sort" >&2; exit 1; }
    command -v head >/dev/null 2>&1 || { echo "Missing command: head" >&2; exit 1; }
    command -v tail >/dev/null 2>&1 || { echo "Missing command: tail" >&2; exit 1; }
}

check_input() {
    if [[ ! -f "$INPUT_CSV" ]]; then
        echo "Input file not found: $INPUT_CSV" >&2
        echo "Place tmdb-movies.csv next to run_all.sh or pass the file path as the first argument." >&2
        exit 1
    fi
}

prepare_output_dir() {
    mkdir -p "$OUTPUT_DIR"
}

merge_csv_records() {
    awk '
    {
        # Join physical lines into one logical CSV record.
        # A space is used so the downstream gawk reads one record per line.
        rec = rec (rec ? " " : "") $0

        for (i = 1; i <= length($0); i++) {
            c = substr($0, i, 1)
            if (c == "\"") {
                if (substr($0, i, 2) == "\"\"") {
                    i++
                } else {
                    inq = !inq
                }
            }
        }

        if (!inq) {
            print rec
            rec = ""
        }
    }
    ' "$INPUT_CSV"
}

question_1() {
    local out_file="$OUTPUT_DIR/question_1.csv"

    echo "[Q1] Sort movies by release date descending"

    head -n 1 "$INPUT_CSV" > "$out_file"

    merge_csv_records |
        tail -n +2 |
        gawk '
        BEGIN {
            FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
        }
        {
            split($16, d, "/")
            yy = d[3] + 0
            yyyy = (yy < 30 ? 2000 + yy : 1900 + yy)
            ts = mktime(sprintf("%04d %02d %02d 00 00 00", yyyy, d[1], d[2]))
            printf "%010d\t%s\n", ts, $0
        }
        ' |
        sort -nr -k1,1 |
        cut -f2- >> "$out_file"
}

question_2() {
    local out_file="$OUTPUT_DIR/question_2.csv"

    echo "[Q2] Filter movies with vote_average > 7.5"

    head -n 1 "$INPUT_CSV" > "$out_file"

    merge_csv_records |
        tail -n +2 |
        gawk '
        BEGIN {
            FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
        }
        ($18 + 0) > 7.5 {
            print $0
        }
        ' >> "$out_file"
}

question_3() {
    local out_file="$OUTPUT_DIR/question_3.txt"

    echo "[Q3] Find movies with highest and lowest revenue"

    merge_csv_records |
        gawk '
        BEGIN {
            FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
        }
        function unq(s) {
            if (s ~ /^"/) {
                sub(/^"/, "", s)
                sub(/"$/, "", s)
                gsub(/""/, "\"", s)
            }
            return s
        }
        NR == 1 {
            next
        }
        {
            rev = $5 + 0
            title = unq($6)

            if (!seen || rev > max_rev) {
                max_rev = rev
                max_title = title
                max_row = $0
            }
            if (!seen || rev < min_rev) {
                min_rev = rev
                min_title = title
                min_row = $0
            }
            seen = 1
        }
        END {
            print "Highest revenue movie:"
            print "title = " max_title
            print "revenue = " max_rev
            print "row = " max_row
            print ""
            print "Lowest revenue movie:"
            print "title = " min_title
            print "revenue = " min_rev
            print "row = " min_row
        }
        ' > "$out_file"
}

question_4() {
    local out_file="$OUTPUT_DIR/question_4.txt"

    echo "[Q4] Calculate total revenue"

    merge_csv_records |
        gawk '
        BEGIN {
            FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
        }
        NR > 1 {
            sum += $5 + 0
        }
        END {
            printf "total_revenue=%.0f\n", sum
        }
        ' > "$out_file"
}

question_5() {
    local out_file="$OUTPUT_DIR/question_5.tsv"

    echo "[Q5] Top 10 movies with highest profit"

    {
        printf "profit\ttitle\tbudget\trevenue\trelease_date\n"

        merge_csv_records |
            tail -n +2 |
            gawk '
            BEGIN {
                FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
                OFS = "\t"
            }
            function unq(s) {
                if (s ~ /^"/) {
                    sub(/^"/, "", s)
                    sub(/"$/, "", s)
                    gsub(/""/, "\"", s)
                }
                return s
            }
            {
                budget = $4 + 0
                revenue = $5 + 0
                profit = revenue - budget
                print profit, unq($6), budget, revenue, unq($16)
            }
            ' |
            sort -nr -k1,1 |
            awk 'NR <= 10 { print }'
    } > "$out_file"
}

question_6() {
    local out_file="$OUTPUT_DIR/question_6.txt"

    echo "[Q6] Find most prolific director and actor"

    merge_csv_records |
        tail -n +2 |
        gawk '
        BEGIN {
            FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
        }
        function unq(s) {
            if (s ~ /^"/) {
                sub(/^"/, "", s)
                sub(/"$/, "", s)
                gsub(/""/, "\"", s)
            }
            return s
        }
        {
            director_name = unq($9)
            if (director_name != "") {
                director_count[director_name]++
            }

            cast_text = unq($7)
            actor_total = split(cast_text, actor_list, /\|/)
            for (i = 1; i <= actor_total; i++) {
                if (actor_list[i] != "") {
                    actor_count[actor_list[i]]++
                }
            }
        }
        END {
            for (name in director_count) {
                if (director_count[name] > max_director_movies) {
                    max_director_movies = director_count[name]
                    best_director = name
                }
            }

            for (name in actor_count) {
                if (actor_count[name] > max_actor_movies) {
                    max_actor_movies = actor_count[name]
                    best_actor = name
                }
            }

            print "Director with most movies:"
            print "name = " best_director
            print "movie_count = " max_director_movies
            print ""
            print "Actor with most movies:"
            print "name = " best_actor
            print "movie_count = " max_actor_movies
        }
        ' > "$out_file"
}

question_7() {
    local out_file="$OUTPUT_DIR/question_7.csv"

    echo "[Q7] Count movies by genre"

    {
        printf "genre,count\n"

        merge_csv_records |
            tail -n +2 |
            gawk '
            BEGIN {
                FPAT = "([^,]*)|(\"([^\"]|\"\")*\")"
            }
            function unq(s) {
                if (s ~ /^"/) {
                    sub(/^"/, "", s)
                    sub(/"$/, "", s)
                    gsub(/""/, "\"", s)
                }
                return s
            }
            {
                genres_text = unq($14)
                genre_total = split(genres_text, genre_list, /\|/)
                for (i = 1; i <= genre_total; i++) {
                    if (genre_list[i] != "") {
                        genre_count[genre_list[i]]++
                    }
                }
            }
            END {
                for (genre in genre_count) {
                    print genre "," genre_count[genre]
                }
            }
            ' |
            sort -t, -k2,2nr -k1,1
    } > "$out_file"
}

question_8() {
    local out_file="$OUTPUT_DIR/question_8_ideas.md"

    echo "[Q8] Write additional analysis ideas"

    cat > "$out_file" <<'EOF'
# Additional analysis ideas

1. Identify the year with the highest total box office revenue.
2. Determine which genre has the highest average vote score.
3. Rank directors by total revenue across their movies.
4. Calculate ROI for each movie to find the most efficient productions.
5. Detect the movies that suffered the biggest financial losses.
6. Compare average revenue by release month to spot seasonal trends.
EOF
}

main() {
    check_requirements
    check_input
    prepare_output_dir

    question_1
    question_2
    question_3
    question_4
    question_5
    question_6
    question_7
    question_8

    echo ""
    echo "Done. Outputs are available in: $OUTPUT_DIR"
}

main "$@"
