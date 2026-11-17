# Checklist khóa DE Batching

Nguồn: `roadmap/checklist.xlsx`, sheet Checklist Roadmap và Tasks Detail. Không gồm sheet Guideline và Performance Control.

Mỗi module một bảng. Tên module lấy từ cột Module của Checklist Roadmap, vì Tasks Detail không có dòng tiêu đề cho SQL Advanced. Cột Status là cột Status trên Checklist Roadmap: `1` = đã tick, `0` = chưa tick.

Đề thực tế của Project 03 và Project 04 nằm ở `roadmap/briefs/p03.md` và `roadmap/briefs/p04.md`, và khác mô tả trong checklist. Checklist bảo Project 03 làm lại Project 01 bằng Pandas, và Project 04 theo đề Bee Movies. Project đã nộp là bộ sinh dữ liệu bán hàng (P03) và đơn hàng trên cùng DB đó (P04).

## Linux & Bash Fundamentals

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 1 | Setup Ubuntu & Tools | DoD: Cài đặt hệ điều hành Ubuntu 22.04 và các công cụ phục vụ cho việc lập trình (IDE, Telegram, Zoom, ...) | Có thể cài đặt Song song với Windows hoặc qua Máy ảo (VMWare, VirtualBox,..). Nếu đang sử dụng Macbook thì chỉ cần cài đặt các Tools để làm việc | 1 |
| 2 | File System Navigation & Operation | DoD: Học hiểu các khái niệm, hoàn thành Exercises và Quiz tại đây: https://linuxjourney.com/lesson/the-shell | Note lại các khái niệm hoặc những keyword chưa thực sự hiểu rõ, tìm kiếm thêm thông tin trên Google hoặc nhắn lên nhóm trao đổi cùng với Team và các Coach. Lưu ý: Thực hành trên Terminal của Ubuntu | 1 |
| 3 | File Permissions | DoD: Học hiểu các khái niệm, hoàn thành Exercises và Quiz tại đây: https://linuxjourney.com/lesson/file-permissions |  | 1 |
| 4 | Text Processing | DoD: Học hiểu các khái niệm, hoàn thành Exercises và Quiz tại đây: https://linuxjourney.com/lesson/stdout-standard-out-redirect | Học thêm các kiến thức nâng cao hơn về Text Processing tại đây: https://linuxjourney.com/lesson/regular-expressions-regex<br>https://www.theunixschool.com/p/awk-sed.html | 1 |
| 5 | System Monitoring | DoD: Đọc hiểu các khái niệm cơ bản về giám sát hệ thống Linux tại đây: https://www.digitalocean.com/community/tutorials/process-management-in-linux | Lưu ý: Cần dừng lại ở mức độ biết được các khái niệm và ý nghĩa cơ bản, take note lại các từ khoá để tìm hiểu thêm về sau. Nắm rõ các command cơ bản:<br>  - Process management: ps, top, htop<br>  - Resource monitoring: free, df, du<br>  - Network tools: netstat, ss, lsof<br>Chi tiết hơn thì có thể tham khảo tại đây: https://linuxjourney.com/lesson/monitor-processes-ps-command | 1 |
| 6 | Bash Basics | DoD: Học và hoàn thành khoá học sau: https://www.codecademy.com/learn/introduction-to-linux-bash-scripting | Lưu ý: Chỉ cần học những module free | 1 |
| 7 | Automation | DoD: Học về cronjob và thực hành sử dụng: https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804 |  | 1 |
| 8 | Project 01 | DoD: Sử dụng bash commandline hoàn thành project theo yêu cầu sau và report lại Coach sau khi xong https://unigap-tech-coaching.notion.site/Linux-CMD-Project-11e04bc026004c3298e85bba8919630a?pvs=4 | Yêu cầu tối thiểu: hoàn thành các yêu cầu từ 1 đến 5. Nếu không hoàn thành các yêu cầu 6 và 7, hãy đưa ra lý do trong form Project submit. <br>Link submit project sau khi hoàn thành: https://docs.google.com/forms/d/1vT9GNL379zI1guOMhVpeqz0EV1GWQsTuIm34n6zsZJA/edit | 1 |

## Computer Network Basics

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 9 | SSH in action | DoD:  Setup 2 thiết bị, một thiết bị là server, một thiết bị là client, hoàn thành các yêu cầu sau:<br>1. Setup để client có thể truy cập đến server qua ssh sử dụng username - password<br>2. Setup để client có thể truy cập đến server qua ssh sử dụng ssh_key<br>3. Thay đổi cấu hình để client ssh được tới server sử dụng port 2222<br>4. SCP file từ lên server | Tham khảo:<br>Understanding the SSH Encryption and Connection Process \| DigitalOcean<br>https://www.cyberciti.biz/faq/how-to-install-ssh-on-ubuntu-linux-using-apt-get/ | 1 |
| 10 | FTP & SFTP in action | DoD: Setup 2 thiết bị, một thiết bị là server, một thiết bị là client. Setup để client có thể upload/download file trên server qua ftp và sftp | Tham khảo:<br>File Transfer Protocol (FTP) - GeeksforGeeks<br>https://www.digitalocean.com/community/tutorials/how-to-use-sftp-to-securely-transfer-files-with-a-remote-server | 1 |
| 11 | REST API Common Practices | DoD: Học các khái niệm về REST API và HTTP theo link sau: https://rapidapi.com/learn/rest#what-is-an-api | Yêu cầu học hết các mục từ 1-> 15 | 1 |
| 12 | Project 02 | DoD: Sử dụng code Python, tải về thông tin của 200k sản phẩm (list product id bên dưới) của Tiki và lưu thành các file .json. Mỗi file có thông tin của khoảng 1000 sản phẩm. Các thông in cần lấy bao gồm: id, name, url_key, price, description, images url. Yêu cầu chuẩn hoá nội dung trong "description" và tìm phương án rút ngắn thời gian lấy dữ liệu.<br>- List product_id: https://1drv.ms/u/s!AukvlU4z92FZgp4xIlzQ4giHVa5Lpw?e=qDXctn<br>- API get product detail: https://api.tiki.vn/product-detail/api/v1/products/138083218 | Lưu ý: Cần lưu lại những sản phẩm bị lỗi và lý do lỗi.<br>Tổng quan về json có thể tham khảo tại đây: https://www.youtube.com/watch?v=iiADhChRriM<br>Link submit project sau khi hoàn thành:  https://docs.google.com/forms/d/1iIJavuPT7haom8NQSGiBwD-d8nMKeAGCBtXvZEEtH_A/edit | 1 |

## Python for Data

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 13 | Setting up Pycharm | DoD: Làm quen với Pycharm với việc tạo project đầu tiên, debug và test ứng dụng<br>- https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html<br>- https://www.jetbrains.com/help/pycharm/debugging-your-first-python-application.html<br>- https://www.jetbrains.com/help/pycharm/testing-your-first-python-application.html | Bạn có thể sử dụng VSCode hoặc bất kỳ IDE nào khác ngoài Pycharm | 1 |
| 14 | Setting up Git with Pycharm | DoD: Thực thi theo hướng dẫn sau để có repository trên github https://www.youtube.com/watch?v=8ZEssR8VTKo | Cần dành thêm thời gian về sau để tìm hiểu và làm chủ về GIT cũng như cách làm việc với team qua GIT. Tham khảo:<br>- https://www.codecademy.com/learn/learn-git-introduction<br>- https://www.codecademy.com/learn/learn-git-branching-and-collaboration | 1 |
| 15 | Python PostgreSQL | DoD: Thực hành Python thao tác với Postgres DB theo hướng dẫn.<br>https://www.postgresqltutorial.com/postgresql-python/ | Lưu ý: Thực thi toàn bộ hướng dẫn và các yêu cầu trên Pycharm, push code lên github và gửi cho coach | 1 |
| 16 | Lab 01 | DoD: Sử dụng Python, đọc toàn bộ dữ liệu Tiki từ các file ở Project 02 rồi ghi thông tin vào Postgres DB | Lưu ý: Push code lên Github và gửi link public cho coach | 1 |
| 17 | Python Exceptions: An Introduction | DoD: Đọc và thực hành theo nội dung sau: https://realpython.com/python-exceptions/ |  | 1 |
| 18 | Lab 02 | DoD: Bổ sung thêm exception cho Lab 01 khi đọc dữ liệu từ file và khi thao tác với Database | Tham khảo thêm về File Handling: https://www.w3schools.com/python/python_file_handling.asp<br>Lưu ý: Push code lên Github và gửi link public cho coach | 1 |
| 19 | Pandas Tutorial | DoD: Học và làm theo toàn bộ các yêu cầu về Pandas Tutorial và Exercises https://www.w3schools.com/python/pandas/default.asp |  | 1 |
| 20 | Project 03 | DoD: Sử dụng Pandas, thực thi lại toàn bộ các yêu cầu của Project 01 (Project Linux CMD) | Link submit project sau khi hoàn thành:<br>https://docs.google.com/forms/d/1G8PWFpZ1Ltf33CyX9hJAii6Y_7ng7qTMNPAv0qmXFMY/edit | 1 |

## SQL Advanced

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 21 | Window function core concept | DoD: Học và thực hành các khái niệm của Window function: rank, partition, named window, frames, lead, lag | Overview of SQL RANK functions<br>Using Partition By SQL Clause - Shiksha Online<br>MySQL 8.4 Reference Manual :: 14.20.4 Named Windows<br>https://www.vertica.com/docs/9.2.x/HTML/Content/Authoring/SQLReferenceManual/Functions/Analytic/window_frame_clause.htm?origin_team=T02V9CHFH<br>The LAG Function and the LEAD Function in SQL \| LearnSQL.com | 1 |
| 22 | Window function Exercise | DoD: Hoàn thành bài tập sau và gửi coach đánh giá https://unigap-tech-coaching.notion.site/Window-function-650d5d8260994f799d57ba5280daddea?pvs=4 | Hãy kết hợp việc tìm hiểu thêm nhiều nguồn tài liệu khác để hiểu được các khái niệm một cách cụ thể nhất và biết được khi nào cần phải sử dụng những phương thức nào để giải quyết vấn đề | 1 |
| 23 | Case when statement | DoD: Thực thi theo hướng dẫn sau để thực hành về SQL Case https://mode.com/sql-tutorial/sql-case |  | 1 |
| 24 | UDFs | DoD: Thực hành UDFs theo hướng dẫn ở link sau. Đảm bảo nắm được các bước triển khai UDFs https://www.geeksforgeeks.org/postgresql-user-defined-functions/ |  | 1 |
| 25 | Stored Procedure | DoD: Tạo store procedure trên PostgresDB mà bạn đã setup https://www.w3schools.com/sql/sql_stored_procedures.asp |  | 1 |
| 26 | Cursors | DoD: Tìm hiểu và thực hành về Cursor trong SQL https://www.geeksforgeeks.org/what-is-cursor-in-sql/ |  | 0 |
| 27 | Exercise | DoD: Hoàn thành các câu hỏi trong link notion sau https://unigap-tech-coaching.notion.site/SQL-Exercises-04727d5678da477c856db3f589c0856d?pvs=4 |  | 0 |
| 28 | Database Indexing | DoD: Tạo Database Indexing và hiểu các khái niệm liên quan đến DB Indexing (clustered & non clustered index) | SQL - Indexes<br>Difference Between Clustered and Non-Clustered Index - GeeksforGeeks | 0 |
| 29 | Order of Query Execution | DoD: Học và hiểu được thứ tự thực hiện các lệnh SQL | Order of Execution in SQL - Shiksha Online | 0 |
| 30 | Join & nested query | DoD: Phân biệt Join và Nest Query trong DBMS | Join operation Vs Nested query in DBMS - GeeksforGeeks | 0 |
| 31 | Exercise | DoD: Hoàn thành các câu hỏi trong link notion sau https://unigap-tech-coaching.notion.site/SQL-Advance-2-a520a098e790467c84be1bb109da3774?pvs=4 |  | 0 |
| 32 | SQL (Advanced) Skills Certification | DoD: Lấy chứng chỉ SQL advanced trên HackerRank | SQL (Advanced) Skills Certification Test | 0 |
| 33 | Project 04 | DoD: Thực hiện project theo các yêu cầu được mô tả https://unigap-tech-coaching.notion.site/Project-Bee-Movies-bf7695ac1a3541e0964a43e3faf12519?pvs=4 | Link submit project sau khi hoàn thành: https://docs.google.com/forms/d/1YDMMBjHKhNkotgGL_xobeA5mw3KQm4MXDJArMVoa8l4/edit | 0 |

## GCP data pipeline

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 34 | GCP Overview | DoD: Đăng ký Credit free của GCP. Tìm hiểu overview về GCP và hoàn thành lab "A Tour of Google Cloud Hands-on Labs" trên https://www.cloudskillsboost.google/ | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm "A Tour of Google Cloud Hands-on Labs". Sau đó thực thi theo yêu cầu | 0 |
| 35 | Compute Engine | DoD: Tìm hiểu về Compute Engine và hoàn thành lab trên <br>https://www.cloudskillsboost.google/:<br>1. Create a Virtual Machine<br>2. Compute Engine: Qwik Start - Windows<br>3. Creating a Persistent Disk | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm theo tên các lab. Sau đó thực thi theo yêu cầu | 0 |
| 36 | VPC Network | DoD: Tìm hiểu về VPC và thực hành lab sau: <br>VPC Networking Fundamentals | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm theo tên các lab. Sau đó thực thi theo yêu cầu | 0 |
| 37 | Google Cloud Storage | DoD: Tìm hiểu về GCS và thực hành lab sau:<br>Cloud Storage: Qwik Start - Cloud Console<br>Ô Task ID ở Tasks Detail bị merge (B47:B49). ID này lấy theo tên task trên Checklist Roadmap. | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm theo tên các lab. Sau đó thực thi theo yêu cầu | 0 |
| 38 | Cloud Function | DoD: Tìm hiểu về Cloud Function và thực hành lab sau:<br> Cloud Run Functions: Qwik Start - Console<br>Ô Task ID ở Tasks Detail bị merge (B47:B49). ID này lấy theo tên task trên Checklist Roadmap. | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm theo tên các lab. Sau đó thực thi theo yêu cầu | 0 |
| 39 | Google BigQuery | DoD: Tìm hiểu về BigQuery và thực hành lab sau:<br>Using BigQuery in the Google Cloud Console | Truy cập vào https://www.cloudskillsboost.google/ rồi tìm kiếm theo tên các lab. Sau đó thực thi theo yêu cầu | 0 |
| 40 | Data Storage | DoD: Tìm hiểu về những định dạng dữ liệu có thể lưu trữ trên Data Lake sử dụng Cloud Storage và những lưu ý khi lưu trữ những dữ liệu này | Tham khảo: https://cloud.google.com/storage/docs/resources | 0 |
| 41 | Cost-effectiveness | DoD: Tìm hiểu về phương cách tối ưu chi phí hiệu quả với Data Lake sử dụng GCS |  | 0 |
| 42 | Data Governance and Management | DoD: Tìm hiểu về Data Governance, và đưa ra các phương án quản trị và quản lý dữ liệu hiệu quả. Các công việc cần làm để đảm bảo dữ liệu được chính xác, đúng đắn và đầy đủ là gì? |  | 0 |
| 43 | Project 05 | DoD: Hoàn thành project sau: https://unigap-tech-coaching.notion.site/Project-05-Data-Collection-Storage-Foundation-fd50b5b264a04576b0def7c0ba1f48af?pvs=4 | Link submit project: https://docs.google.com/forms/d/e/1FAIpQLScddB5U26TFzwT0YGvbO57RFtJSx8SX_nu5qjL92xgdkomHRg/viewform?usp=sharing | 0 (Checklist Roadmap ghi Task ID 33 cho cùng tên task) |
| 44 | General Data Architect | DoD: Tìm hiểu Data Architect concept thông qua ví dụ trực quan | What is a Data Architecture? Modern Data Architectures Explained - YouTube | 0 (Checklist Roadmap ghi Task ID 43 cho cùng tên task) |
| 45 | Data Warehouse Understanding | DoD: Tìm hiểu về Data Warehouse, lý do cần có Warehouse và sự khác biệt so với khái niệm Database thông thường là gì? | Understanding The Data Warehouse \| The Analytics Setup Guidebook | 0 (Checklist Roadmap ghi Task ID 44 cho cùng tên task) |
| 46 | Dimensional Warehouse Design - Data Modeling | DoD: Tìm hiểu về Data Modeling và cách cách thiết kế mô hình dữ liệu trong thực tế | Data Modeling Layer & Concepts \| The Analytics Setup Guidebook | 0 (Checklist Roadmap ghi Task ID 45 cho cùng tên task) |
| 47 | Dimensional Warehouse Design - Dimensional Modeling | DoD: Tìm hiểu về Dimensional Modeling và cách cách thiết kế mô hình dữ liệu | Dimensional Modeling - YouTube | 0 (Checklist Roadmap ghi Task ID 46 cho cùng tên task) |
| 48 | Data processing in Warehouse | DoD: Tìm hiểu khái niệm về ETL và ELT cách xử lý dữ liệu trong DataWarehouse. Best practices khi sử dụng BigQuery cho Data Warehouse? | ETL vs. ELT - What's the big deal? \| The Analytics Setup Guidebook<br>Transforming Data in the ELT paradigm \| The Analytics Setup Guidebook<br>Data Warehousing With BigQuery: Best Practices (Cloud Next '19) - YouTube | 0 (Checklist Roadmap ghi Task ID 47 cho cùng tên task) |
| 49 | Data Lake & Data Warehouse Best Practices | DoD: Các team sẽ tổng hợp và trình bày về Data Lake & Data Warehouse | Note: Toàn bộ những kiến thức tìm hiểu về Data Lake và Data Warehouse sử dụng công cụ trên trên nền tảng GCP | 0 (Checklist Roadmap ghi Task ID 48 cho cùng tên task) |
| 50 | Project 06 | Hoàn thành project sau: https://unigap-tech-coaching.notion.site/Project-06-Data-Pipeline-Storage-a36cf22baa9e4628bddfaab513011eef?pvs=4 | Link submit project:<br>https://docs.google.com/forms/d/e/1FAIpQLSep9VN5nbq3KLeSNd3ac4gSffU3Qz0_6ZT81C_ZoRW0qlRxAQ/viewform?usp=sharing | 0 (Checklist Roadmap ghi Task ID 33 cho cùng tên task) |
| 51 | Modernizing Data Lakes and Data Warehouses | DoD: Tìm hiểu về cách Xây dựng Data Lake và Data Warehouse trên GCP, thực hành các bài labs https://www.cloudskillsboost.google/course_templates/54 |  | 0 (Checklist Roadmap ghi Task ID 49 cho cùng tên task) |

## DBT

| Task ID | Task | DoD | Guideline | Status |
|---|---|---|---|---|
| 52 | Visualize data with Looker | DoD: Học cách Visualize data cơ bản với Looker https://www.cloudskillsboost.google/paths/28/course_templates/323 |  | 0 (Checklist Roadmap ghi Task ID 50 cho cùng tên task) |
| 53 | DBT Fundamentals | DoD: Hoàn thành course sau về kiến thức nền tảng DBT https://learn.getdbt.com/courses/dbt-fundamentals |  | 0 (Checklist Roadmap ghi Task ID 51 cho cùng tên task) |
| 54 | DBT Unit Testing | DoD: Hoàn thành course sau về Unit Testing: https://learn.getdbt.com/courses/unit-testing |  | không có trên sheet Checklist Roadmap |
| 55 | DBT with BigQuery | DoD: Học course ứng dụng DBT với Google BigQuery https://learn.getdbt.com/learn/course/dbt-cloud-and-bigquery-for-developers/join-a-project-in-dbt-cloud-and-bigquery-15min/getting-started?page=7 |  | không có trên sheet Checklist Roadmap |
| 56 | Final Project | DoD: Hoàn thành project sau: https://unigap-tech-coaching.notion.site/Project-07-Data-Transformation-Visualization-d069859fe2d742a8a41cdac670a84c05?pvs=4 | Link submit project: https://docs.google.com/forms/d/e/1FAIpQLSfatTJNnTo2BsXEe_AdW9Y4Jy7JqN1Ven2TytndzOQzOx3V3A/viewform?usp=sharing | không có trên sheet Checklist Roadmap |
