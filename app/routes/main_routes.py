from flask import Blueprint, render_template
from app.database.connection import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main dashboard displaying overview, metrics, and quick lab access."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Quick metrics for dashboard
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM audit_logs")
    log_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE risk_level = 'HIGH'")
    high_risk_count = cursor.fetchone()[0]

    return render_template(
        'index.html',
        user_count=user_count,
        product_count=product_count,
        log_count=log_count,
        high_risk_count=high_risk_count
    )

@main_bp.route('/theory')
def theory():
    """Theory & Educational section explaining SQLi mechanics and mitigations."""
    return render_template('theory.html')

