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
