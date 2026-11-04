# SQL Injection Attack Simulator

## Kế hoạch xây dựng dự án mô phỏng SQL Injection

> **Mục tiêu:** Xây dựng một ứng dụng web nhỏ để học và minh họa cách lỗ
> hổng SQL Injection có thể ảnh hưởng đến chức năng đăng nhập và dữ liệu
> trong một cơ sở dữ liệu thử nghiệm, đồng thời so sánh cách triển khai
> không an toàn với cách triển khai an toàn.
>
> **Phạm vi an toàn:** Dự án chỉ chạy trên dữ liệu giả lập do người phát
> triển tạo. Không kiểm thử website, máy chủ hoặc cơ sở dữ liệu của bên
> thứ ba. Không triển khai chức năng tự động dò quét hay tấn công mục
> tiêu bên ngoài.

------------------------------------------------------------------------

## 1. Tổng quan dự án

### 1.1. Tên dự án

-   **English:** SQL Injection Attack Simulator
-   **Vietnamese:** Chương trình mô phỏng tấn công SQL Injection và biện
    pháp phòng chống

### 1.2. Mô tả ngắn

Ứng dụng cung cấp một trang đăng nhập thử nghiệm và một khu vực quản trị
dữ liệu giả lập. Người học có thể chuyển đổi giữa hai chế độ:

-   **Vulnerable Mode:** Minh họa một cách viết truy vấn SQL không an
    toàn trong môi trường local.
-   **Secure Mode:** Sử dụng truy vấn tham số hóa (parameterized queries
    / prepared statements) để ngăn dữ liệu đầu vào bị diễn giải thành
    một phần câu lệnh SQL.

Ứng dụng hiển thị kết quả đăng nhập, thông báo phát hiện đầu vào bất
thường và nhật ký sự kiện để người học quan sát sự khác biệt. Chế độ dễ
bị tổn thương phải được giới hạn trong ứng dụng local, với database giả
lập và dữ liệu không nhạy cảm.

### 1.3. Mục tiêu học tập

Sau khi hoàn thành, người phát triển có thể:

1.  Giải thích SQL Injection là gì và vì sao nó xảy ra.
2.  Nhận biết rủi ro khi ghép trực tiếp dữ liệu đầu vào vào câu truy vấn
    SQL.
3.  Phân biệt truy vấn SQL không an toàn và truy vấn tham số hóa.
4.  Minh họa ảnh hưởng của lỗ hổng trên database giả lập.
5.  Áp dụng một số biện pháp phòng chống cơ bản.
6.  Viết README, hướng dẫn cài đặt, kiểm thử và ghi nhận giới hạn của dự
    án.

------------------------------------------------------------------------

## 2. Phạm vi phiên bản đầu tiên (MVP)

Giữ dự án nhỏ, hoàn thành các chức năng cốt lõi trước. Không cần tài
khoản đăng ký, phân quyền phức tạp, triển khai cloud hoặc nhiều loại
database.

### Chức năng bắt buộc

  -----------------------------------------------------------------------
  ID                      Chức năng               Mô tả
  ----------------------- ----------------------- -----------------------
  F01                     Trang giới thiệu        Giới thiệu SQL
                                                  Injection, mục tiêu và
                                                  cảnh báo phạm vi thử
                                                  nghiệm

  F02                     Login Simulator         Form nhập username và
                                                  password

  F03                     Chọn chế độ             Chuyển giữa Vulnerable
                                                  Mode và Secure Mode

  F04                     Kết quả mô phỏng        Hiển thị đăng nhập
                                                  thành công/thất bại và
                                                  giải thích kết quả

  F05                     Database Viewer         Hiển thị danh sách tài
                                                  khoản giả lập, chỉ đọc

  F06                     Attack/Event Logs       Ghi lại thời gian, chế
                                                  độ, loại sự kiện và kết
                                                  quả

  F07                     Security Explanation    Giải thích vì sao chế
                                                  độ an toàn ngăn được
                                                  lỗi

  F08                     Reset Demo Data         Khôi phục dữ liệu mẫu
                                                  ban đầu
  -----------------------------------------------------------------------

### Không làm trong MVP

-   Không tấn công website hoặc máy chủ bên ngoài.
-   Không có chức năng tự động quét website.
-   Không thu thập mật khẩu thật hoặc dữ liệu cá nhân.
-   Không thực hiện đánh cắp dữ liệu, duy trì truy cập hay phá hoại hệ
    thống.
-   Không cần đăng ký/đăng nhập người dùng thật.
-   Không cần Docker, cloud hoặc hệ thống phân tán ở phiên bản đầu.

------------------------------------------------------------------------

## 3. Công nghệ sử dụng

  -----------------------------------------------------------------------
  Thành phần              Công nghệ               Lý do
  ----------------------- ----------------------- -----------------------
  Ngôn ngữ                Python 3                Dễ học, phù hợp làm
                                                  prototype

  Backend                 Flask                   Nhẹ, dễ tạo route

  Database                SQLite                  Không cần cài database
                                                  server

  Frontend                HTML, CSS               Đủ cho giao diện demo

  Giao diện tương tác     JavaScript cơ bản       Gửi form và cập nhật
                                                  kết quả

  Quản lý mã nguồn        Git + GitHub            Theo dõi tiến độ và
                                                  công khai project

  Kiểm thử                pytest                  Viết test cho các chức
                                                  năng chính
  -----------------------------------------------------------------------

**Khuyến nghị:** Không cần React/Vue ở phiên bản đầu. Dùng Flask render
template để giảm độ phức tạp.

------------------------------------------------------------------------

## 4. Thiết kế chức năng và luồng hoạt động

### 4.1. Trang chính

Nội dung:

-   Tên dự án và mô tả ngắn.
-   SQL Injection là gì?
-   Nút mở Login Simulator.
-   Cảnh báo: chỉ sử dụng trong môi trường local và dữ liệu giả lập.

### 4.2. Login Simulator

Người dùng nhập username và password, sau đó chọn chế độ.

**Vulnerable Mode:**

-   Backend gọi một hàm mô phỏng truy vấn không an toàn.
-   Có thể sử dụng một kịch bản demo cố định, được định nghĩa sẵn trong
    code, để minh họa việc dữ liệu đầu vào làm thay đổi logic xác thực.
-   Không cho người dùng gửi SQL tùy ý hoặc thực thi câu lệnh tùy ý.
-   Hiển thị thông báo rằng đây là mô phỏng lỗi ghép chuỗi SQL.

**Secure Mode:**

-   Backend sử dụng parameterized query.
-   Dữ liệu nhập vào được xem là giá trị, không phải cú pháp SQL.
-   Cùng một kịch bản đầu vào minh họa phải không vượt qua xác thực.
-   Hiển thị giải thích về prepared statements.

> Gợi ý triển khai an toàn: thay vì tạo một giao diện cho phép nhập và
> chạy SQL tùy ý, hãy xây dựng các test case mô phỏng có sẵn. Mục đích
> là minh họa nguyên nhân và cách phòng chống, không tạo công cụ khai
> thác có thể dùng lên mục tiêu khác.

### 4.3. Database Viewer

Tạo bảng `users` với dữ liệu giả lập, ví dụ:

  id   username       password_hash          role
  ---- -------------- ---------------------- -------
  1    admin_demo     giá trị hash giả lập   admin
  2    student_demo   giá trị hash giả lập   user
  3    guest_demo     giá trị hash giả lập   guest

Lưu ý:

-   Không lưu mật khẩu dạng văn bản thuần.
-   Không dùng mật khẩu cá nhân hoặc mật khẩu đang sử dụng.
-   Không hiển thị password hash trên giao diện.
-   Database Viewer chỉ đọc dữ liệu mẫu và chỉ hiển thị các trường cần
    thiết.

### 4.4. Event Logs

Mỗi lần thử đăng nhập ghi lại:

-   Thời gian.
-   Chế độ đang chạy.
-   Tên test case.
-   Kết quả: thành công/thất bại.
-   Ghi chú giải thích.

Không ghi password hoặc toàn bộ dữ liệu nhạy cảm vào log.

### 4.5. Security Comparison

Tạo một khu vực so sánh:

  -----------------------------------------------------------------------
  Nội dung                Vulnerable Mode         Secure Mode
  ----------------------- ----------------------- -----------------------
  Xử lý đầu vào           Minh họa cách xử lý     Dùng tham số truy vấn
                          không an toàn           

  Dữ liệu đầu vào         Có thể làm thay đổi     Được xử lý như dữ liệu
                          logic truy vấn trong    
                          kịch bản mô phỏng       

  Rủi ro                  Có nguy cơ SQL          Giảm thiểu SQL
                          Injection               Injection

  Khuyến nghị             Không sử dụng trong ứng Ưu tiên sử dụng
                          dụng thực tế            
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 5. Kiến trúc dự án

Luồng tổng quát:

``` text
Browser
   |
   v
Flask Routes
   |
   +------ Login Simulator
   |          |
   |          +------ Vulnerable Demo (local test scenario)
   |          |
   |          +------ Secure Login (parameterized query)
   |
   +------ Database Viewer
   |
   +------ Event Logs
   |
   v
SQLite Database
```

### Trách nhiệm từng phần

-   **Browser:** Hiển thị giao diện, gửi thông tin form.
-   **Flask Routes:** Nhận request, kiểm tra dữ liệu và gọi service phù
    hợp.
-   **Login Service:** Chạy kịch bản mô phỏng hoặc xác thực an toàn.
-   **Database Layer:** Truy vấn SQLite.
-   **Logging Service:** Ghi lại sự kiện demo.
-   **SQLite:** Lưu tài khoản giả lập và lịch sử sự kiện.

------------------------------------------------------------------------

## 6. Cấu trúc thư mục đề xuất

``` text
sql-injection-attack-simulator/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── db.py
│   ├── init_db.py
│   └── schema.sql
│
├── services/
│   ├── auth_service.py
│   ├── simulation_service.py
│   └── log_service.py
│
├── routes/
│   ├── home_routes.py
│   ├── auth_routes.py
│   └── dashboard_routes.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── simulator.html
│   ├── database.html
│   └── logs.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── tests/
│   ├── test_auth.py
│   ├── test_simulation.py
│   └── test_database.py
│
└── instance/
    └── .gitkeep
```

**Lưu ý:** File database được tạo khi chạy chương trình nên không commit
database chứa dữ liệu runtime lên Git. Có thể commit script tạo schema
và dữ liệu demo.

------------------------------------------------------------------------

## 7. Thiết kế database

### Bảng `users`

  Cột             Kiểu dữ liệu   Ý nghĩa
  --------------- -------------- -----------------
  id              INTEGER        Khóa chính
  username        TEXT           Tên tài khoản
  password_hash   TEXT           Mật khẩu đã băm
  role            TEXT           Vai trò demo

### Bảng `event_logs`

  Cột          Kiểu dữ liệu   Ý nghĩa
  ------------ -------------- ----------------------------
  id           INTEGER        Khóa chính
  created_at   TEXT           Thời điểm xảy ra
  mode         TEXT           vulnerable / secure
  event_type   TEXT           login / simulation
  result       TEXT           success / failed / blocked
  message      TEXT           Giải thích ngắn

Tạo khóa chính cho cả hai bảng. Đặt `username` là duy nhất. Chỉ lưu
những thông tin thực sự cần cho demo.

------------------------------------------------------------------------

## 8. Kế hoạch triển khai theo từng giai đoạn

### Giai đoạn 1 --- Khởi tạo project

-   [ ] Tạo repository GitHub.
-   [ ] Tạo thư mục dự án.
-   [ ] Tạo virtual environment Python.
-   [ ] Cài Flask và pytest.
-   [ ] Tạo `app.py` và chạy trang Flask đầu tiên.
-   [ ] Tạo `.gitignore`.
-   [ ] Viết README bản đầu.

**Kết quả:** Ứng dụng Flask chạy được trên máy local.

### Giai đoạn 2 --- Database

-   [ ] Tạo SQLite database.
-   [ ] Tạo bảng `users`.
-   [ ] Tạo bảng `event_logs`.
-   [ ] Viết script khởi tạo dữ liệu demo.
-   [ ] Viết hàm kết nối database.
-   [ ] Kiểm tra việc đọc dữ liệu mẫu.

**Kết quả:** Database có dữ liệu giả lập và có thể truy vấn.

### Giai đoạn 3 --- Login Simulator

-   [ ] Tạo form đăng nhập.
-   [ ] Viết luồng xác thực an toàn bằng parameterized query.
-   [ ] Viết kịch bản Vulnerable Mode cố định, chỉ chạy trên database
    demo.
-   [ ] Thêm lựa chọn chế độ.
-   [ ] Hiển thị kết quả và giải thích.
-   [ ] Không lưu password vào log.

**Kết quả:** Có thể so sánh hai cách xử lý đầu vào trên cùng một bộ dữ
liệu thử nghiệm.

### Giai đoạn 4 --- Database Viewer và Logs

-   [ ] Tạo trang xem danh sách tài khoản demo.
-   [ ] Chỉ hiển thị username và role.
-   [ ] Tạo trang lịch sử sự kiện.
-   [ ] Ghi log mỗi lần chạy test case.
-   [ ] Thêm nút reset dữ liệu demo.

**Kết quả:** Người xem quan sát được tác động mô phỏng và lịch sử chạy
thử.

### Giai đoạn 5 --- Giao diện

-   [ ] Tạo layout chung.
-   [ ] Tạo trang giới thiệu.
-   [ ] Thiết kế Login Simulator.
-   [ ] Thiết kế bảng Database Viewer.
-   [ ] Thiết kế bảng Event Logs.
-   [ ] Thêm nhãn phân biệt Vulnerable Mode và Secure Mode.
-   [ ] Hiển thị cảnh báo khi chạy chế độ mô phỏng dễ bị tổn thương.

**Kết quả:** Giao diện rõ ràng, dễ demo và dễ hiểu.

### Giai đoạn 6 --- Kiểm thử và hoàn thiện

-   [ ] Kiểm tra đăng nhập hợp lệ.
-   [ ] Kiểm tra đăng nhập sai.
-   [ ] Kiểm tra kịch bản mô phỏng cố định ở Vulnerable Mode.
-   [ ] Kiểm tra cùng kịch bản ở Secure Mode.
-   [ ] Kiểm tra dữ liệu database không bị thay đổi ngoài dự kiến.
-   [ ] Kiểm tra log không chứa password.
-   [ ] Kiểm tra reset dữ liệu.
-   [ ] Viết hướng dẫn cài đặt và chạy.
-   [ ] Chụp ảnh giao diện để đưa vào README.

**Kết quả:** Project chạy ổn định, có test và tài liệu hướng dẫn.

------------------------------------------------------------------------

## 9. Test cases đề xuất

  -----------------------------------------------------------------------
  ID                      Tình huống              Kết quả mong đợi
  ----------------------- ----------------------- -----------------------
  TC01                    Username/password hợp   Đăng nhập thành công
                          lệ                      

  TC02                    Password không đúng     Đăng nhập thất bại

  TC03                    Username không tồn tại  Đăng nhập thất bại

  TC04                    Dữ liệu đầu vào chứa ký Được xử lý như dữ liệu,
                          tự đặc biệt             không gây lỗi ứng dụng

  TC05                    Chạy kịch bản mô phỏng  Hiển thị kết quả mô
                          ở Vulnerable Mode       phỏng đã định nghĩa

  TC06                    Chạy cùng kịch bản ở    Không vượt qua xác thực
                          Secure Mode             

  TC07                    Mở Database Viewer      Chỉ hiển thị trường
                                                  được phép

  TC08                    Kiểm tra Event Logs     Có log nhưng không chứa
                                                  mật khẩu

  TC09                    Reset demo data         Database trở về trạng
                                                  thái ban đầu

  TC10                    Gửi form thiếu dữ liệu  Hiển thị thông báo hợp
                                                  lệ, không làm ứng dụng
                                                  crash
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 10. Cách chạy dự án

### Yêu cầu

-   Python 3.10 trở lên.
-   Git.
-   VS Code hoặc IDE tương đương.

### Bước 1: Clone repository

``` bash
git clone https://github.com/<your-username>/sql-injection-attack-simulator.git
cd sql-injection-attack-simulator
```

### Bước 2: Tạo virtual environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài dependencies

``` bash
pip install -r requirements.txt
```

### Bước 4: Khởi tạo database

``` bash
python database/init_db.py
```

### Bước 5: Chạy ứng dụng

``` bash
python app.py
```

Mở trình duyệt tại địa chỉ local mà Flask hiển thị, thường là:

``` text
http://127.0.0.1:5000
```

------------------------------------------------------------------------

## 11. Dependencies dự kiến

File `requirements.txt` có thể bắt đầu như sau:

``` text
Flask
pytest
```

Trong quá trình phát triển, nếu cần thêm thư viện xử lý password hash,
hãy chọn thư viện phù hợp và cập nhật requirements. SQLite đã được tích
hợp sẵn trong Python nên không cần cài package riêng.

------------------------------------------------------------------------

## 12. Git workflow

Nên chia công việc thành các commit nhỏ, dễ theo dõi:

  Commit gợi ý                                Nội dung
  ------------------------------------------- ------------------------
  `chore: initialize Flask project`           Khởi tạo project
  `feat: add SQLite database schema`          Tạo schema
  `feat: implement secure authentication`     Xác thực an toàn
  `feat: add SQL injection simulation mode`   Thêm kịch bản mô phỏng
  `feat: add database viewer`                 Trang xem dữ liệu
  `feat: add event logging`                   Ghi nhật ký
  `feat: build simulator interface`           Giao diện
  `test: add authentication test cases`       Kiểm thử
  `docs: complete project README`             Tài liệu

Có thể dùng nhánh `main` cho phiên bản ổn định và nhánh `feature/...`
cho từng chức năng.

------------------------------------------------------------------------

## 13. Nội dung README trên GitHub

README nên có các phần:

1.  Project title và mô tả ngắn.
2.  Project overview.
3.  Learning objectives.
4.  Features.
5.  Technologies.
6.  Application screenshots.
7.  Project structure.
8.  Installation.
9.  How to run.
10. Test cases.
11. Security notes and limitations.
12. Future improvements.

### Mô tả GitHub ngắn

``` text
A local educational web application that demonstrates SQL Injection risks
using a controlled SQLite environment and compares vulnerable behavior
with parameterized queries.
```

### Topics gợi ý

``` text
sql-injection
cybersecurity
information-security
python
flask
sqlite
web-security
educational-project
```

------------------------------------------------------------------------

## 14. Kịch bản demo khi thuyết trình

Thời lượng gợi ý: 5--7 phút.

1.  **Giới thiệu (30--45 giây):** Nêu SQL Injection là gì và mục tiêu dự
    án.
2.  **Giới thiệu ứng dụng (45 giây):** Cho xem trang Login Simulator và
    database demo.
3.  **Vulnerable Mode (1 phút):** Chạy test case mô phỏng đã định nghĩa
    sẵn, giải thích vì sao cách xử lý không an toàn có thể làm sai lệch
    logic xác thực.
4.  **Secure Mode (1 phút):** Chạy cùng test case và cho thấy
    parameterized query xử lý đầu vào như dữ liệu.
5.  **Database Viewer (45 giây):** Cho xem dữ liệu giả lập.
6.  **Event Logs (45 giây):** Cho xem lịch sử các lần chạy thử.
7.  **Kết luận (30--45 giây):** Nhấn mạnh prepared statements và kiểm
    tra đầu vào là các biện pháp quan trọng.

------------------------------------------------------------------------

## 15. Tiêu chí hoàn thành dự án

Dự án được xem là hoàn thành khi:

-   [ ] Chạy được trên máy local theo README.
-   [ ] Có database SQLite và dữ liệu giả lập.
-   [ ] Có hai chế độ mô phỏng và an toàn.
-   [ ] Có thể giải thích sự khác nhau giữa hai chế độ.
-   [ ] Secure Mode sử dụng parameterized queries.
-   [ ] Có Database Viewer chỉ đọc.
-   [ ] Có Event Logs và không ghi password.
-   [ ] Có ít nhất 10 test cases hoặc kiểm tra tương đương.
-   [ ] Có README, ảnh minh họa và hướng dẫn cài đặt.
-   [ ] Không chứa chức năng tấn công mục tiêu bên ngoài.

------------------------------------------------------------------------

## 16. Hướng phát triển nếu còn thời gian

Chỉ thực hiện sau khi MVP hoàn thành:

-   Thêm biểu đồ thống kê số lần đăng nhập thành công/thất bại.
-   Thêm giải thích trực quan về cách parameterized query hoạt động.
-   Thêm các bài học nhỏ về input validation, least privilege và error
    handling.
-   Thêm chế độ so sánh kết quả test tự động.
-   Viết Dockerfile để người khác chạy project dễ hơn.
-   Bổ sung video demo ngắn vào README.

Không cần thêm nhiều tính năng ngay từ đầu. Một project nhỏ, chạy ổn
định, có test và giải thích rõ nguyên lý sẽ có giá trị hơn một project
lớn nhưng chưa hoàn thiện.

------------------------------------------------------------------------

## 17. Lộ trình thời gian tham khảo

  Ngày     Công việc
  -------- --------------------------------------
  Ngày 1   Khởi tạo Flask, GitHub và README
  Ngày 2   Thiết kế SQLite và dữ liệu demo
  Ngày 3   Làm Login Simulator và hai chế độ
  Ngày 4   Database Viewer và Event Logs
  Ngày 5   Hoàn thiện giao diện
  Ngày 6   Viết test và sửa lỗi
  Ngày 7   Viết tài liệu, chụp ảnh và quay demo

Có thể kéo dài hoặc rút ngắn tùy thời gian. Ưu tiên hoàn thành luồng
chính trước khi làm đẹp giao diện.

------------------------------------------------------------------------

## 18. Kết luận

**SQL Injection Attack Simulator** là một dự án học tập vừa sức, phù hợp
để đưa lên GitHub và trình bày trong môn An toàn thông tin. Điểm quan
trọng nhất không phải tạo ra một công cụ tấn công thực tế, mà là chứng
minh được:

-   Lỗ hổng SQL Injection hình thành như thế nào.
-   Một ứng dụng có thể xử lý đầu vào không an toàn ra sao.
-   Parameterized queries giúp ngăn dữ liệu đầu vào bị hiểu nhầm là cú
    pháp SQL như thế nào.
-   Cách ghi log, kiểm thử và xây dựng ứng dụng an toàn hơn.

**Định hướng MVP:** Python + Flask + SQLite + HTML/CSS/JavaScript, chạy
local, dùng dữ liệu giả lập và test case cố định.
