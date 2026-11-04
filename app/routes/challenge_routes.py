from flask import Blueprint, render_template, request, jsonify, session
from app.database.connection import get_db

challenge_bp = Blueprint('challenges', __name__, url_prefix='/challenges')

CHALLENGE_DEFINITIONS = [
    {
        "id": "c1",
        "title": "Thử thách 1: Chiếm quyền Admin (Auth Bypass)",
        "difficulty": "Easy",
        "points": 100,
        "description": "Khai thác lỗ hổng ghép chuỗi tại Phòng thí nghiệm 1 (Auth Bypass) để đăng nhập vào tài khoản 'admin' mà không cần biết mật khẩu.",
        "hint": "Sử dụng ký tự nháy đơn ' kèm theo toán tử logic OR hoặc ký hiệu comment SQL: admin' --",
        "sample_payload": "admin' --",
        "flag": "FLAG{SQLI_AUTH_BYPASS_MASTER}",
        "target_url": "/lab/auth"
    },
    {
        "id": "c2",
        "title": "Thử thách 2: Trích xuất Flag bí mật (UNION Exfiltration)",
        "difficulty": "Medium",
        "points": 200,
        "description": "Khai thác ô tìm kiếm sản phẩm tại Phòng thí nghiệm 2 để trích xuất cờ bí mật được lưu trong bảng 'secret_vault' (clearance_level = 'LEVEL_2').",
        "hint": "Bảng products có 5 cột (id, name, category, price, description). Bảng secret_vault có các cột (id, item_name, flag_code, clearance_level). Sử dụng UNION SELECT với đúng 5 cột!",
        "sample_payload": "' UNION SELECT id, item_name, clearance_level, 0, flag_code FROM secret_vault --",
        "flag": "FLAG{SQLI_UNION_DATA_EXFIL_2026}",
        "target_url": "/lab/search"
    },
    {
        "id": "c3",
        "title": "Thử thách 3: Đánh bại bộ lọc Regex (Filter Evasion)",
        "difficulty": "Hard",
        "points": 300,
        "description": "Vượt qua bộ lọc Naive Blacklist tại Phòng thí nghiệm 3. Bộ lọc này chặn từ khóa 'OR' chữ hoa. Hãy tìm cách biến thể payload để đăng nhập thành công.",
        "hint": "Thử dùng chữ hoa xen lẫn chữ thường như 'oR 1=1 --' hoặc sử dụng comment inline 'admin'/**/oR/**/1=1--'.",
        "sample_payload": "admin'/**/oR/**/1=1--",
        "flag": "FLAG{SQLI_FILTER_EVASION_HERO}",
        "target_url": "/lab/filter"
    }
]

@challenge_bp.route('')
def challenge_board():
    solved = session.get('solved_challenges', [])
    return render_template(
        'challenges.html',
        challenges=CHALLENGE_DEFINITIONS,
        solved=solved
    )

@challenge_bp.route('/api/submit', methods=['POST'])
def submit_flag():
    data = request.get_json() or {}
    challenge_id = data.get('challenge_id')
    submitted_flag = data.get('flag', '').strip()

    target_challenge = next((c for c in CHALLENGE_DEFINITIONS if c['id'] == challenge_id), None)
    if not target_challenge:
        return jsonify({"success": False, "message": "Không tìm thấy thử thách tương ứng."}), 404

    if submitted_flag == target_challenge['flag']:
        solved = session.get('solved_challenges', [])
        if challenge_id not in solved:
            solved.append(challenge_id)
            session['solved_challenges'] = solved

        return jsonify({
            "success": True,
            "message": f"🎉 Chính xác! Bạn đã giải thành công '{target_challenge['title']}' (+{target_challenge['points']} điểm)!",
            "points": target_challenge['points'],
            "solved": solved
        })
    else:
        return jsonify({
            "success": False,
            "message": "❌ Flag không chính xác! Hãy kiểm tra lại kết quả trích xuất được từ database sandbox."
        }), 400
