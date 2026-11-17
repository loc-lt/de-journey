# Pipeline Xử Lý Dữ Liệu Của Project

## 1. Tổng quan pipeline

Pipeline mới của project đi theo thứ tự này:

1. Validate input CSV
2. Deduplicate input IDs
3. Main crawl theo batch
4. Ghi output và failed records theo batch
5. Cập nhật checkpoint sau mỗi batch
6. Chạy retry pipeline cho failed IDs
7. Validate output cuối cùng
8. Ghi summary và các report

## 2. Stage 1: Input validation

Mục tiêu:

- không tin ngay file đầu vào
- kiểm tra số dòng hợp lệ
- phát hiện duplicate
- phát hiện giá trị lỗi format

Output:

- `data/output/input_validation_report.json`

Ý nghĩa:

- giúp biết chính xác trước khi crawl là mình đang có bao nhiêu `product_id` dùng được

## 3. Stage 2: Main crawl

Mục tiêu:

- gọi API lấy product details
- giới hạn concurrency bằng semaphore
- retry ngay khi gặp lỗi tạm thời

Đặc điểm:

- chạy theo batch
- mỗi batch ghi ra file ngay
- không giữ toàn bộ kết quả trong RAM

Output:

- `data/output/products_00001.json`
- `data/output/products_00002.json`
- ...

## 4. Stage 3: Failed records

Mục tiêu:

- không chỉ lưu `product_id` fail
- lưu thêm thông tin lỗi để phân tích sau

Output:

- `data/output/_failed/failed_00001.json`
- ...

Ví dụ mỗi record lỗi gồm:

- `product_id`
- `status_code`
- `error`
- `elapsed_s`

## 5. Stage 4: Checkpoint

Mục tiêu:

- sau mỗi batch hoàn thành thì lưu trạng thái
- nếu job chết giữa chừng thì có thể chạy lại mà không làm lại từ đầu

Output:

- `data/output/checkpoint.json`

## 6. Stage 5: Retry pipeline

Mục tiêu:

- gom toàn bộ failed IDs
- retry lại theo kiểu tuần tự từng ID
- ưu tiên độ đúng hơn tốc độ

Output:

- `data/output/retry/recovered_00001.json`
- `data/output/retry/still_failed.json`
- `data/output/retry/retry_summary.json`
- `data/output/retry/confirmed_404.json`
- `data/output/retry/still_unstable.json`

Retry pipeline mới không chỉ retry một lần, mà:

- recheck failed IDs qua nhiều vòng
- chạy tuần tự từng ID
- có delay giữa các vòng
- phân loại nhóm lỗi cuối cùng thành:
  - `confirmed_404`
  - `still_unstable`

## 7. Stage 6: Output validation

Mục tiêu:

- kiểm tra output sau khi crawl và retry
- tìm duplicate
- đếm field rỗng hoặc thiếu

Output:

- `data/output/output_validation_report.json`

## 8. Stage 7: Final reporting

Mục tiêu:

- tổng hợp toàn bộ job thành một báo cáo cuối

Output:

- `data/output/summary.json`

Báo cáo nên trả lời được:

- tổng input là bao nhiêu
- đã xử lý bao nhiêu
- thành công bao nhiêu
- lỗi bao nhiêu
- retry cứu được bao nhiêu
- output có duplicate không
- nếu process bị die thì có tự restart và resume được không

## 9. Tại sao module Computer Network Basics lại dạy REST API và Pub/Sub

Vì network không chỉ là IP, port hay ping.  
Trong thực tế, engineer thường gặp network qua các mô hình giao tiếp giữa hệ thống.

### REST API

REST API là mô hình giao tiếp theo kiểu:

- client gửi request
- server trả response

Project này dùng đúng mô hình đó:

- Python crawler là client
- API Tiki là server
- response là JSON product detail

Cho nên phần REST API là **rất liên quan trực tiếp** tới project.

### Pub/Sub là gì

Pub/Sub là viết tắt của **Publish / Subscribe**.

Đây là mô hình giao tiếp mà:

- một bên publish message
- một hoặc nhiều bên subscribe để nhận message đó

Ví dụ:

- service A phát sự kiện "đơn hàng đã tạo"
- service B và C subscribe để xử lý tiếp

Các hệ thống hay dùng:

- Kafka
- RabbitMQ
- Google Pub/Sub
- Redis Streams

### Project này có dùng Pub/Sub không

Hiện tại project này **không dùng Pub/Sub**.

Project của bạn đang là:

- batch pipeline
- request/response
- pull dữ liệu từ REST API

Chưa có:

- event broker
- message queue
- publisher/subscriber thực thụ

### Vậy tại sao Coach vẫn dạy Pub/Sub

Vì về mặt tư duy hệ thống, Pub/Sub rất quan trọng khi làm backend/data:

- giúp hiểu cách hệ thống giao tiếp bất đồng bộ
- giúp hiểu event-driven architecture
- giúp mở rộng từ request/response sang pipeline lớn hơn

Nếu sau này project lớn lên, bạn có thể dùng Pub/Sub cho các bước như:

- publish batch cần retry
- publish event khi một batch crawl xong
- tách khâu crawl, normalize, validate thành nhiều worker

Nhưng ở phiên bản hiện tại, project **chưa cần Pub/Sub**.

## 10. Kết luận

Pipeline mới giúp project đi đúng mindset:

- không chỉ crawl cho ra file
- mà phải biết input có sạch không
- fail đã retry chưa
- output có đáng tin chưa
- job chết thì có resume được không

Đó mới là hướng làm data pipeline gần production-ready.
