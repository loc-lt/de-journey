```mermaid
flowchart LR
  subgraph M[Modules]
    M1[M01 Linux & Bash]
    M2[M02 Network & REST API]
    M3[M03 Python for Data]
    M4[M04 SQL Advanced]
    M5[M05 GCP · Lake · Warehouse]
    M6[M06 dbt]
  end

  subgraph P[Projects]
    P1[P01 TMDB bằng bash/awk]
    P2[P02 Tiki crawler 200k]
    P3[P03 Sinh dữ liệu bán hàng → Postgres]
    P4[P04 5 triệu đơn · partition · index]
    P5[P05 Glamira: 41 triệu event → Mongo trên GCP]
    P6[P06 Pipeline & Storage]
    P7[P07 Transformation & Visualization]
  end

  M1 --> P1
  M2 --> P2
  M3 --> P3
  M4 --> P4
  M5 --> P5
  M5 --> P6
  M6 --> P7

  P3 == cùng DB, bảng master ==> P4
  P5 == dữ liệu Glamira ==> P6 ==> P7
  P2 -. kinh nghiệm crawl .-> P5
  M1 -. bash: infra/gcp/*.sh, tmux .-> P5
  M2 -. SSH tunnel tới Mongo .-> P5
  M4 -. SQL, partition, index .-> P6

  subgraph C[Ý tưởng lặp lại]
    C1([Đọc luồng, không nạp hết vào RAM])
    C2([Thử nhỏ trước khi chạy thật])
    C3([Chia lô])
    C4([Chạy lại an toàn])
    C5([Retry · backoff · phân loại lỗi])
    C6([Cổng kiểm tra dữ liệu])
    C7([Đo rồi mới quyết])
    C8([Cấu hình tách khỏi code])
  end

  P1 --- C1
  P5 --- C1
  P2 --- C2 & C3 & C4 & C5 & C6 & C7
  P3 --- C3 & C4 & C6 & C8
  P4 --- C2 & C3 & C6 & C7
  P5 --- C2 & C3 & C4 & C5 & C6 & C7 & C8
```

## Module → phải nắm gì → đã dùng ở đâu

| Module (Task ID) | Phải trả lời được | Đã dùng thật ở | Chưa dùng trong project nào |
|---|---|---|---|
| **M01 Linux & Bash** (1–8) | Pipe, redirect, stdin/stdout/stderr; `awk`/`sed`/`grep`/regex; quyền file; `ps`/`top`/`df`; biến, hàm, exit code; `set -euo pipefail`; cron | P01 `run_all.sh` (hàm, pipe, `awk`→`gawk`→`sort`→`cut`); P05 `infra/gcp/*.sh` (`lib.sh` dùng chung, script kiểm tra-rồi-tạo), `tmux` | cron, quyền file |
| **M02 Network & API** (9–12) | SSH key vs password, port forwarding; SFTP; HTTP method, status code, header; REST; JSON; rate limit | P02 `client.py` (status 200/404/429/5xx, header, HTTP/2); P05 `tunnel.sh` (SSH local forward 27018→27017), firewall theo IP | FTP/SFTP |
| **M03 Python for Data** (13–20) | venv và quản lý gói; kết nối Postgres, transaction; exception; pandas đọc/ghi/biến đổi; test | P03 (pandas `to_sql`, SQLAlchemy `engine.begin()`), P04 (`psycopg2.execute_values`), test ở P02/P04/P05 | pandas cho phân tích (groupby, merge) — P03 chủ yếu dùng để sinh và nạp |
| **M04 SQL Advanced** (21–33) | Window function, `PARTITION BY`, frame, `LEAD`/`LAG`; `CASE`; UDF; stored procedure; cursor; index; thứ tự thực thi; join vs subquery; đọc `EXPLAIN` | P04: `ROW_NUMBER() OVER (PARTITION BY …)` trong `01_report_functions.sql`, `SUM() OVER ()`, hàm `fn_…`, thủ tục `sp_snapshot_order_status_report`, `01_indexes.sql`, `00_baseline_explain.sql` | `LEAD`/`LAG`, named window, cursor |
| **M05 GCP · Lake · Warehouse** (34–52) | Compute Engine, VPC/firewall, GCS, Cloud Functions, BigQuery; định dạng file; chi phí; governance; data modeling; ETL vs ELT | P05: VM + firewall (`04_vm.sh`), bucket (`02_bucket.sh`), service account | Cloud Functions, BigQuery, Parquet/Avro, dimensional modeling → **P06** |
| **M06 dbt** (53–56) | model, source, ref, test, materialization; unit test; Looker | — | Toàn bộ → **P07** |

Cột cuối là danh sách lỗ hổng: học rồi nhưng chưa có project nào ép phải dùng. Ưu tiên ôn bằng prompt 05. Checklist cũng đang để chưa tick các task 26–32 của M04 (Cursors, Indexing, Order of Execution, Join vs nested query, chứng chỉ) — rà lại vì P06/P07 dựa nhiều vào SQL.

## Ý tưởng lặp lại qua các project — mỗi dòng là một file trong `concepts/`

| Ý tưởng | P01 | P02 | P03 | P04 | P05 |
|---|---|---|---|---|---|
| **Đọc luồng** (xử lý từng phần, không nạp hết vào RAM) | `awk` đọc từng dòng, gộp dòng vật lý thành bản ghi CSV | — | — | — | `stream/tar_bson.py` đọc 31 GB trong `.tar.gz` không giải nén; `bson_lite.py` chỉ giải mã field cần; HyperLogLog (`sketch.py`) đếm số giá trị khác nhau với sai số ~1% |
| **Thử nhỏ trước** | — | lệnh `probe` thử concurrency 5/10/20/40/60 | — | `--allow-small-run` với 100k đơn | pilot 100 sản phẩm; `--limit`, `--sample-size` |
| **Chia lô** | — | 1000 id/lô = 1 file | `to_sql(chunksize=1000)` | 25.000 đơn/lô; `execute_values` 10k/20k dòng | `INGEST_BATCH_SIZE=10000`, `insert_many(ordered=False)` |
| **Chạy lại an toàn** | Ghi đè file output | Bỏ qua lô đã có file + `checkpoint.json` + tự khởi động lại | `--reset-db` (xóa rồi tạo lại) | `--truncate-first` | `_id` = ObjectId gốc nên nạp lại không trùng (bỏ qua lỗi 11000); crawl lưu tiến độ ngay trong Mongo (`name` hoặc `not_found`) |
| **Retry + phân loại lỗi** | — | Thử lại 429/5xx/timeout với backoff `2^n` + jitter; 404 không thử lại; vòng kiểm lại tuần tự tách `confirmed_404` / `still_unstable` | — | — | `is_transient()`; mở lại Chrome khi chết; chậm lại khi CDN bóp; `_with_mongo_retry` |
| **Cổng kiểm tra dữ liệu** | `check_requirements`, `check_input` | Báo cáo kiểm input (trùng, sai) và output | `validators.py`: khóa ngoại, trùng, khoảng ngày | `sql/01_quality_gate/` 4 file | `data_quality_report.md`, `null_profile.md`, đối chiếu đúng 41.432.473 document sau khi nạp; `product-status` so với seed |
| **Đo rồi mới quyết** | — | probe đo req/s, p95, tỉ lệ lỗi | — | benchmark trước/sau index (`snapshot_benchmarks.py`, `compare_benchmarks.py`) | `scope_confirmation.md`: quyết định GO dựa trên tỉ lệ đo được (IP 99,16% trên `checkout_success`) |
| **Cấu hình tách khỏi code** | Tham số dòng lệnh có mặc định | `settings.yaml` + CLI ghi đè | `.env` + `.env.example` | `.env` | `.env` + `gcp.env`, lớp `Settings` |
| **Một lệnh, nhiều lệnh con** | `run_all.sh` gồm các hàm `question_N` | `cli.py`: `probe`, `crawl` | `main.py` với cờ `--load`, `--reset-db` | `run_order.md` 26 bước | `cli.py`: `explore` / `ingest` / `enrich` |
| **Quản lý gói** | — | pip + `requirements.txt` | Poetry | Poetry | uv |

Hai dòng đáng viết thành bài riêng vì cho thấy bạn tiến bộ thế nào:

- **Chạy lại an toàn:** từ "ghi đè" (P01) → "nhớ đã làm tới đâu bằng file" (P02) → "xóa sạch làm lại" (P03, P04) → "nạp lại bao nhiêu lần cũng ra cùng kết quả vì khóa chính lấy từ nguồn" (P05). Cách cuối là idempotent thật sự; hai cách giữa có điểm yếu riêng (xem Mục 7).
- **Crawl:** P02 gọi API JSON công khai bằng `httpx` bất đồng bộ, 20 kết nối. P05 thử lại cách đó thì bị CDN trả 403 → phải dùng Chrome thật qua Playwright, 1 request/giây → rồi tìm ra endpoint JSON `reactdata` (robots.txt cho phép), gọi `fetch()` từ trong tab Chrome, ~0,5 giây/sản phẩm thay vì 5–10 giây khi tải cả trang. Cùng bài toán, ràng buộc khác nên lời giải khác — đây là câu trả lời mẫu cho "sao không dùng async như lần trước?".
