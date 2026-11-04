import re

class NaiveDefenseFilter:
    """
    Implements a flawed, naive blacklist filter commonly attempted by beginners.
    Demonstrates why Blacklist Filtering fails against SQL Injection evasion techniques.
    """

    # Naive filter checking only exact case or simple regex without accounting for
    # case variations (uNiOn), inline comment tricks (/**/), or nested words (OORR).
    NAIVE_BLACKLIST = [r'\bOR\b', r'\bAND\b', r'\bUNION\b', r'\bSELECT\b']

    @classmethod
    def check_input(cls, user_input: str) -> dict:
        """
        Naive check: Only checks uppercase keywords with word boundaries (\b).
        Fails against:
          - Mixed case: 'oR 1=1', 'uNiOn sElEcT'
          - Inline comment bypass: '/**/OR/**/1=1'
          - Symbol based tautology: '||' or char tricks
        """
        if not user_input:
            return {"blocked": False, "matched": None, "reason": None}

        # Flawed check 1: only checks UPPERCASE exact keywords
        for pattern in cls.NAIVE_BLACKLIST:
            if re.search(pattern, user_input):  # Note: case-sensitive match!
                return {
                    "blocked": True,
                    "matched": pattern,
                    "reason": f"Bộ lọc Naive Blacklist phát hiện từ khóa nguy hiểm bị cấm: '{pattern}' (Chữ hoa)."
                }

        return {
            "blocked": False,
            "matched": None,
            "reason": "Vượt qua bộ lọc Naive Blacklist thành công (Bypass)!"
        }

class DefenseKnowledge:
    """
    Theoretical explanations comparing defense mechanisms for education.
    """
    
    @staticmethod
    def get_comparison():
        return {
            "vulnerable": {
                "title": "Cấp 0: Không phòng thủ (Raw Concatenation)",
                "mechanism": "Nối chuỗi trực tiếp: f\"SELECT ... WHERE col = '{input}'\"",
                "weakness": "Dữ liệu người dùng trở thành một phần của cú pháp lệnh SQL (Cây cú pháp AST bị bẻ cong).",
                "risk": "CỰC KỲ NGUY HIỂM (Critical CVSS 9.8+)"
            },
            "naive": {
                "title": "Cấp 1: Phòng thủ yếu (Naive Blacklist / Regex)",
                "mechanism": "Dùng regex hoặc hàm replace để loại bỏ từ khóa nguy hiểm như 'OR', 'UNION'.",
                "weakness": "Dễ dàng bị qua mặt bằng kỹ thuật Obfuscation (chữ hoa xen thường 'uNiOn', comment '/**/', URL encode).",
                "risk": "NGUY HIỂM CAO - Tạo cảm giác an toàn giả tạo (False Sense of Security)"
            },
            "secure": {
                "title": "Cấp 2: Phòng thủ chuẩn mực (Parameterized Queries)",
                "mechanism": "Sử dụng Prepared Statements: cursor.execute(query, params) với dấu '?' hoặc ':name'.",
                "advantage": "Database Engine biên dịch câu lệnh TRƯỚC khi gán dữ liệu. Ký tự đặc biệt như ' hoặc -- chỉ là chuỗi thông thường.",
                "risk": "AN TOÀN TUYỆT ĐỐI trước SQL Injection (Theo chuẩn OWASP Top 10)"
            }
        }

