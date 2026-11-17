# Meeting Notes Sau Buổi Review Với Coach

## 1. Mục tiêu của project

Đây không phải là một project chỉ cần "code chạy được".  
Mục tiêu là làm theo hướng gần với **production-ready** nhất có thể:

- có tư duy kiểm soát chất lượng dữ liệu
- có quy trình xử lý lỗi và retry
- có khả năng resume khi job bị chết
- có báo cáo đủ rõ để biết dữ liệu có thật sự dùng được hay không

Nói cách khác, logic bài toán thì đơn giản, nhưng phần thực chiến lại rất nhiều việc.

## 2. Tư duy tổng quát Coach nhấn mạnh

### Data first, không phải code first

Điều quan trọng nhất không phải là code async hay code "xịn", mà là:

- cuối cùng có bao nhiêu dữ liệu dùng được
- dữ liệu đó có đúng không
- phần bị fail đã được xử lý tiếp hay chưa

Ví dụ:

- crawl được `90%` chưa phải là đủ tốt
- `10%` fail trên `200000` sản phẩm là khoảng `20000` record, cực kỳ lớn

### 100% thành công cũng cần nghi ngờ

Trong các bài toán dữ liệu lớn, kết quả quá đẹp cũng đáng nghi:

- có thể input bị trùng
- có thể output bị duplicate
- có thể lấy nhầm dữ liệu nhưng vẫn tưởng là đúng

Vì vậy:

- dữ liệu đã thành công vẫn phải validate
- dữ liệu fail cũng phải retry và phân loại lại

## 3. Những câu hỏi phải trả lời trước khi viết code

1. File input có sạch không?
2. Có duplicate `product_id` không?
3. Có dòng rỗng hoặc lỗi format không?
4. Sẽ crawl theo đồng bộ, bất đồng bộ, hay multiprocessing?
5. Sẽ lưu file theo batch như thế nào?
6. Nếu job chết giữa chừng thì resume ra sao?
7. Nếu có `10%` lỗi thì pipeline retry sẽ chạy như thế nào?
8. Sau khi crawl xong, sẽ validate output bằng cách nào?

## 4. Những rủi ro chính của project

### Rủi ro 1: Input sai hoặc duplicate

Nếu file `200000 product_id` có vấn đề mà không kiểm tra trước:

- output có thể bị trùng
- thống kê thành công có thể bị ảo
- tỷ lệ `90% success` có thể không còn ý nghĩa

### Rủi ro 2: Async quá nhanh

Async không xấu, nhưng dùng thiếu kiểm soát thì rất nguy hiểm:

- dễ bị `403`, `429`, timeout
- dễ tạo false negative
- khó checkpoint/resume hơn đồng bộ

### Rủi ro 3: Chỉ nhìn vào phần fail

Không được mặc định:

- success = đúng
- fail = thật sự fail

Phải luôn tự hỏi:

- dữ liệu đã lấy được có bị trùng không?
- có field nào rỗng bất thường không?
- có đang lấy nhầm nhưng vẫn tưởng là đúng không?

### Rủi ro 4: Không có checkpoint

Nếu job chạy hàng giờ mà bị chết:

- không thể chấp nhận việc chạy lại từ đầu
- phải có checkpoint hoặc ít nhất là cơ chế resume theo batch

## 5. Kinh nghiệm thực chiến rút ra từ meeting

### Chia batch và ghi file ngay

Không nên nhét tất cả `200000` product details vào một list rồi mới xử lý tiếp.

Nên làm:

- lấy theo batch
- ghi ra file ngay
- giải phóng bộ nhớ
- xử lý tiếp batch sau

### Retry cần có 2 tầng

1. Retry ngay trong lúc fetch từng product  
2. Retry pipeline riêng cho toàn bộ danh sách failed IDs sau khi crawl xong

Đợt retry thứ hai nên chạy:

- chậm hơn
- tuần tự từng ID hoặc gần như tuần tự
- ưu tiên độ đúng hơn tốc độ

### Validate output là bắt buộc

Ít nhất phải kiểm tra:

- duplicate output IDs
- field bắt buộc có bị thiếu không
- `description` có rỗng bất thường không
- `images` có rỗng bất thường không

## 6. Những việc project cần có theo tinh thần Coach
 
- validate input CSV
- deduplicate input IDs
- main crawl pipeline
- retry per request
- retry pipeline cho failed IDs
- checkpoint / resume theo batch
- auto restart khi process die
- output validation
- summary cuối job
- unit tests cho phần quan trọng

## 7. Kết luận

Buổi meeting không chỉ nói về cách crawl dữ liệu, mà đang kéo project từ mức:

- bài tập gọi API

lên mức:

- một pipeline dữ liệu thực tế có thể giải thích, đo đạc, resume và validate

Đó là giá trị lớn nhất của buổi review này.
