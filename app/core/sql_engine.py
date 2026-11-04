import sqlite3
from werkzeug.security import check_password_hash
from app.database.connection import get_db
from app.core.query_highlighter import QueryHighlighter
from app.core.defense_service import NaiveDefenseFilter

class SQLEngine:
    """
    Central execution engine for SQL Injection simulations across:
    1. Authentication Bypass Lab
    2. UNION-based Data Exfiltration Lab
    3. Filter Evasion Lab
    """

    @staticmethod
    def log_event(conn, module: str, mode: str, payload: str, query: str, status: str, risk: str):
        """Records every attempt into the sandbox audit_logs table."""
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO audit_logs (module, mode, payload, executed_query, status, risk_level)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (module, mode.upper(), payload[:255], query[:500], status, risk)
            )
            conn.commit()
        except Exception:
            pass

    @classmethod
    def execute_login(cls, username: str, password: str, mode: str = "vulnerable", db_path=None) -> dict:
        conn = get_db(db_path)
        cursor = conn.cursor()
        
        # 1. NAIVE DEFENSE CHECK (Lab 3 mode)
        if mode == "naive":
            check_result = NaiveDefenseFilter.check_input(username)
            if check_result["blocked"]:
                inspector = QueryHighlighter.highlight_login_query(username, password, mode="vulnerable")
                cls.log_event(conn, "AUTH", mode, username, inspector["raw_query"], "BLOCKED", "MEDIUM")
                return {
                    "success": False,
                    "blocked_by_filter": True,
                    "filter_reason": check_result["reason"],
                    "error": "Yêu cầu bị chặn bởi bộ lọc WAF/Blacklist cơ bản.",
                    "user": None,
                    "inspector": inspector,
                    "mode": mode
                }
            # If not blocked, it proceeds to vulnerable execution to show successful bypass!
            vulnerable_res = cls._run_vulnerable_login(conn, cursor, username, password, mode_label="naive")
            vulnerable_res["bypassed_filter"] = True
            vulnerable_res["filter_reason"] = check_result["reason"]
            return vulnerable_res

        # 2. SECURE MODE (Prepared statements & Password Hash validation)
        if mode == "secure":
            inspector = QueryHighlighter.highlight_login_query(username, password, mode="secure")
            try:
                # Parameterized query to look up user
                cursor.execute(
                    "SELECT id, username, password_hash, full_name, role, secret_note FROM users WHERE username = ?",
                    (username,)
                )
                user_row = cursor.fetchone()
                
                if user_row and check_password_hash(user_row["password_hash"], password):
                    cls.log_event(conn, "AUTH", mode, username, inspector["raw_query"], "SUCCESS", "LOW")
                    return {
                        "success": True,
                        "blocked_by_filter": False,
                        "user": dict(user_row),
                        "error": None,
                        "inspector": inspector,
                        "mode": mode
                    }
                else:
                    cls.log_event(conn, "AUTH", mode, username, inspector["raw_query"], "FAILED", "LOW")
                    return {
                        "success": False,
                        "blocked_by_filter": False,
                        "user": None,
                        "error": "Tài khoản hoặc mật khẩu không chính xác (Được bảo vệ bởi Prepared Statements).",
                        "inspector": inspector,
                        "mode": mode
                    }
            except Exception as e:
                return {
                    "success": False,
                    "user": None,
                    "error": f"Lỗi hệ thống: {str(e)}",
                    "inspector": inspector,
                    "mode": mode
                }

        # 3. VULNERABLE MODE (Raw String Concatenation)
        return cls._run_vulnerable_login(conn, cursor, username, password, mode_label="vulnerable")

    @classmethod
    def _run_vulnerable_login(cls, conn, cursor, username: str, password: str, mode_label: str) -> dict:
        inspector = QueryHighlighter.highlight_login_query(username, password, mode="vulnerable")
        raw_query = inspector["raw_query"]
        
        try:
            cursor.execute(raw_query)
            user_row = cursor.fetchone()
            
            if user_row:
                risk = "HIGH" if inspector["injected_syntax_detected"] else "LOW"
                status = "EXPLOITED" if inspector["injected_syntax_detected"] else "SUCCESS"
                cls.log_event(conn, "AUTH", mode_label, username, raw_query, status, risk)
                
                try:
                    user_dict = {
                        "id": user_row["id"],
                        "username": user_row["username"],
                        "full_name": user_row["full_name"],
                        "role": user_row["role"],
                        "secret_note": user_row["secret_note"]
                    }
                except (TypeError, IndexError, KeyError):
                    user_dict = {
                        "id": user_row[0],
                        "username": user_row[1],
                        "full_name": user_row[3] if len(user_row) > 3 else "Unknown",
                        "role": user_row[4] if len(user_row) > 4 else "unknown",
                        "secret_note": user_row[5] if len(user_row) > 5 else None
                    }

                return {
                    "success": True,
                    "blocked_by_filter": False,
                    "user": user_dict,
                    "error": None,
                    "inspector": inspector,
                    "mode": mode_label
                }
            else:
                cls.log_event(conn, "AUTH", mode_label, username, raw_query, "FAILED", "LOW")
                return {
                    "success": False,
                    "blocked_by_filter": False,
                    "user": None,
                    "error": "Đăng nhập thất bại: Sai thông tin hoặc điều kiện WHERE đánh giá là FALSE.",
                    "inspector": inspector,
                    "mode": mode_label
                }
        except sqlite3.OperationalError as db_err:
            # Return exact SQL error for educational demonstration of Error-based SQLi!
            err_msg = f"Lỗi SQLite Syntax Error: {str(db_err)}"
            cls.log_event(conn, "AUTH", mode_label, username, raw_query, "SQL_ERROR", "HIGH")
            return {
                "success": False,
                "blocked_by_filter": False,
                "user": None,
                "error": err_msg,
                "sql_syntax_error": True,
                "inspector": inspector,
                "mode": mode_label
            }

    @classmethod
    def execute_search(cls, search_term: str, mode: str = "vulnerable", db_path=None) -> dict:
        conn = get_db(db_path)
        cursor = conn.cursor()
        
        if mode == "secure":
            inspector = QueryHighlighter.highlight_search_query(search_term, mode="secure")
            try:
                cursor.execute(
                    "SELECT id, name, category, price, description FROM products WHERE name LIKE ?",
                    (f"%{search_term}%",)
                )
                rows = [dict(r) for r in cursor.fetchall()]
                cls.log_event(conn, "SEARCH", mode, search_term, inspector["raw_query"], "SUCCESS", "LOW")
                return {
                    "success": True,
                    "results": rows,
                    "count": len(rows),
                    "error": None,
                    "inspector": inspector,
                    "mode": mode
                }
            except Exception as e:
                return {
                    "success": False,
                    "results": [],
                    "count": 0,
                    "error": str(e),
                    "inspector": inspector,
                    "mode": mode
                }

        # Vulnerable Mode: Raw concatenation allowing UNION SELECT
        inspector = QueryHighlighter.highlight_search_query(search_term, mode="vulnerable")
        raw_query = inspector["raw_query"]
        
        try:
            cursor.execute(raw_query)
            # Fetch all rows and column names returned by query
            col_names = [col[0] for col in cursor.description] if cursor.description else []
            raw_rows = cursor.fetchall()
            
            # Format results
            results = []
            for row in raw_rows:
                row_dict = {}
                for idx, col in enumerate(col_names):
                    row_dict[col] = row[idx]
                results.append(row_dict)
                
            risk = "HIGH" if inspector["injected_syntax_detected"] else "LOW"
            status = "EXPLOITED" if ("UNION" in search_term.upper()) else "SUCCESS"
            cls.log_event(conn, "SEARCH", mode, search_term, raw_query, status, risk)
            
            return {
                "success": True,
                "columns": col_names,
                "results": results,
                "count": len(results),
                "error": None,
                "inspector": inspector,
                "mode": mode
            }
        except sqlite3.OperationalError as db_err:
            err_msg = f"Lỗi SQLite Syntax/UNION Error: {str(db_err)}"
            cls.log_event(conn, "SEARCH", mode, search_term, raw_query, "SQL_ERROR", "HIGH")
            return {
                "success": False,
                "columns": [],
                "results": [],
                "count": 0,
                "error": err_msg,
                "sql_syntax_error": True,
                "inspector": inspector,
                "mode": mode
            }
