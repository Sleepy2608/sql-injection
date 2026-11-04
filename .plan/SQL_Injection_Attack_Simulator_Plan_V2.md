# SQL Injection Attack & Defense Interactive Simulator (Plan V2)

> **Đề tài:** Đồ án môn học An toàn thông tin  
> **Chủ đề:** Chương trình mô phỏng nguyên tắc hoạt động của mã độc / tấn công SQL Injection và cơ chế phòng thủ chuyên sâu  
> **Môi trường:** Local Sandbox (Python Flask + SQLite + Vanilla JS / Modern Cyber CSS)  
> **Trạng thái:** Bản đề xuất V2 (Đang chờ duyệt trước khi triển khai code)

---

## 1. So sánh sự khác biệt: Kế hoạch V1 vs Kế hoạch V2

| Tiêu chí | Kế hoạch V1 (Bản cũ) | Kế hoạch V2 (Bản nâng cấp toàn diện) |
| :--- | :--- | :--- |
| **Tính tương tác** | Hạn chế, chỉ chạy các test case kịch bản cố định (mock), người dùng không được nhập payload thật. | **Sandbox tương tác thực tế 100%:** Cho phép gõ hoặc chọn payload SQLi thực tế chạy trực tiếp trên SQLite sandbox local an toàn. |
| **Phạm vi kịch bản** | Chỉ có 1 form Đăng nhập (Auth Bypass). | **3 Vector tấn công kinh điển:**<br>1. Auth Bypass (Trang đăng nhập)<br>2. Data Extraction / Exfiltration (UNION-based SQLi trong ô tìm kiếm)<br>3. Filter Evasion (Vượt qua bộ lọc ký tự yếu / Naive Blacklist). |
| **Trực quan hóa SQL** | Chỉ hiển thị kết quả thành công/thất bại dạng text. | **Live SQL Query Inspector & Tokenizer:** Tô màu trực quan câu truy vấn: phần Code gốc của lập trình viên (xanh), phần Payload bị tiêm vào (đỏ/vàng), phần bị vô hiệu hóa bởi comment `--` (xám gạch). |
| **Cơ chế phòng thủ** | So sánh 2 chế độ: Vulnerable vs Secure. | **So sánh 3 cấp độ phòng thủ:**<br>1. *No Defense* (Nối chuỗi trực tiếp)<br>2. *Naive Defense* (Blacklist/Regex cơ bản - minh họa tại sao dễ bị bypass)<br>3. *Standard Defense* (Parameterized Queries / Prepared Statements). |
| **Tính học tập & Demo** | Đọc báo cáo tĩnh. | **Chế độ Thử thách CTF (Challenge Mode):** Có 3 bài lab với mục tiêu cụ thể, cờ bí mật (Flag), nút gợi ý (Hint) và "1-Click Payload Library" phục vụ thuyết trình trơn tru trước Giảng viên. |
| **Giao diện (UI/UX)** | HTML/CSS cơ bản dạng trang web cũ. | **Cybersecurity SOC Dashboard Theme:** Dark mode hiện đại, hiệu ứng terminal/code highlight, chia split-view hoặc tabs so sánh trực tiếp. |

---

## 2. Mục tiêu đồ án & Yêu cầu đề bài

1. **Đáp ứng yêu cầu môn học:**
   - Minh họa sinh động nguyên tắc hoạt động của kỹ thuật tấn công khai thác lỗ hổng cơ sở dữ liệu (tương tự hành vi của attacker/malware khi khai thác web target).
   - Thể hiện rõ sự khác biệt giữa mã nguồn chứa lỗ hổng bảo mật và mã nguồn đã được khắc phục chuẩn mực.
2. **Nguyên tắc an toàn (Safety Guidelines):**
   - Toàn bộ cơ sở dữ liệu là SQLite cục bộ (`local_sandbox.db`).
   - Có nút **"Reset Database"** (1-click khôi phục dữ liệu gốc bất kỳ lúc nào).
   - Tuyệt đối không kết nối ra Internet, không scan hay tấn công bất kỳ website/hệ thống bên ngoài nào.

---

## 3. Kiến trúc các Module chức năng

```text
                             [ Web Browser / Client ]
                                        │
                         [ Modern SOC / Cyber UI ]
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
    [ Module 1 ]                  [ Module 2 ]                  [ Module 3 ]
  Authentication Bypass        Data Exfiltration             Filter Bypass Lab
  (Login: ' OR 1=1 --)     (UNION SELECT on Products)    (Bypass weak regex/WAF)
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │
                         [ Live Query Inspector & Engine ]
             (Phân tách: Query Template vs Injected Syntax vs Comments)
                                        │
                     ┌──────────────────┴──────────────────┐
                     │                                     │
           [ Vulnerable Mode ]                     [ Secure Mode ]
        Raw String Concatenation             Parameterized Query (?, ?)
                     │                                     │
                     └──────────────────┬──────────────────┘
                                        │
                                [ SQLite Database ]
                     (users, products, secret_flags, audit_logs)
```

### Module 1: Authentication Bypass Simulator (Mô phỏng chiếm quyền đăng nhập)
- **Kịch bản:** Trang đăng nhập quản trị viên.
- **Mục tiêu tấn công:** Đăng nhập vào tài khoản `admin` mà không cần biết mật khẩu.
- **Câu truy vấn nền tảng:**
  ```sql
  SELECT * FROM users WHERE username = '{user_input}' AND password = '{pass_input}'
  ```
- **Khai thác:** 
  - Payload kinh điển: `admin' --` hoặc `' OR '1'='1' --`
  - Kết quả: Biểu thức luôn đúng (`TRUE`), vượt qua cơ chế kiểm tra mật khẩu.
- **Phòng thủ:** Chuyển sang `cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pass))` để vô hiệu hóa toàn bộ cú pháp SQL độc hại.

### Module 2: UNION-Based Data Exfiltration Simulator (Trích xuất dữ liệu nhạy cảm)
- **Kịch bản:** Trang tra cứu thông tin sản phẩm hoặc tin tức (`/search?q=`).
- **Mục tiêu tấn công:** Kẻ tấn công sử dụng mệnh đề `UNION SELECT` để lấy trích xuất dữ liệu từ các bảng nhạy cảm khác (bảng `users` hoặc bảng `secret_flags`).
- **Câu truy vấn nền tảng:**
  ```sql
  SELECT id, name, category, price FROM products WHERE name LIKE '%{search_term}%'
  ```
- **Khai thác:**
  - Payload: `' UNION SELECT id, username, role, password_hash FROM users --`
  - Kết quả: Dữ liệu tài khoản quản trị và mật khẩu bị lộ ngay trên bảng hiển thị sản phẩm!
- **Phòng thủ:** Sử dụng tham số hóa chuỗi tìm kiếm hoặc kiểm soát chặt chẽ schema đầu ra.

### Module 3: Filter Evasion & Naive Defense Lab (Minh họa điểm yếu của Blacklist)
- **Kịch bản:** Hệ thống cố gắng ngăn chặn SQLi bằng cách lọc từ khóa đơn giản (Regex / Blacklist):
  - Lọc từ khóa `OR`, `AND`, `UNION`, `SELECT` (chỉ kiểm tra chữ thường).
  - Hoặc loại bỏ khoảng trắng.
- **Khai thác (Bypass):**
  - Kỹ thuật thay đổi hoa/thường: `uNiOn SeLeCt`, `oR 1=1`.
  - Kỹ thuật dùng comment thay thế khoảng trắng: `admin'/**/OR/**/1=1#`.
  - Kỹ thuật lồng từ khóa: `OORR` -> sau khi bị replace `OR` sẽ còn lại `OR`.
- **Bài học rút ra:** Bộ lọc danh sách đen (Blacklist) là giải pháp chắp vá và luôn tiềm ẩn nguy cơ bị vượt qua. Chỉ có **Parameterized Queries** (Whitelist/Prepared Statements) mới là giải pháp triệt để.

### Module 4: Live Query Inspector (Điểm nhấn đồ án - Bộ phân tích thị giác)
Mỗi khi người dùng bấm gửi dữ liệu, màn hình sẽ hiển thị bảng phân tích:
1. **Raw SQL Executed:** Câu lệnh thực tế được gửi xuống SQLite.
2. **Visual Syntax Highlighting:**
   - Text màu trắng/xanh: Phần code cố định của hệ thống.
   - Text màu đỏ/cam: Đoạn payload người dùng nhập vào.
   - Text màu xám gạch ngang: Đoạn code phía sau bị vô hiệu hóa do comment (`--` hoặc `/* */`).
3. **AST / Logic Explanation:** Giải thích tại sao logic câu lệnh bị thay đổi từ `AND (password = X)` thành `TRUE`.

### Module 5: Interactive CTF Challenges (Chế độ phòng thí nghiệm chấm điểm)
Tạo thanh tiến độ với 3 nhiệm vụ dành cho người học/người xem demo:
- [ ] **Thử thách 1:** Vượt qua trang Login với quyền `admin` mà không nhập password.
- [ ] **Thử thách 2:** Khai thác lỗ hổng ô Tìm kiếm để tìm chuỗi bí mật `FLAG{SQLi_UNION_MASTER_2026}` nằm trong bảng bí mật.
- [ ] **Thử thách 3:** Đăng nhập thành công khi hệ thống bật chế độ "Lọc từ khóa thô sơ" (Bypass Filter).
- Kèm theo: Nút **"Show Hint"** và nút **"Quick Inject Payload"** (dành cho người thuyết trình bấm nhanh khi demo).

---

## 4. Thiết kế cơ sở dữ liệu (SQLite Schema)

### 4.1. Bảng `users` (Tài khoản người dùng)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'admin', 'user', 'guest'
    secret_note TEXT
);
```

### 4.2. Bảng `products` (Dữ liệu công khai cho trang Search)
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);
```

### 4.3. Bảng `secret_vault` (Dữ liệu bí mật cho bài CTF)
```sql
CREATE TABLE secret_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    flag_code TEXT NOT NULL,
    clearance_level TEXT NOT NULL
);
```

### 4.4. Bảng `audit_logs` (Nhật ký giám sát an ninh)
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    module TEXT NOT NULL,         -- 'LOGIN', 'SEARCH', 'FILTER_LAB'
    mode TEXT NOT NULL,           -- 'VULNERABLE', 'NAIVE_FILTER', 'SECURE'
    payload TEXT NOT NULL,
    executed_query TEXT NOT NULL,
    status TEXT NOT NULL,         -- 'SUCCESS', 'BLOCKED', 'ERROR'
    risk_level TEXT NOT NULL      -- 'HIGH', 'MEDIUM', 'LOW'
);
```

---

## 5. Cấu trúc thư mục dự án đề xuất

```text
sql-injection/
│
├── run.py                       # Điểm khởi chạy chính của ứng dụng
├── config.py                    # Cấu hình môi trường (DEBUG, DATABASE_PATH, SECRET_KEY)
├── requirements.txt             # Danh sách thư viện Python (Flask, pytest, ...)
├── README.md                    # Hướng dẫn chi tiết, hình ảnh minh họa, tài liệu đồ án
├── .gitignore                   # Loại trừ file tạm, file database runtime
│
├── app/
│   ├── __init__.py              # Application Factory (create_app)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # Quản lý kết nối SQLite thread-safe
│   │   ├── schema.sql           # Cấu trúc bảng ban đầu
│   │   └── seed_data.py         # Dữ liệu mẫu ban đầu & hàm Reset DB
│   │
│   ├── core/                    # Xử lý logic SQL Injection & Phòng thủ
│   │   ├── __init__.py
│   │   ├── sql_engine.py        # Thực thi query (Vulnerable vs Secure vs Naive)
│   │   ├── query_highlighter.py # Tokenizer phân tích tô màu cú pháp câu truy vấn
│   │   └── defense_service.py   # Triển khai Prepared Statements & Regex Filter
│   │
│   ├── routes/                  # Controller & API Endpoints
│   │   ├── __init__.py
│   │   ├── main_routes.py       # Trang chủ, Dashboard tổng quan
│   │   ├── auth_routes.py       # API mô phỏng Login Injection
│   │   ├── search_routes.py     # API mô phỏng UNION-based Search
│   │   ├── filter_routes.py     # API mô phỏng Filter Bypass
│   │   ├── challenge_routes.py  # Quản lý trạng thái và tiến độ bài tập CTF
│   │   └── api_routes.py        # Reset DB, lấy logs, lấy query inspector
│   │
│   ├── static/                  # Tài nguyên Frontend
│   │   ├── css/
│   │   │   ├── main.css         # Layout & theme phong cách Dark/SOC Cyber
│   │   │   └── components.css   # Style cho bảng, badges, visual inspector
│   │   └── js/
│   │       ├── main.js          # Khởi tạo giao diện, thông báo Toast
│   │       ├── simulator.js     # Xử lý gửi payload và cập nhật kết quả Live
│   │       └── challenges.js    # Kiểm tra cờ CTF, gợi ý, 1-click payload
│   │
│   └── templates/               # Giao diện Jinja2
│       ├── base.html            # Layout chung: Navbar, Footer, Status Bar
│       ├── index.html           # Trang giới thiệu lý thuyết & kiến trúc SQLi
│       ├── login_lab.html       # Phòng thí nghiệm 1: Auth Bypass
│       ├── search_lab.html      # Phòng thí nghiệm 2: UNION-based Exfiltration
│       ├── filter_lab.html      # Phòng thí nghiệm 3: Bypass Blacklist
│       ├── challenges.html      # Chế độ thử thách CTF có chấm điểm
│       ├── db_viewer.html       # Xem trực tiếp database nội bộ & nút Reset
│       └── audit_logs.html      # Bảng ghi nhật ký tấn công theo thời gian thực
│
├── tests/                       # Bộ kiểm thử tự động với Pytest
│   ├── __init__.py
│   ├── conftest.py              # Fixture khởi tạo test database tạm
│   ├── test_auth_injection.py   # Test case kịch bản đăng nhập
│   ├── test_union_injection.py  # Test case kịch bản tìm kiếm UNION
│   ├── test_filter_bypass.py    # Test case vượt qua bộ lọc
│   └── test_secure_mode.py      # Test case xác minh Prepared Statement chặn được 100%
│
└── .plan/                       # Thư mục chứa tài liệu kế hoạch phát triển
    ├── SQL_Injection_Attack_Simulator_Plan.md      # Bản kế hoạch V1 gốc
    └── SQL_Injection_Attack_Simulator_Plan_V2.md   # Bản kế hoạch V2 chi tiết hiện tại
```

---

## 6. Lộ trình triển khai chi tiết (Implementation Phases)

### Phase 1: Nền tảng dự án & Cơ sở dữ liệu Sandbox
- [ ] Thiết lập môi trường ảo (`venv`), cài đặt Flask, pytest.
- [ ] Xây dựng mô-đun kết nối SQLite thread-safe (`connection.py`).
- [ ] Tạo file schema và script gieo dữ liệu mẫu (`seed_data.py`).
- [ ] Viết chức năng **Reset Database** đưa dữ liệu về trạng thái nguyên bản chỉ với 1 click.

### Phase 2: Core Engine & Query Inspector (Trái tim của Simulator)
- [ ] Xây dựng `sql_engine.py` hỗ trợ 3 chế độ thực thi:
  - `Vulnerable`: Nối chuỗi trực tiếp (`f"SELECT ... '{input}'"`).
  - `Naive Defense`: Kiểm tra qua bộ lọc từ khóa đơn giản trước khi thực thi.
  - `Secure`: Sử dụng `cursor.execute(query, params)`.
- [ ] Xây dựng thuật toán phân tích chuỗi `query_highlighter.py` để phân biệt:
  - Code gốc của ứng dụng (Template).
  - Ký tự độc hại người dùng chèn vào (Injected Tokens).
  - Đoạn lệnh bị vô hiệu hóa bởi comment SQL (`--` hoặc `/*`).

### Phase 3: Phát triển 3 Phòng thí nghiệm (Lab Modules)
- [ ] **Lab 1 (Auth Bypass):** Xây dựng route và giao diện đăng nhập kiểm thử.
- [ ] **Lab 2 (UNION Exfiltration):** Xây dựng trang tìm kiếm sản phẩm và cơ chế trả về kết quả rò rỉ dữ liệu.
- [ ] **Lab 3 (Filter Evasion):** Xây dựng bộ lọc từ khóa yếu và form thử nghiệm kỹ thuật bypass.

### Phase 4: Giao diện người dùng Cyber Dashboard & CTF Mode
- [ ] Thiết kế giao diện Dark Mode phong cách An toàn thông tin (chuyên nghiệp, hiện đại, không lòe loẹt).
- [ ] Xây dựng thanh công cụ "Payload Library" (nhấp 1 nút là tự điền payload mẫu như `' OR 1=1 --`, `' UNION SELECT ...`).
- [ ] Tích hợp bảng trạng thái kiểm tra mục tiêu CTF (Challenge status tracker).
- [ ] Trang Database Viewer (cho phép quan sát bảng `users`, `products`, `secret_vault` thay đổi như thế nào sau mỗi lần tấn công).
- [ ] Trang Audit Logs hiển thị toàn bộ lịch sử các truy vấn kèm mức độ cảnh báo an ninh.

### Phase 5: Kiểm thử tự động (Automated Testing) & Hoàn thiện tài liệu
- [ ] Viết bộ test cases bằng `pytest` kiểm tra đầy đủ cả 3 kịch bản:
  - Xác nhận payload tấn công thành công ở chế độ Vulnerable.
  - Xác nhận kỹ thuật bypass qua mặt được Naive Filter.
  - Xác nhận Prepared Statement chặn đứng hoàn toàn mọi payload ở chế độ Secure.
- [ ] Viết file `README.md` chuyên nghiệp:
  - Tổng quan đồ án, video/ảnh chụp màn hình demo.
  - Hướng dẫn cài đặt và chạy trong 3 bước.
  - Giải thích nguyên lý tấn công và cách phòng thủ chuẩn OWASP.

---

## 7. Bộ Test Cases kiểm thử đề xuất

| Test ID | Module | Payload kiểm tra | Chế độ chạy | Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- |
| **TC01** | Auth Bypass | `admin' --` (Pass để trống) | Vulnerable | Đăng nhập thành công với quyền `admin`. |
| **TC02** | Auth Bypass | `admin' --` | Secure | Đăng nhập thất bại (xem payload là chuỗi ký tự thông thường). |
| **TC03** | Auth Bypass | `' OR '1'='1` | Vulnerable | Đăng nhập thành công với tài khoản đầu tiên trong bảng. |
| **TC04** | Auth Bypass | `' OR '1'='1` | Secure | Đăng nhập thất bại. |
| **TC05** | UNION Exfil | `' UNION SELECT id, username, role, password_hash FROM users --` | Vulnerable | Danh sách tài khoản và mật khẩu hiển thị trên bảng sản phẩm. |
| **TC06** | UNION Exfil | `' UNION SELECT id, username, role, password_hash FROM users --` | Secure | Trả về 0 kết quả tìm kiếm (không lỗi, không rò rỉ). |
| **TC07** | Filter Lab | `admin' OR 1=1 --` | Naive Filter | Bị chặn bởi bộ lọc (phát hiện từ khóa `OR`). |
| **TC08** | Filter Lab | `admin'/**/oR/**/1=1#` | Naive Filter | Vượt qua bộ lọc thành công do biến thể chữ hoa/thường và comment! |
| **TC09** | Filter Lab | `admin'/**/oR/**/1=1#` | Secure | Đăng nhập thất bại an toàn. |
| **TC10** | Database Reset | Gọi API `/api/reset-db` | Bất kỳ | Cơ sở dữ liệu trở lại trạng thái ban đầu chính xác 100%. |

---

## 8. Kịch bản thuyết trình Demo đề xuất (7 Phút)

- **Phút 1 (Đặt vấn đề):** Giới thiệu đề tài đồ án An toàn thông tin. Giải thích nguyên nhân gốc rễ của SQL Injection: Sự nhầm lẫn giữa dữ liệu (Data) và mã lệnh (Code) khi lập trình viên ghép chuỗi thô.
- **Phút 2 (Demo Auth Bypass):** 
  - Thao tác đăng nhập thất bại với tài khoản sai.
  - Chọn payload mẫu `admin' --`, bấm tấn công ở chế độ Vulnerable -> Đăng nhập admin thành công.
  - Mở thanh **Live Query Inspector** chỉ rõ câu lệnh bị vô hiệu hóa phần kiểm tra mật khẩu.
- **Phút 3 (Demo Phòng thủ chuẩn):** 
  - Bật chế độ Secure Mode, chạy lại chính payload đó -> Hệ thống chặn đứng, giải thích nguyên lý tham số hóa của Prepared Statements.
- **Phút 4 (Demo UNION Exfiltration):** 
  - Sang trang tìm kiếm sản phẩm. Tiêm payload UNION để lôi toàn bộ bảng `users` và bảng mật khẩu ra ngoài giao diện.
- **Phút 5 (Demo Vượt qua bộ lọc - Filter Bypass):** 
  - Chứng minh rằng bộ lọc từ khóa đơn giản (Blacklist) dễ dàng bị đánh bại bởi các kỹ thuật biến đổi payload (`oR`, `/**/`).
- **Phút 6 (Giới thiệu Audit Logs & Database Viewer):** 
  - Mở trang Logs cho thấy toàn bộ dấu vết tấn công được ghi lại với cảnh báo mức độ rủi ro (Risk Level).
  - Bấm nút **Reset Database** để chứng minh tính an toàn và khả năng phục hồi của hệ thống.
- **Phút 7 (Tổng kết & Kết luận):** 
  - Khẳng định thông điệp phòng thủ: "Never trust user input, always use Parameterized Queries / Prepared Statements".

---

## 9. Điểm nổi bật giúp đồ án đạt điểm cao (Điểm cộng chuyên môn)

1. **Không phải là ứng dụng Mock tĩnh:** Câu lệnh SQL thực sự chạy trên SQLite sandbox thật, sinh ra kết quả thật hoặc báo lỗi cú pháp thật.
2. **Trực quan hóa cao độ (Visual Query Inspector):** Giảng viên nhìn vào là hiểu ngay cách thức lỗ hổng hoạt động mà không cần giải thích dài dòng.
3. **Có kịch bản phản biện (Defense Counter-measure):** Không chỉ dừng lại ở việc tấn công, đồ án còn phân tích sâu tại sao các cách phòng thủ nửa vời (như viết regex lọc từ) lại thất bại, từ đó tôn vinh tầm quan trọng của Prepared Statements.
4. **Trải nghiệm mượt mà:** Có sẵn "Payload Library" và nút "Reset Database" giúp việc demo trong phòng thi diễn ra tự tin, không sợ bị treo dữ liệu hay gõ sai cú pháp.

---

> ⚠️ **Quy trình tiếp theo:** Hãy xem xét kỹ bản kế hoạch V2 này. Khi bạn cảm thấy đã hoàn toàn ưng ý với cấu trúc và tính năng, hãy phản hồi lại để tôi bắt đầu triển khai code từng bước một cách bài bản!

