from flask import Blueprint, render_template, request, jsonify, session
from app.database.connection import get_db
from app.database.seed_data import reset_db

api_bp = Blueprint('api', __name__)

@api_bp.route('/db-viewer')
def db_viewer():
    """Renders the Database Inspection Dashboard."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, full_name, role, secret_note FROM users")
    users = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT id, name, category, price, description FROM products")
    products = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT id, item_name, flag_code, clearance_level FROM secret_vault")
    secrets = [dict(r) for r in cursor.fetchall()]

    return render_template(
        'db_viewer.html',
        users=users,
        products=products,
        secrets=secrets
    )

@api_bp.route('/audit-logs')
def audit_logs_page():
    """Renders the live audit logs page."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 100")
    logs = [dict(r) for r in cursor.fetchall()]
    return render_template('audit_logs.html', logs=logs)

@api_bp.route('/api/reset-db', methods=['POST'])
def api_reset_database():
    """1-Click API to wipe and reset sandbox database to original seeded state."""
    try:
        reset_db()
        # Optionally reset session solved challenges
        session.pop('solved_challenges', None)
        return jsonify({
            "success": True,
            "message": "Đã khôi phục toàn bộ dữ liệu SQLite Sandbox về trạng thái ban đầu thành công!"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi khi reset cơ sở dữ liệu: {str(e)}"
        }), 500

@api_bp.route('/api/audit-logs', methods=['GET'])
def get_audit_logs_json():
    """Returns the latest audit logs in JSON for auto-refreshing UI."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50")
    logs = [dict(r) for r in cursor.fetchall()]
    return jsonify({"logs": logs})

@api_bp.route('/api/database/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """Safe table inspection API limited to whitelisted demo tables."""
    allowed_tables = ['users', 'products', 'secret_vault', 'audit_logs']
    if table_name not in allowed_tables:
        return jsonify({"error": "Bảng không được phép truy cập."}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    if table_name == 'users':
        cursor.execute("SELECT id, username, full_name, role, secret_note FROM users")
    else:
        cursor.execute(f"SELECT * FROM {table_name}")
        
    rows = [dict(r) for r in cursor.fetchall()]
    return jsonify({"table": table_name, "rows": rows, "count": len(rows)})

