<p align="center">
  <b>SQL Injection Attack & Defense Interactive Simulator</b>
</p>

> **Đồ án môn học:** An Toàn Thông Tin (Information Security)  
> **Yêu cầu đề tài:** Viết một chương trình có nguyên tắc hoạt động mô phỏng mã độc / kỹ thuật tấn công khai thác lỗ hổng cơ sở dữ liệu và cơ chế phòng thủ chuyên sâu.  
> **Môi trường:** Local Sandbox an toàn 100% (Python Flask + SQLite + Vanilla JS / Modern Cyber CSS)

---

## 📌 1. Giới thiệu tổng quan

**SQL Injection (SQLi)** là một trong những lỗ hổng bảo mật web nguy hiểm và phổ biến nhất (nằm trong danh mục **OWASP Top 10 - Injection A03**). Lỗ hổng này phát sinh khi dữ liệu người dùng không được kiểm soát chặt chẽ mà được nối chuỗi trực tiếp vào câu lệnh SQL, khiến Database Engine hiểu nhầm dữ liệu độc hại thành chỉ thị cú pháp cần thực thi.

Dự án này là một **Interactive Security Lab & Attack Simulator** chạy hoàn toàn trên máy cục bộ với cơ sở dữ liệu SQLite giả lập, cho phép người học và giảng viên:
1. **Trực tiếp quan sát và thực thi** các kỹ thuật tấn công SQLi thực tế.
2. **Trực quan hóa cấu trúc câu lệnh** bằng công cụ **Live SQL Query Inspector** (tô màu bóc tách phần mã nguồn gốc của hệ thống vs phần payload độc hại vs phần bị vô hiệu hóa do comment `--`).
3. **Thực nghiệm 3 cấp độ phòng thủ:** Từ không phòng thủ (Ghép chuỗi) $\rightarrow$ Phòng thủ yếu (Blacklist Regex dễ bị bypass) $\rightarrow$ Phòng thủ chuẩn mực (Prepared Statements / Parameterized Queries).
4. **Tham gia chế độ thử thách CTF (Challenge Arena):** Chinh phục 3 bài lab có chấm điểm và nộp Flag tự động.

---

## 🛡️ 2. Nguyên tắc an toàn (Security Guidelines)

- **Sandbox cục bộ:** Toàn bộ ứng dụng và dữ liệu hoạt động trên SQLite local (`instance/sqli_sandbox.db`). Không kết nối mạng ngoài, không quét (scan) hay thực thi trên bất kỳ mục tiêu bên thứ ba nào.
- **1-Click Database Reset:** Trang bị nút khôi phục dữ liệu nguyên bản tức thì qua API `/api/reset-db`, bảo đảm hệ thống luôn trong tầm kiểm soát.

---

## 🏗️ 3. Kiến trúc các Module & Tính năng

```text
                           [ Trình duyệt Client ]
                                     │
                   [ Giao diện Modern SOC Dashboard ]
       ┌─────────────────────────────┼─────────────────────────────┐
       │                             │                             │
 [ Lab 1: Auth Bypass ]    [ Lab 2: UNION Exfil ]     [ Lab 3: Filter Bypass ]
   (admin' --, ' OR 1=1)    (' UNION SELECT ...)       (/**/oR/**/1=1--)
       │                             │                             │
       └─────────────────────────────┼─────────────────────────────┘
                                     │
                    [ Live SQL Query Inspector ]
         (Tô màu: Template vs Injected Syntax vs Comments vs Params)
                                     │
              ┌──────────────────────┴──────────────────────┐
              │                                             │
    [ Chế độ Lỗ hổng ]                            [ Chế độ An toàn ]
  Raw String Concatenation                      Parameterized Queries (?, ?)
              │                                             │
              └──────────────────────┬──────────────────────┘
                                     │
                           [ SQLite Database ]
               (users, products, secret_vault, audit_logs)
```

### Chi tiết các phòng thí nghiệm:
1. **Lab 1: Authentication Bypass (Chiếm quyền Admin):**
   - Lỗ hổng: `SELECT * FROM users WHERE username = '{user}' AND password = '{pass}'`
   - Khai thác: Payload `admin' --` đóng chuỗi sớm và comment toàn bộ phần kiểm tra password.
   - Phòng thủ: Dùng `SELECT * FROM users WHERE username = ?` và hàm băm mật khẩu `check_password_hash`.
2. **Lab 2: UNION-Based Data Exfiltration (Trích xuất dữ liệu bí mật):**
   - Lỗ hổng: Ô tìm kiếm sản phẩm cho phép ghép mệnh đề `UNION SELECT`.
   - Khai thác: Ghép thêm các dòng từ bảng nhạy cảm `users` hoặc `secret_vault` với đúng 5 cột kết quả.
   - Phòng thủ: Sử dụng tham số hóa `WHERE name LIKE ?` với tuple `(f"%{term}%",)`.
3. **Lab 3: Filter Evasion & Blacklist Bypass (Đánh bại bộ lọc Regex):**
   - Vấn đề: Bộ lọc Naive Blacklist chỉ lọc từ khóa chữ hoa `OR`, `AND`.
   - Khai thác: Sử dụng chữ thường `oR` hoặc thay khoảng trắng bằng comment `/**/` (`admin'/**/oR/**/1=1--`).
   - Bài học: Blacklist luôn tạo ra cảm giác an toàn giả tạo; chỉ có Parameterized Queries mới ngăn chặn triệt để.
4. **CTF Challenge Arena:** 3 bài tập chấm điểm (+100, +200, +300 điểm), nút hiển thị gợi ý (Hint), nút điền nhanh payload và form nộp cờ (Flag verification).
5. **Database Viewer & Audit Logs:** Bảng theo dõi trực tiếp các bảng cơ sở dữ liệu và lịch sử các cuộc tấn công theo thời gian thực (Forensics).

---

## 💻 4. Công nghệ sử dụng

| Thành phần | Công nghệ | Mục đích |
| :--- | :--- | :--- |
| **Backend** | Python 3.12 + Flask | Nhẹ, chuẩn RESTful, quản lý route theo Blueprints |
| **Cơ sở dữ liệu** | SQLite 3 | Cục bộ, phi máy chủ, thread-safe, dễ dàng reset |
| **Bảo mật mật khẩu**| Werkzeug Security | Băm mật khẩu chuẩn PBKDF2:SHA256 |
| **Frontend** | HTML5, CSS3, Vanilla JS | Giao diện Dark SOC Dashboard, Live Query Inspector |
| **Kiểm thử tự động**| Pytest | Bộ test suite 25 ca kiểm thử tự động đạt 100% pass |
| **Tiện ích thực thi**| Windows Batch Script | `run.bat` khởi chạy server 1-click & `test.bat` chạy test nhanh |

---

## 📁 5. Cấu trúc mã nguồn

```text
sql-injection/
│
├── run.bat                      # [MỚI] Script khởi chạy ứng dụng 1-click trên Windows
├── test.bat                     # [MỚI] Script chạy 25 ca test tự động 1-click trên Windows
├── run.py                       # File khởi chạy ứng dụng chính (Flask Server)
├── config.py                    # Cấu hình môi trường và đường dẫn SQLite
├── requirements.txt             # Thư viện phụ thuộc (Flask, pytest, Werkzeug)
├── README.md                    # Tài liệu đồ án và hướng dẫn sử dụng
├── .gitattributes               # Chuẩn hóa line-ending và phân loại binary
├── .gitignore                   # Loại trừ file tạm, cache và database runtime
│
├── app/
│   ├── __init__.py              # Application Factory (create_app)
│   ├── database/
│   │   ├── connection.py        # Quản lý kết nối SQLite an toàn
│   │   ├── schema.sql           # Cấu trúc 4 bảng dữ liệu
│   │   └── seed_data.py         # Dữ liệu mẫu & hàm Reset Database
│   ├── core/
│   │   ├── sql_engine.py        # Bộ máy thực thi truy vấn (Vulnerable, Naive, Secure)
│   │   ├── query_highlighter.py # Bộ phân tích tô màu cú pháp (Inspector)
│   │   └── defense_service.py   # Triển khai Prepared Statements & Regex Filter
│   ├── routes/
│   │   ├── main_routes.py       # Trang chủ Dashboard & Trang lý thuyết
│   │   ├── auth_routes.py       # API & Giao diện Lab 1 (Auth Bypass)
│   │   ├── search_routes.py     # API & Giao diện Lab 2 (UNION Exfiltration)
│   │   ├── filter_routes.py     # API & Giao diện Lab 3 (Filter Bypass)
│   │   ├── challenge_routes.py  # Đấu trường CTF & Nộp Flag
│   │   └── api_routes.py        # Reset DB, Table inspection, Audit logs API
│   ├── static/
│   │   ├── css/                 # main.css, components.css (Dark Cyber Theme)
│   │   └── js/                  # main.js, simulator.js, challenges.js
│   └── templates/               # base.html, index.html, các trang lab Jinja2
│
└── tests/                       # 25 Test Cases tự động với Pytest
    ├── conftest.py              # Test database fixtures
    ├── test_auth_injection.py   # Test cases cho Lab 1 (Auth Bypass)
    ├── test_union_injection.py  # Test cases cho Lab 2 (UNION Exfiltration)
    ├── test_filter_bypass.py    # Test cases cho Lab 3 (Filter Bypass)
    ├── test_boundary_and_edge_cases.py # [MỚI] Test cases kiểm tra trường hợp biên & ngoại lệ
    └── test_api_and_reset.py    # Test cases cho Reset DB, CTF Flags & API
```

---

## 🚀 6. Hướng dẫn cài đặt & Khởi chạy

### Cách 1: Khởi chạy nhanh 1-Click trên Windows (Khuyến nghị)
Chỉ cần nhấp đúp chuột vào file **`run.bat`**:
- Script sẽ tự động kiểm tra Python, tự tạo `venv` và cài dependencies (nếu chưa có).
- Tự động mở trình duyệt web tại `http://127.0.0.1:5000`.
- Khởi động server Flask sẵn sàng tương tác.

---

### Cách 2: Khởi chạy thủ công qua dòng lệnh

#### Bước 1: Mở Terminal tại thư mục dự án
```bash
cd "c:\University Coding Project\sql-injection"
```

#### Bước 2: Kích hoạt Virtual Environment & Cài dependencies
Trên Windows:
```bash
# Đã có sẵn venv hoặc tạo mới:
python -m venv venv
venv\Scripts\activate

# Cài đặt thư viện:
pip install -r requirements.txt
```

#### Bước 3: Khởi chạy máy chủ Web
```bash
python run.py
```

Mở trình duyệt web và truy cập địa chỉ:  
👉 **`http://127.0.0.1:5000`**

---

## 🧪 7. Chạy kiểm thử tự động (Automated Pytest)

### Cách 1: Chạy nhanh qua file batch
Nhấp đúp chuột vào file **`test.bat`** để chạy toàn bộ 25 bài test tự động.

---

### Cách 2: Chạy qua dòng lệnh
Dự án đi kèm bộ **25 test cases** kiểm thử tự động toàn diện:
```bash
.\venv\Scripts\pytest.exe -v
```

**Kết quả kiểm thử:**
```text
============================= test session starts =============================
collected 25 items

tests/test_api_and_reset.py::test_tc16_reset_database_api PASSED          [  4%]
tests/test_api_and_reset.py::test_tc17_table_inspection_api PASSED        [  8%]
tests/test_api_and_reset.py::test_tc18_table_inspection_whitelist PASSED  [ 12%]
tests/test_api_and_reset.py::test_tc19_submit_correct_flag PASSED         [ 16%]
tests/test_api_and_reset.py::test_tc20_submit_wrong_flag PASSED           [ 20%]
tests/test_auth_injection.py::test_tc01_valid_login PASSED                [ 24%]
tests/test_auth_injection.py::test_tc02_invalid_password PASSED           [ 28%]
tests/test_auth_injection.py::test_tc03_admin_bypass_vulnerable PASSED    [ 32%]
tests/test_auth_injection.py::test_tc04_tautology_bypass_vulnerable PASSED [ 36%]
tests/test_auth_injection.py::test_tc05_admin_bypass_blocked_in_secure_mode PASSED [ 40%]
tests/test_auth_injection.py::test_tc06_unclosed_quote_syntax_error PASSED [ 44%]
tests/test_boundary_and_edge_cases.py::test_tc21_boundary_empty_and_whitespace_login PASSED [ 48%]
tests/test_boundary_and_edge_cases.py::test_tc22_boundary_unicode_vietnamese_characters PASSED [ 52%]
tests/test_boundary_and_edge_cases.py::test_tc23_boundary_extremely_long_payload PASSED [ 56%]
tests/test_boundary_and_edge_cases.py::test_tc24_edge_case_missing_json_fields PASSED [ 60%]
tests/test_boundary_and_edge_cases.py::test_tc25_idempotent_multiple_db_resets PASSED [ 64%]
tests/test_filter_bypass.py::test_tc12_naive_filter_blocks_uppercase_or PASSED [ 68%]
tests/test_filter_bypass.py::test_tc13_mixed_case_bypasses_naive_filter PASSED [ 72%]
tests/test_filter_bypass.py::test_tc14_inline_comment_bypasses_naive_filter PASSED [ 76%]
tests/test_filter_bypass.py::test_tc15_secure_mode_neutralizes_all_bypasses PASSED [ 80%]
tests/test_union_injection.py::test_tc07_normal_product_search PASSED     [ 84%]
tests/test_union_injection.py::test_tc08_union_users_exfiltration_vulnerable PASSED [ 88%]
tests/test_union_injection.py::test_tc09_union_secret_vault_flag_exfiltration PASSED [ 92%]
tests/test_union_injection.py::test_tc10_union_blocked_in_secure_mode PASSED [ 96%]
tests/test_union_injection.py::test_tc11_union_column_mismatch_error PASSED [100%]

============================= 25 passed in 100% =============================
```

---

## 🎤 8. Kịch bản thuyết trình Demo 7 phút trước Giảng viên

- **Phút 1: Đặt vấn đề & Bản chất lỗ hổng**
  - Mở trang chủ Dashboard `http://127.0.0.1:5000/`.
  - Giới thiệu đề tài: Lỗ hổng SQL Injection phát sinh khi trộn lẫn Code và Data.
- **Phút 2: Demo Lab 1 (Authentication Bypass)**
  - Vào **Lab 1**. Chọn chế độ *Vulnerable*.
  - Nhấp nút payload `admin' --` (1-click fill) $\rightarrow$ Bấm *Thực Thi Đăng Nhập*.
  - Chỉ vào khung **Live SQL Query Inspector** để phân tích: Dấu `'` đóng chuỗi sớm, dấu `--` vô hiệu hóa phần kiểm tra mật khẩu $\rightarrow$ Đăng nhập thành công với quyền `admin`.
- **Phút 3: Minh chứng phòng thủ (Prepared Statements)**
  - Chuyển sang chế độ *Secure (Prepared Query)* với cùng payload `admin' --`.
  - Bấm gửi $\rightarrow$ Đăng nhập thất bại an toàn. Giải thích: Dấu `?` trong Prepared Statement xem chuỗi là Literal Value, không có quyền thay đổi cú pháp SQL.
- **Phút 4: Demo Lab 2 (UNION Data Exfiltration)**
  - Vào **Lab 2**. Bấm nút `Trích xuất bảng Users` $\rightarrow$ Câu lệnh `UNION SELECT` đưa toàn bộ mật khẩu băm và ghi chú bí mật từ bảng `users` lên màn hình tìm kiếm sản phẩm.
- **Phút 5: Demo Lab 3 (Đánh bại bộ lọc Regex Blacklist)**
  - Vào **Lab 3**. Thử payload `admin' OR 1=1 --` $\rightarrow$ Bị bộ lọc chặn.
  - Thử payload `admin'/**/oR/**/1=1--` $\rightarrow$ Vượt qua bộ lọc thành công! Giải thích nguyên lý tại sao Blacklist Regex là giải pháp chắp vá và dễ bị bypass.
- **Phút 6: Demo CTF Arena & Nộp Flag**
  - Vào trang **CTF Challenges**. Nhập flag vừa trích xuất được ở Lab 2: `FLAG{SQLI_UNION_DATA_EXFIL_2026}` $\rightarrow$ Bấm *Nộp Flag* $\rightarrow$ Điểm số tăng lên và chuyển trạng thái "ĐÃ HOÀN THÀNH".
- **Phút 7: Audit Logs, 1-Click Reset & Kết luận**
  - Mở trang **Audit Logs** để chứng minh toàn bộ dấu vết truy vấn được giám sát (Forensics).
  - Bấm nút **Reset DB** trên thanh menu để đưa SQLite về nguyên bản.
  - Kết luận: Luôn áp dụng Prepared Statements, Input Whitelisting và Least Privilege trong phát triển phần mềm an toàn.

---

## 📜 9. Bản quyền & Lưu ý học thuật

Dự án được xây dựng phục vụ hoàn toàn cho mục đích giáo dục, nghiên cứu và báo cáo học phần An Toàn Thông Tin. Mọi hành vi sao chép hay sử dụng kỹ thuật tấn công trên các hệ thống thực tế mà không có sự cho phép bằng văn bản là vi phạm pháp luật.
