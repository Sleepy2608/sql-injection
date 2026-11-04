import html
import re

class QueryHighlighter:
    """
    Analyzes and tokenizes SQL queries to produce rich, educational visual breakdowns.
    Highlights the difference between developer SQL templates, attacker-injected syntax,
    and neutralized SQL comments.
    """

    @staticmethod
    def highlight_login_query(username: str, password: str, mode: str = "vulnerable"):
        """
        Creates visual breakdown for the Authentication query:
        SELECT * FROM users WHERE username = '{username}' AND password = '{password}'
        """
        if mode == "secure":
            query_template = "SELECT * FROM users WHERE username = ? AND password = ?"
            explanation = (
                "Chế độ An Toàn (Prepared Statements): Cơ sở dữ liệu biên dịch trước khung câu lệnh với các dấu '?' "
                "làm tham số. Toàn bộ chuỗi đầu vào của người dùng được coi là DỮ LIỆU THUẦN TÚY (Data Literal), "
                "không thể can thiệp hoặc thay đổi cấu trúc cây cú pháp (AST) của SQL."
            )
            html_output = (
                '<span class="tok-kw">SELECT</span> * <span class="tok-kw">FROM</span> users '
                '<span class="tok-kw">WHERE</span> username = <span class="tok-param">?</span> '
                '<span class="tok-kw">AND</span> password = <span class="tok-param">?</span>'
            )
            params_display = f"Params: [username = '{html.escape(username)}', password = '{html.escape(password)}']"
            return {
                "raw_query": query_template,
                "html_output": html_output,
                "params_display": params_display,
                "mode": mode,
                "explanation": explanation,
                "injected_syntax_detected": False
            }

        # Vulnerable mode query concatenation
        raw_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        # Check if comment symbols exist in username
        comment_match = re.search(r'(--|#|\/\*)', username)
        
        has_injection = any(keyword in username.upper() for keyword in ["'", "--", "OR", "AND", "UNION", "SELECT", "/*", "#"])
        
        if comment_match:
            c_start = comment_match.start()
            c_marker = comment_match.group(1)
            
            injected_active = username[:c_start]
            injected_marker = username[c_start:c_start + len(c_marker)]
            injected_after_marker = username[c_start + len(c_marker):]
            
            # The remaining template part:
            disabled_tail = f"'{injected_after_marker}' AND password = '{password}'"
            
            html_output = (
                '<span class="tok-template">SELECT * FROM users WHERE username = \'</span>'
                f'<span class="tok-injected-code">{html.escape(injected_active)}</span>'
                f'<span class="tok-comment-marker">{html.escape(injected_marker)}</span>'
                f'<span class="tok-commented-out">{html.escape(disabled_tail)}</span>'
            )
            explanation = (
                f"Ký hiệu comment '<strong>{html.escape(c_marker)}</strong>' đã vô hiệu hóa hoàn toàn "
                "mệnh đề kiểm tra mật khẩu phía sau. Hệ thống chỉ còn kiểm tra điều kiện phía trước, "
                "cho phép đăng nhập trái phép vào tài khoản mục tiêu."
            )
        else:
            html_output = (
                '<span class="tok-template">SELECT * FROM users WHERE username = \'</span>'
                f'<span class="tok-injected-code">{html.escape(username)}</span>'
                '<span class="tok-template">\' AND password = \'</span>'
                f'<span class="tok-injected-code">{html.escape(password)}</span>'
                '<span class="tok-template">\'</span>'
            )
            if has_injection:
                explanation = (
                    "Chuỗi đầu vào chứa các ký tự điều khiển cú pháp SQL (dấu nháy đơn, từ khóa logic). "
                    "Nếu biểu thức được đánh giá là TRUE (ví dụ: ' OR '1'='1), logic xác thực sẽ bị bẻ gãy."
                )
            else:
                explanation = "Câu truy vấn được ghép chuỗi thông thường. Không phát hiện dấu hiệu khai thác rõ ràng."

        return {
            "raw_query": raw_query,
            "html_output": html_output,
            "params_display": "None (Raw String Concatenation)",
            "mode": mode,
            "explanation": explanation,
            "injected_syntax_detected": has_injection
        }

    @staticmethod
    def highlight_search_query(search_term: str, mode: str = "vulnerable"):
        """
        Creates visual breakdown for the UNION Exfiltration query:
        SELECT id, name, category, price, description FROM products WHERE name LIKE '%{search_term}%'
        """
        if mode == "secure":
            query_template = "SELECT id, name, category, price, description FROM products WHERE name LIKE ?"
            explanation = (
                "Chế độ An Toàn (Prepared Statements): Ký tự đại diện '%' được kết hợp an toàn vào tham số "
                "dạng '?'. Câu lệnh chỉ tìm kiếm trong bảng products, không thể mở rộng sang các bảng khác bằng UNION."
            )
            html_output = (
                '<span class="tok-kw">SELECT</span> id, name, category, price, description '
                '<span class="tok-kw">FROM</span> products '
                '<span class="tok-kw">WHERE</span> name <span class="tok-kw">LIKE</span> <span class="tok-param">?</span>'
            )
            params_display = f"Params: ['%{html.escape(search_term)}%']"
            return {
                "raw_query": query_template,
                "html_output": html_output,
                "params_display": params_display,
                "mode": mode,
                "explanation": explanation,
                "injected_syntax_detected": False
            }

        raw_query = f"SELECT id, name, category, price, description FROM products WHERE name LIKE '%{search_term}%'"
        
        has_union = "UNION" in search_term.upper()
        comment_match = re.search(r'(--|#|\/\*)', search_term)
        
        if comment_match:
            c_start = comment_match.start()
            c_marker = comment_match.group(1)
            
            injected_active = search_term[:c_start]
            injected_marker = search_term[c_start:c_start + len(c_marker)]
            injected_after = search_term[c_start + len(c_marker):]
            disabled_tail = f"{injected_after}%'"
            
            html_output = (
                '<span class="tok-template">SELECT id, name, category, price, description FROM products WHERE name LIKE \'%</span>'
                f'<span class="tok-injected-code">{html.escape(injected_active)}</span>'
                f'<span class="tok-comment-marker">{html.escape(injected_marker)}</span>'
                f'<span class="tok-commented-out">{html.escape(disabled_tail)}</span>'
            )
        else:
            html_output = (
                '<span class="tok-template">SELECT id, name, category, price, description FROM products WHERE name LIKE \'%</span>'
                f'<span class="tok-injected-code">{html.escape(search_term)}</span>'
                '<span class="tok-template">%\'</span>'
            )

        if has_union:
            explanation = (
                "Phát hiện mệnh đề <strong>UNION SELECT</strong>: Kẻ tấn công nối thêm kết quả từ bảng khác "
                "(như bảng users hoặc secret_vault) vào cùng cấu trúc cột trả về của bảng products, "
                "dẫn đến rò rỉ dữ liệu nhạy cảm ra giao diện tìm kiếm."
            )
        else:
            explanation = "Tìm kiếm sản phẩm ghép chuỗi trực tiếp. Chưa phát hiện mệnh đề UNION."

        return {
            "raw_query": raw_query,
            "html_output": html_output,
            "params_display": "None (Raw String Concatenation)",
            "mode": mode,
            "explanation": explanation,
            "injected_syntax_detected": has_union or (comment_match is not None)
        }

