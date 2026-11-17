# DE Journey — Setup repo tổng hợp để học Data Engineer cùng AI

> Dành cho: Lê Thành Lộc — khóa DE Batching (6 modules, 7 projects).
> Bản 2 (15/11/2026): đã đọc code của 5 repo `loc-lt/01…05`. P01–P04 đã nộp, P05 đang làm, P06–P07 sắp làm.
>
> **Giới hạn:** tôi đọc được GitHub nhưng không mở được các link Notion (đề bài P03–P07). Mọi mô tả dưới đây lấy từ code, README và git log; chỗ nào cần đề bài tôi ghi rõ.

---

## 0. Tóm tắt 1 phút

1. Tạo **một repo** `de-journey`, kéo 5 repo vào `projects/` bằng `git subtree` (giữ lịch sử commit).
2. Ba tầng: `roadmap/` (khóa học yêu cầu gì) → `knowledge/` (tôi hiểu gì) → `projects/` (tôi đã làm gì, vì sao).
3. `AGENTS.md` ở gốc cho AI biết bạn là ai, đang ở đâu, phải giải thích kiểu nào. `prompts/` chứa prompt dùng lại.
4. Điều tôi thấy sau khi đọc code: 5 project của bạn **không rời rạc** — cùng vài ý tưởng lặp lại và lớn dần (chạy thử nhỏ trước, chia lô, chạy lại không trùng, kiểm tra dữ liệu ở cổng vào/ra). Mục 6.3 là bảng đó, kèm file minh chứng. Đây là thứ đáng "flex" nhất và cũng là xương sống của sơ đồ kiến thức.

---

## 1. Các project thực tế (đọc từ repo)

| Mã | Repo | Thực chất là gì | Công cụ chính | Trạng thái |
|---|---|---|---|---|
| P01 | `01_linux_cmd_prj` | Phân tích `tmdb-movies.csv` chỉ bằng dòng lệnh; 1 file `run_all.sh`, 8 câu hỏi → 8 file output | bash, awk, gawk (`FPAT`), sort, cut | Xong, 1 commit |
| P02 | `02_tiki_crawler` | Tải chi tiết 200k sản phẩm Tiki qua API, 1000 sp/file JSON, có probe, checkpoint, retry, tự khởi động lại | Python, `asyncio`, `httpx` (HTTP/2), PyYAML, pip | Xong, 4 commit |
| P03 | `03_python_in_data` | Sinh dữ liệu giả cho hệ thống bán hàng (7 bảng: brand, category, seller, customer, product, promotion, promotion_product) → CSV → PostgreSQL, có kiểm tra sau khi nạp | Faker, pandas, numpy, SQLAlchemy, Poetry | Xong, 6 commit |
| P04 | `04_sql` | Làm tiếp trên DB của P03: bảng `orders`/`order_item` phân vùng theo tháng, 5 triệu đơn (~17,5 triệu dòng), index, đo trước/sau bằng EXPLAIN, view, KPI, hàm + thủ tục báo cáo | PostgreSQL, plpgsql, psycopg2 `execute_values`, Poetry | Đã nộp, 3 commit — còn việc dở (Mục 2, Bước 4) |
| P05 | `05_glamira` | Dữ liệu hành vi Glamira: đọc luồng file mongodump 31 GB (41.432.473 document) không giải nén, đo chất lượng, dựng MongoDB trên VM GCP, tra IP → quốc gia, crawl ~19k sản phẩm | pymongo, IP2Location, Playwright, BeautifulSoup, gcloud, uv | Đang làm, 31 commit |
| P06 | chưa có | Data Pipeline & Storage — dùng dữ liệu P05 | (theo đề) | Sắp làm |
| P07 | chưa có | Data Transformation & Visualization — dùng P05, P06 | dbt, Looker (theo checklist) | Sắp làm |

Khác với bản trước của tài liệu này: P03 **không phải** "làm lại P01 bằng Pandas" như checklist cũ ghi, mà là bộ sinh dữ liệu; P04 **không phải** Bee Movies mà nối thẳng vào P03. Chuỗi phụ thuộc thật là **P03 → P04** và **P05 → P06 → P07**.

---

## 2. Cây thư mục và setup

```text
de-journey/
├── AGENTS.md                  # Ngữ cảnh + luật chơi cho mọi AI agent (nguồn chính)
├── CLAUDE.md                  # 1 dòng trỏ về AGENTS.md
├── README.md                  # Trang bìa: bảng project, link sơ đồ
├── .gitignore
│
├── roadmap/
│   ├── checklist.xlsx         # File gốc
│   ├── checklist.md           # Bản markdown cho AI đọc
│   ├── briefs/                # Đề bài dán từ Notion: p03.md … p07.md
│   └── progress.md            # Đang ở đâu, còn nợ gì
│
├── knowledge/
│   ├── MAP.md                 # Sơ đồ module ↔ project ↔ khái niệm
│   ├── glossary.md            # Từ điển keyword
│   ├── modules/               # m01-linux-bash.md … m06-dbt.md
│   └── concepts/              # 1 file = 1 ý dùng lại nhiều project (Mục 6.3)
│
├── projects/
│   ├── _template/             # README.md + docs/{BUILD_LOG,DECISIONS,RETRO}.md
│   ├── p01-linux-cmd/
│   ├── p02-tiki-crawler/
│   ├── p03-python-in-data/
│   ├── p04-sql/
│   ├── p05-glamira/
│   ├── p06-data-pipeline-storage/
│   └── p07-transformation-visualization/
│
├── prompts/                   # 01 … 07 (Mục 5)
└── journal/{daily,bugs}/
```

Quy ước tên: `mNN-…`/`pNN-…` chữ thường nối `-` để sắp đúng thứ tự và gõ được trên bash không cần escape. `modules/` là thứ tự học, `concepts/` là thứ dùng lại — tách ra vì "retry" học ở P02 nhưng dùng lại ở P05. Mỗi project đúng 4 file doc giống nhau để AI và bạn luôn biết tìm gì ở đâu.

### Bước 1 — Khung thư mục

```bash
mkdir de-journey && cd de-journey && git init

mkdir -p roadmap/briefs knowledge/{modules,concepts} prompts journal/{daily,bugs} \
         projects/_template/docs
touch AGENTS.md CLAUDE.md README.md roadmap/progress.md knowledge/{MAP,glossary}.md \
      projects/_template/README.md projects/_template/docs/{BUILD_LOG,DECISIONS,RETRO}.md

cat > .gitignore <<'EOF'
.env
*.env
!.env.example
!*.env.example
.venv/
.uv/
__pycache__/
*.py[cod]
.pytest_cache/
.idea/
.vscode/
data/
output/*
!output/.gitkeep
*.tar.gz
*.bson
*.BIN
*.log
EOF

cp /duong/dan/checklist.xlsx roadmap/checklist.xlsx
git add . && git commit -m "chore: scaffold de-journey"
```

### Bước 2 — Bí mật: đã kiểm tra giúp

Tôi đã quét 5 repo (file đang track và tên file trong toàn bộ lịch sử): **không có** `.env`, `gcp.env`, key hay mật khẩu thật. Chỉ có `DB_PASSWORD=postgres` làm ví dụ trong README/.env.example — chấp nhận được. Mật khẩu Mongo trên VM được nhập tay lúc chạy `install_mongo.sh`, không nằm trong repo. Không cần làm gì thêm.

### Bước 3 — Gộp 5 repo, giữ lịch sử

Cả 5 repo đều dùng nhánh `main`.

```bash
git subtree add --prefix=projects/p01-linux-cmd      https://github.com/loc-lt/01_linux_cmd_prj.git  main
git subtree add --prefix=projects/p02-tiki-crawler   https://github.com/loc-lt/02_tiki_crawler.git   main
git subtree add --prefix=projects/p03-python-in-data https://github.com/loc-lt/03_python_in_data.git main
git subtree add --prefix=projects/p04-sql            https://github.com/loc-lt/04_sql.git            main
git subtree add --prefix=projects/p05-glamira        https://github.com/loc-lt/05_glamira.git        main

for p in projects/p0[1-5]-*; do mkdir -p "$p/docs"; cp -n projects/_template/docs/*.md "$p/docs/"; done
```

**P05 đang làm dở — chọn một nơi làm việc.** Khuyến nghị: từ giờ làm trong `de-journey/projects/p05-glamira` (để AI có đủ ngữ cảnh các project trước), khi cần nộp thì đẩy ngược về repo cũ:

```bash
git subtree push --prefix=projects/p05-glamira https://github.com/loc-lt/05_glamira.git main
```

Trước khi chuyển: commit hết ở repo cũ, và copy tay các file **không nằm trong git** sang thư mục mới — `.env`, `infra/gcp/gcp.env`, thư mục `data/` (seed `product_urls.csv`, log crawl). Script `resume.sh` đọc các file này.

### Bước 4 — Dọn những chỗ lệch tôi thấy trong repo

| Project | Vấn đề | Việc cần làm |
|---|---|---|
| P02 | README nhắc `MEETING_NOTES_VI.md`, `PIPELINE_GUIDE_VI.md`, `PRODUCTION_READY_CHECKLIST.md` nhưng 3 file này không có trên GitHub | Tìm trên máy. Đây chính là ghi chú học của bạn — đưa vào `docs/`. Nếu mất thì xóa dòng tham chiếu |
| P02 | Thư mục `.idea/` (cấu hình PyCharm) bị commit | `git rm -r --cached projects/p02-tiki-crawler/.idea` |
| P02 | `requirements.txt` không ghi phiên bản | Ghi phiên bản đang dùng (`pip freeze`) |
| P04 | README trỏ tới `docs/HUONG_DAN_CHAY_DU_AN_04.md` và `docs/KE_HOACH_DU_AN_05.md` — không có trên GitHub | Như trên: tìm và đưa vào, hoặc bỏ link |
| P04 | `sql/99_submission/results_snapshot.md` **vẫn là mẫu trống**, trong khi chính file ghi "không để placeholder khi nộp" | Chạy lại benchmark, điền số thật. Đây là bằng chứng index/partition có tác dụng — thiếu nó thì không bảo vệ được phần tối ưu |
| P04 | README hướng dẫn `cd ../project03`; `src/config.py` đọc `.env` ở thư mục cha làm dự phòng | Sau khi gộp: sửa thành `../p03-python-in-data`; đặt `.env` ngay trong `p04-sql/` để không phụ thuộc thư mục cha |
| P05 | `pyproject.toml` khai `readme = "README.md"` nhưng chưa có README | Viết README theo template (Mục 4). Nội dung đã có sẵn trong `docs/scope_confirmation.md` |
| P01 | Chỉ 1 commit → không dựng lại được thứ tự từ git | BUILD_LOG dựng theo thứ tự hàm trong `run_all.sh` |

### Bước 5 — Dán nội dung các file lõi

Mục 3 (AGENTS.md), Mục 4 (template), Mục 5 (prompts), Mục 6 (MAP.md, bảng module, bảng khái niệm). Nhanh nhất: mở repo bằng AI agent, đưa file này, nói *"Tạo các file theo đúng nội dung Mục 3–6, không thêm bớt"*.

### Bước 6 — Dán đề bài Notion

Lưu đề P03, P04, P05, P06, P07 vào `roadmap/briefs/pNN.md`. Việc này bắt buộc làm tay: không có đề thì AI không biết code đã đáp ứng yêu cầu nào, và không lên kế hoạch P06 được.

### Bước 7 — Backfill doc (thứ tự và trọng tâm)

Với mỗi project: prompt 01 (build log) → prompt 02 (decisions) → **tự viết** RETRO → prompt 03 (note module) → prompt 04 (cập nhật sơ đồ) → prompt 05 (vấn đáp). Bước vấn đáp là bước biến "có tài liệu" thành "nắm chắc" — đừng bỏ.

| Thứ tự | Project | Vì sao theo thứ tự này | Trọng tâm khi viết |
|---|---|---|---|
| 1 | **P05** | Đang làm, còn nhớ; P06 cần nó ngay; git log 31 commit kể gần đủ câu chuyện | Vì sao tự đọc luồng tar/BSON; vì sao bảng `ip_geo` riêng; vì sao đổi từ crawl trang sang endpoint JSON |
| 2 | **P02** | Nền của phần crawl ở P05 — so sánh hai lần crawl là bài học lớn nhất | Mục 7 đã viết sẵn D1 |
| 3 | **P03 + P04** | Làm chung vì chung một DB | Thứ tự nạp bảng theo khóa ngoại; partition; index nào giúp query nào |
| 4 | **P01** | Nhỏ, 1 buổi | Vì sao phải gộp dòng CSV trước; `FPAT` là gì |

---

## 3. File ngữ cảnh cho AI

### `AGENTS.md`

```markdown
# AGENTS.md — de-journey

## Tôi là ai
- Lê Thành Lộc, đang học Data Engineer (khóa DE Batching: 6 modules, 7 projects).
- Mới với DE. Mục tiêu: hiểu đủ sâu để tự giải thích và bảo vệ mọi quyết định trong
  project của mình khi phỏng vấn, không chỉ chạy được code.
- Đã dùng: bash/awk, Python (asyncio, httpx, pandas, Faker, SQLAlchemy, psycopg2,
  pymongo, Playwright), PostgreSQL (partition, index, plpgsql), MongoDB,
  GCP (Compute Engine, GCS, firewall, gcloud), pip → Poetry → uv.
- Sắp học: BigQuery, Cloud Functions, data modeling, dbt, Looker.

## Repo này là gì
- `roadmap/`   : khóa học yêu cầu gì. `checklist.md` + `briefs/pNN.md` (đề bài).
- `knowledge/` : tôi hiểu gì. `MAP.md` sơ đồ tổng, `modules/` theo thứ tự học,
                 `concepts/` khái niệm dùng lại nhiều project, `glossary.md` từ điển.
- `projects/`  : tôi đã làm gì. Mỗi project: README.md + docs/{BUILD_LOG,DECISIONS,RETRO}.md.
- Phụ thuộc: P03 → P04 (chung DB `ecommerce_project03`). P05 → P06 → P07 (dữ liệu Glamira).
- Trạng thái hiện tại: `roadmap/progress.md`.

## Luật khi làm việc với tôi
1. **Không bịa.** Mô tả project phải dựa trên code, docs và git log thật trong repo.
   Không chắc thì ghi `TODO(Lộc xác nhận)`.
2. **Ngôn ngữ:** giải thích tiếng Việt, giữ keyword tiếng Anh. Lần đầu gặp keyword:
   định nghĩa 1 câu.
3. **Giải thích một lựa chọn kỹ thuật luôn đủ 5 ý:**
   Là gì → Vì sao chọn → Phương án khác → Đánh đổi → Khi nào nó gãy.
4. **Liên kết kiến thức:** khái niệm đã có trong `knowledge/concepts/` hoặc đã dùng ở
   project trước thì nhắc lại kèm file ("giống checkpoint ở P02, `checkpoint.py`").
   Chưa có thì đề xuất tạo note.
5. **Chế độ học cho project mới:** không đưa lời giải hoàn chỉnh trước. Hỏi tôi định
   làm thế nào → góp ý → tôi code → review. Chỉ viết hộ khi tôi nói "viết giúp",
   sau đó giải thích từng phần.
6. **Sau thay đổi code có ý nghĩa**, nhắc tôi cập nhật BUILD_LOG, DECISIONS (nếu có
   lựa chọn mới), glossary (nếu có keyword mới).
7. **Trung thực:** code/thiết kế có vấn đề thì nói thẳng, kèm mức độ
   (phải sửa / nên sửa / tùy).
8. **An toàn:** không ghi key, mật khẩu, URI có mật khẩu vào file được commit.
   Lệnh tốn tiền trên GCP phải báo chi phí ước tính và cách dọn. Không chạy lệnh xóa
   dữ liệu (`--truncate-first`, `--reset-db`, `DROP`, xóa bucket/VM) khi chưa hỏi tôi.

## Quy ước
- Thư mục `mNN-ten`, `pNN-ten`. Commit `type(scope): nội dung`, scope = p02, m04, map...
- Mỗi project giữ môi trường riêng (P02 pip, P03–P04 Poetry, P05 trở đi uv).
  Project mới dùng uv, cấu hình qua `.env`, có `.env.example`.
- Thói quen đã thành nếp, project mới phải giữ: chạy thử nhỏ trước khi chạy thật;
  ghi theo lô; chạy lại không sinh trùng; đo và ghi số liệu vào `docs/`.
- Sơ đồ: mermaid.

## Định nghĩa "xong" cho một project
- [ ] Chạy lại được từ đầu theo README
- [ ] README có đề bài, cách chạy, kết quả bằng số
- [ ] BUILD_LOG, DECISIONS, RETRO đã viết
- [ ] Note module + MAP + glossary đã cập nhật
- [ ] Qua 1 lượt vấn đáp (prompts/05) không mở tài liệu
- [ ] Đã push và nộp form
```

### `CLAUDE.md`

```markdown
Đọc và tuân theo AGENTS.md ở thư mục gốc. Đó là nguồn hướng dẫn duy nhất.
```

---

## 4. Template cho mỗi project

### `projects/_template/README.md`

```markdown
# PNN — <Tên project>

| | |
|---|---|
| Module | MNN — … |
| Thời gian | … → … |
| Repo gốc | <link GitHub cũ nếu có> |
| Kiến thức dùng | [[concept-a]], [[concept-b]] |
| Dùng lại từ project trước | PNN: … |

## Đề bài
<dán nguyên yêu cầu từ Notion + DoD trong checklist>

## Kết quả
<số liệu cụ thể: bao nhiêu bản ghi, chạy mất bao lâu, bao nhiêu lỗi>

## Cách chạy
<các lệnh từ máy sạch>

## Cấu trúc thư mục
<tree + 1 dòng mô tả mỗi file>

## Tài liệu
- [BUILD_LOG](docs/BUILD_LOG.md) — dựng từ folder trống như thế nào
- [DECISIONS](docs/DECISIONS.md) — vì sao chọn cách này
- [RETRO](docs/RETRO.md) — học được gì, lần sau làm khác gì
```

### `docs/BUILD_LOG.md` — "từ folder trống tới project hoàn chỉnh"

```markdown
# BUILD LOG — PNN

> Mỗi bước = một thứ được sinh ra. Đọc từ trên xuống là dựng lại được project.

## Bước N — <việc làm>
- **Sinh ra:** `duong/dan/file`
- **Vì sao cần:** <vấn đề nó giải quyết; nếu thiếu nó thì sao>
- **Vì sao tên/vị trí như vậy:** <quy ước nào>
- **Nội dung chính:** <hàm/khối quan trọng, 3–7 gạch đầu dòng>
- **Lệnh đã chạy:** `…`
- **Kiểm tra đã đúng bằng cách:** <lệnh/kết quả mong đợi>
- **Khái niệm liên quan:** [[…]]
- **Vấp phải:** <lỗi gặp và cách sửa, nếu có>
```

### `docs/DECISIONS.md`

```markdown
# DECISIONS — PNN

## D1 — <câu hỏi phải quyết định>
- **Bối cảnh / ràng buộc:** <quy mô dữ liệu, thời gian, yêu cầu đề>
- **Các phương án:**
  | Phương án | Ưu | Nhược | Điều kiện cần |
  |---|---|---|---|
- **Chọn:** … 
- **Vì sao:** …
- **Đánh đổi chấp nhận:** …
- **Sẽ đổi quyết định khi:** <dữ liệu ×100? chạy hằng ngày? nhiều máy?>
- **Số đo thực tế:** <trước/sau, nếu có>
```

### `docs/RETRO.md` (tự viết, không nhờ AI)

```markdown
# RETRO — PNN
- 3 thứ học được:
- Chỗ mắc kẹt lâu nhất và cách thoát:
- Nếu làm lại sẽ làm khác:
- Câu hỏi còn mở:
- Thứ mang sang project sau:
```

### Template note module — `knowledge/modules/mNN-….md`

```markdown
# MNN — <Tên module>

## Một câu: module này dạy tôi làm được gì?
## Vì sao DE cần nó?
## Kiến thức phải nắm
| Chủ đề | Tôi phải trả lời được | Task ID | Mức tự tin (1–5) |
|---|---|---|---|
## Lệnh / cú pháp hay dùng (cheat sheet của riêng tôi)
## Áp dụng trong project nào, ở đâu
| Kiến thức | Project | File/dòng |
|---|---|---|
## Liên kết: cần gì từ module trước → mở đường cho module nào sau
## Lỗ hổng còn lại
```

### Template note khái niệm — `knowledge/concepts/<ten>.md`

```markdown
# <Khái niệm>
- **Định nghĩa 1 câu:**
- **Ví dụ đời thường:**
- **Vấn đề nó giải quyết:**
- **Tôi đã gặp ở:** P02 (`file.py`), P05 (…)
- **Dễ nhầm với:**
- **Câu hỏi phỏng vấn hay gặp:**
```

---

## 5. Thư viện prompt (`prompts/`)

Cách dùng: mở AI agent tại thư mục gốc repo (để nó đọc được `AGENTS.md` và code), dán prompt, thay `PNN`.

### `01-build-log-from-code.md`

```text
Đọc toàn bộ projects/PNN-… (code, cấu hình, README) và chạy
`git log --reverse --stat -- projects/PNN-…` để biết thứ tự file ra đời.

Viết projects/PNN-…/docs/BUILD_LOG.md theo đúng template trong
projects/_template/docs/BUILD_LOG.md, kể lại cách dựng project từ một folder trống:
- Thứ tự bước theo phụ thuộc logic (cái gì phải có trước), đối chiếu với git log.
  Nếu git log và logic mâu thuẫn, theo logic và ghi chú lại.
- Mỗi folder/file: vì sao tồn tại, vì sao tên như vậy, bên trong làm gì, dùng để làm gì.
- Trích đúng tên hàm, tên biến, lệnh có thật trong code. Không thêm thứ không có.
- Chỗ nào không suy ra được lý do từ code thì ghi TODO(Lộc xác nhận) và hỏi tôi ở cuối.
- Cuối file: danh sách design pattern / kỹ năng đã dùng, mỗi cái kèm file minh chứng.
Tôi là người mới: giải thích như cho người biết Python cơ bản nhưng chưa biết DE.
```

### `02-decisions.md`

```text
Dựa trên code thật của projects/PNN-… và đề bài trong README, liệt kê mọi lựa chọn kỹ
thuật có ý nghĩa (thư viện, cách xử lý song song, định dạng lưu, cách chia file,
xử lý lỗi, cấu trúc bảng...). Với mỗi lựa chọn viết một mục trong docs/DECISIONS.md
theo template, bắt buộc có:
- Tất cả phương án phổ biến cho bài toán đó (kể cả phương án tôi không dùng)
- Vì sao cách hiện tại hợp với ràng buộc của đề; điều kiện cần để nó hoạt động
- Khi nào cách hiện tại gãy và nên chuyển sang phương án nào
Sau đó chỉ ra 3 chỗ code hiện tại chưa tốt nhất, xếp theo mức độ nghiêm trọng.
Trước khi viết, hỏi tôi tối đa 5 câu về lý do thật sự tôi chọn như vậy.
```

### `03-module-note.md`

```text
Đọc roadmap/checklist.md phần module MNN, và docs của project tương ứng.
Viết knowledge/modules/mNN-….md theo template. Cột "Tôi phải trả lời được" viết dưới
dạng câu hỏi cụ thể. Cột "Áp dụng trong project" phải trỏ tới file thật.
Phần nào checklist yêu cầu mà project không dùng tới: liệt kê riêng ở "Lỗ hổng còn lại".
```

### `04-update-map.md`

```text
Vừa hoàn thành doc cho PNN. Hãy:
1. Cập nhật knowledge/MAP.md: thêm node/cạnh mới, giữ sơ đồ dưới 40 node
   (gộp chi tiết vào note thay vì thêm node).
2. Thêm keyword mới vào knowledge/glossary.md (xếp A–Z, 1 dòng định nghĩa, link note,
   ghi project đã dùng).
3. Với khái niệm xuất hiện ở từ 2 project trở lên mà chưa có file trong
   knowledge/concepts/: tạo file theo template. Khái niệm đã có: bổ sung mục "Tôi đã gặp ở".
Cho tôi xem diff trước khi ghi.
```

### `05-quiz-me.md`

```text
Đóng vai người phỏng vấn Senior Data Engineer. Dựa trên docs và code của PNN, hỏi tôi
10 câu, từng câu một, chờ tôi trả lời rồi mới hỏi tiếp:
- 3 câu "giải thích": cái này là gì, chạy thế nào
- 4 câu "vì sao": sao không dùng X, đánh đổi gì
- 3 câu "nếu": dữ liệu gấp 100 lần, chạy hằng ngày, mạng chập chờn thì sửa gì
Sau mỗi câu: chấm 0–2, nói thiếu gì, trỏ tới file note cần đọc lại.
Cuối buổi: ghi các câu dưới 2 điểm vào mục "Lỗ hổng còn lại" của note module.
```

### `06-start-new-project.md`

```text
Tôi bắt đầu PNN. Đề bài ở roadmap/briefs/pNN.md (và README của project).
1. Đọc đề, roadmap/checklist.md (module liên quan), knowledge/MAP.md và
   DECISIONS.md + RETRO.md của các project trước.
2. Cho tôi biết: project này dùng lại được gì từ P01–P(N-1) (khái niệm, đoạn code,
   bài học trong RETRO), và khái niệm nào hoàn toàn mới.
3. Hỏi tôi định thiết kế thế nào. KHÔNG đưa lời giải trước.
4. Sau khi tôi trả lời: góp ý, rồi cùng tôi chốt kế hoạch thành các bước nhỏ,
   mỗi bước có cách kiểm tra. Ghi kế hoạch vào đầu docs/BUILD_LOG.md.
Trong lúc làm, mỗi khi xong một bước, nhắc tôi ghi BUILD_LOG ngay.
```

### `07-bug-report.md`

```text
Tôi gặp lỗi sau: <dán lỗi + lệnh đã chạy>.
Trước khi đưa cách sửa: hỏi tôi đã thử gì, rồi gợi ý cách thu hẹp nguyên nhân.
Sau khi sửa xong, viết journal/bugs/YYYY-MM-DD-<ten>.md gồm: triệu chứng, nguyên nhân
gốc, cách tìm ra, cách sửa, cách phòng — theo đúng cấu trúc Bug Report của khóa học
để tôi dán sang Notion.
```

---

## 6. Nội dung khởi tạo cho `knowledge/`

### 6.1 `knowledge/MAP.md`

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

### 6.2 Module → phải nắm gì → đã dùng ở đâu

| Module (Task ID) | Phải trả lời được | Đã dùng thật ở | Chưa dùng trong project nào |
|---|---|---|---|
| **M01 Linux & Bash** (1–8) | Pipe, redirect, stdin/stdout/stderr; `awk`/`sed`/`grep`/regex; quyền file; `ps`/`top`/`df`; biến, hàm, exit code; `set -euo pipefail`; cron | P01 `run_all.sh` (hàm, pipe, `awk`→`gawk`→`sort`→`cut`); P05 `infra/gcp/*.sh` (`lib.sh` dùng chung, script kiểm tra-rồi-tạo), `tmux` | cron, quyền file |
| **M02 Network & API** (9–12) | SSH key vs password, port forwarding; SFTP; HTTP method, status code, header; REST; JSON; rate limit | P02 `client.py` (status 200/404/429/5xx, header, HTTP/2); P05 `tunnel.sh` (SSH local forward 27018→27017), firewall theo IP | FTP/SFTP |
| **M03 Python for Data** (13–20) | venv và quản lý gói; kết nối Postgres, transaction; exception; pandas đọc/ghi/biến đổi; test | P03 (pandas `to_sql`, SQLAlchemy `engine.begin()`), P04 (`psycopg2.execute_values`), test ở P02/P04/P05 | pandas cho phân tích (groupby, merge) — P03 chủ yếu dùng để sinh và nạp |
| **M04 SQL Advanced** (21–33) | Window function, `PARTITION BY`, frame, `LEAD`/`LAG`; `CASE`; UDF; stored procedure; cursor; index; thứ tự thực thi; join vs subquery; đọc `EXPLAIN` | P04: `ROW_NUMBER() OVER (PARTITION BY …)` trong `01_report_functions.sql`, `SUM() OVER ()`, hàm `fn_…`, thủ tục `sp_snapshot_order_status_report`, `01_indexes.sql`, `00_baseline_explain.sql` | `LEAD`/`LAG`, named window, cursor |
| **M05 GCP · Lake · Warehouse** (34–52) | Compute Engine, VPC/firewall, GCS, Cloud Functions, BigQuery; định dạng file; chi phí; governance; data modeling; ETL vs ELT | P05: VM + firewall (`04_vm.sh`), bucket (`02_bucket.sh`), service account | Cloud Functions, BigQuery, Parquet/Avro, dimensional modeling → **P06** |
| **M06 dbt** (53–56) | model, source, ref, test, materialization; unit test; Looker | — | Toàn bộ → **P07** |

Cột cuối là danh sách lỗ hổng: học rồi nhưng chưa có project nào ép phải dùng. Ưu tiên ôn bằng prompt 05. Checklist cũng đang để chưa tick các task 26–32 của M04 (Cursors, Indexing, Order of Execution, Join vs nested query, chứng chỉ) — rà lại vì P06/P07 dựa nhiều vào SQL.

### 6.3 Ý tưởng lặp lại qua các project — mỗi dòng là một file trong `concepts/`

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

### 6.4 `roadmap/checklist.md`

Prompt: *"Chuyển roadmap/checklist.xlsx (sheet Checklist Roadmap + Tasks Detail) thành roadmap/checklist.md: mỗi module một bảng Task ID, Task, DoD, Guideline, Status. Với Project 03 và 04, ghi chú rằng đề thực tế nằm ở roadmap/briefs/ và khác với mô tả trong checklist."*

---

## 7. Ví dụ mẫu: `DECISIONS.md` của P02, viết từ code thật

Đây là mẫu về độ sâu. Số đo thực tế tôi không có vì `data/output/` không được commit — điền từ `summary.json` trên máy bạn.

### D1 — Gọi 200.000 request theo cách nào?

**Bối cảnh:** mỗi id một request `GET api.tiki.vn/product-detail/api/v1/products/{id}` trả JSON. Đề yêu cầu rút ngắn thời gian và lưu lại sản phẩm lỗi.

**Bản chất:** gần như toàn bộ thời gian là chờ server trả lời (I/O-bound), CPU rảnh; các request độc lập nhau. Hai điều này là **điều kiện cần** để chạy đồng thời có lợi.

| Phương án                                                 | Ưu                                                             | Nhược                                                | Hợp khi                                               |
| --------------------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| Tuần tự (`requests` + vòng lặp)                           | Đơn giản, dễ debug                                             | Chậm nhất — 200k × ~0,3 s ≈ 16 giờ                   | Vài trăm request; hoặc khi cần *chắc* hơn cần *nhanh* |
| Đa luồng (`ThreadPoolExecutor`)                           | Giữ code đồng bộ quen thuộc                                    | Mỗi luồng tốn bộ nhớ; khó kiểm soát khi lên vài trăm | Vài chục request đồng thời                            |
| **Bất đồng bộ (**`asyncio` **+** `httpx.AsyncClient`**)** | Một luồng giữ được rất nhiều kết nối; dùng lại kết nối; HTTP/2 | Phải viết `async/await` xuyên suốt; khó debug hơn    | Rất nhiều request I/O                                 |
| Đa tiến trình                                             | Dùng nhiều nhân CPU                                            | Nặng; sai vấn đề vì nút thắt là mạng                 | Tính toán nặng                                        |
| Scrapy                                                    | Có sẵn hàng đợi, retry, giãn tốc                               | Thừa cho một endpoint JSON                           | Crawl nhiều trang theo link                           |

**Chọn:** bất đồng bộ. Trong code:

- `client.py › create_client()` — một `httpx.AsyncClient` dùng chung cho cả lần chạy, bật HTTP/2 nếu có gói `h2`.
- `cli.py › run_crawl()` — mỗi lô 1000 id: tạo `asyncio.Semaphore(concurrency)` rồi `asyncio.gather` toàn bộ lô. Mặc định `concurrency: 20` (`settings.yaml`).
- Con số 20 không phải đoán: lệnh `probe` chạy thử các mức 5/10/20/40/60 và in `success_rate`, `req_per_sec`, `p95_latency_s`, số lỗi 429.

**Điều kiện cần để chạy đồng thời an toàn — và code đáp ứng thế nào:**

| Điều kiện | Trong code |
|---|---|
| Giới hạn số request cùng lúc | `Semaphore`, bọc trong `fetch_product()` |
| Timeout từng request | `timeout_s: 15.0` |
| Một id lỗi không làm hỏng cả lô | `fetch_product()` luôn trả `FetchResult(ok=False, …)`, không ném lỗi ra `gather` |
| Phân loại lỗi | 429/500/502/503/504 và timeout/lỗi kết nối → thử lại; còn lại (404…) → ghi `http_<mã>` |
| Thử lại có giãn cách | `build_backoff_delay`: `2**attempt + random(0–0,3)` giây — jitter để các request không cùng thử lại một lúc |
| Tiếp tục được khi chết giữa chừng | Bỏ qua lô đã có file; `checkpoint.json`; `run_crawl_with_auto_restart()` |
| Thứ tự không quan trọng | Mỗi bản ghi mang `id` của nó |

**Sẽ đổi quyết định khi:** server chặn theo dấu vân tay trình duyệt (đã xảy ra ở P05 → Playwright); phải chạy hằng ngày (cần lập lịch, chỉ lấy phần thay đổi); lên hàng chục triệu id (cần hàng đợi, nhiều máy).

**Số đo:** `TODO(Lộc)` — bảng probe; tổng thời gian; req/s; tỉ lệ lỗi theo loại.

### D2 — Xử lý id lỗi: vì sao vòng sau lại chạy *tuần tự*?

Sau lượt chính, `retry_pipeline.py` gom mọi id trong `_failed/`, rồi kiểm lại bằng client **đồng bộ**, từng id một, 3 vòng cách nhau 1,5 giây, timeout dài hơn (20 s), thử lại nhiều hơn (3). Kết quả tách hai nhóm: `confirmed_404` (cả 3 vòng đều 404 → sản phẩm thật sự không còn) và `still_unstable` (lỗi không nhất quán).

Lý do: ở lượt chính, lỗi có thể do *chính mình gây ra* (gửi quá nhanh). Kiểm lại chậm và đơn lẻ loại bỏ khả năng đó, nên kết luận "404 thật" mới đáng tin. Đánh đổi: chậm — chấp nhận được vì số id lỗi nhỏ. Đây là câu trả lời cho "sao lúc async lúc không?": **tốc độ cho phần lớn, độ chắc chắn cho phần còn lại.**

### D3–D5 nên viết tiếp

- D3 — vì sao 1000 sản phẩm/file (đề yêu cầu; và nó cũng là đơn vị để tiếp tục khi chết).
- D4 — làm sạch `description` bằng `html.parser` có sẵn thay vì BeautifulSoup (`normalize.py › DescriptionParser`): ít phụ thuộc hơn, đổi lại phải tự liệt kê `BLOCK_TAGS`.
- D5 — `settings.yaml` + CLI ghi đè.

### Ba câu hỏi để tự kiểm (tôi thấy khi đọc code)

1. `writer.py › write_json()` **ghi thẳng vào file đích, còn** `run_crawl()` **coi "file tồn tại" là "lô đã xong".** Nếu tiến trình chết đúng lúc đang ghi thì sao? Lần chạy lại sẽ làm gì với file dở đó? (Gợi ý cách sửa: ghi ra file tạm rồi đổi tên.) — mức: nên sửa.
2. `fetch_product()` và `fetch_product_sync()` gần như giống hệt nhau. Sửa quy tắc retry ở một chỗ mà quên chỗ kia thì hậu quả gì? — mức: tùy.
3. `gather` giữ cả 1000 kết quả trong RAM rồi mới ghi. Với 1000 thì ổn; nếu đề đổi thành 100.000 sản phẩm/file thì sao?

Trả lời được ba câu này là bạn đã hiểu project hơn mức "chạy được".

---

## 8. Quy trình cho project mới (P06, P07)

| Lúc | Việc | File chạm tới |
|---|---|---|
| Ngày 0 | `cp -r projects/_template projects/p06-…`; dán đề vào README; chạy prompt 06 | README, BUILD_LOG (phần kế hoạch) |
| Mỗi buổi làm | Xong một bước → ghi ngay 1 mục BUILD_LOG (5 phút). Có lựa chọn → 1 mục DECISIONS. Gặp lỗi > 30 phút → prompt 07 | BUILD_LOG, DECISIONS, journal/bugs |
| Cuối buổi | 3 dòng daily: làm gì, kẹt gì, mai làm gì | journal/daily |
| Xong project | Tự viết RETRO → prompt 03, 04 → prompt 05 (quiz) → tick "Định nghĩa xong" trong AGENTS.md → cập nhật progress.md | RETRO, modules, MAP, glossary |

Nguyên tắc: **ghi trong lúc làm, không ghi sau**. Lý do bạn phải backfill 5 project bây giờ chính là vì trước đây ghi sau.

---

## 9. P06 và P07

Tôi chưa đọc được đề, nên chỉ nêu những gì chắc chắn từ repo P05:

- **Đầu vào đã có** (theo `docs/` của P05): collection `glamira_raw` (41.432.473 event, khóa `_id` gốc, index trên `collection`, `time_stamp`, `ip`, `product_id`), `ip_geo` (một dòng cho mỗi IP, nối qua `glamira_raw.ip`), `products` (một document cho mỗi product id trong seed), và bản CSV của hai collection sau.
- **P05 đã tự ghi phần để lại cho sau:** `scope_confirmation.md` mục "Ngoài scope P05" liệt kê GCS, Cloud Function, BigQuery, dbt, Looker; hai câu hỏi dashboard đã chốt (doanh thu Đức vs Pháp; nhẫn vs vòng tay) và các giả định (doanh thu = tổng `cart_products[].price` của `checkout_success`, tách theo `currency`, không tự quy đổi tỉ giá). Dán nguyên phần này vào đầu README của P06 và P07.
- **Việc phải xong ở P05 trước khi sang P06:** crawl đủ seed (chạy `infra/gcp/resume.sh` để xem còn bao nhiêu), `product-status` khớp, viết README.
- **Một quyết định cần ghi vào DECISIONS của P06 ngay ngày đầu:** P06 là thư mục riêng dùng lại dữ liệu P05, hay viết tiếp trong `p05-glamira`? Mặc định nên tách thư mục (mỗi project nộp riêng, doc riêng) và chỉ dùng chung *dữ liệu*, không import code chéo thư mục. Xác nhận lại sau khi đọc đề.

Khởi động bằng `prompts/06-start-new-project.md` sau khi đã dán đề vào `roadmap/briefs/p06.md`.

---

## 10. Danh sách việc cần làm

- [ ] Bước 1: tạo repo + khung thư mục
- [ ] Bước 3: `git subtree add` × 5; chuyển `.env`, `gcp.env`, `data/` của P05 sang
- [ ] Bước 4: dọn 8 chỗ lệch (ưu tiên: điền `results_snapshot.md` của P04; tìm lại các file ghi chú tiếng Việt của P02, P04)
- [ ] Bước 5: dán AGENTS.md, CLAUDE.md, template, prompts, MAP.md, bảng 6.2 và 6.3
- [ ] Bước 6: dán đề Notion P03–P07 vào `roadmap/briefs/`
- [ ] Hoàn tất P05: crawl đủ, viết README
- [ ] Backfill P05 → P02 (điền số đo vào Mục 7, trả lời 3 câu tự kiểm) → P03 + P04 → P01
- [ ] Viết 2 note khái niệm đầu tiên: `rerun-safety.md` và `crawling.md` (từ hai đoạn cuối Mục 6.3)
- [ ] Bắt đầu P06 bằng prompt 06