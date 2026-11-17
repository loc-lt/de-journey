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