from flask import Blueprint, render_template, request, jsonify
from app.core.sql_engine import SQLEngine

auth_bp = Blueprint('auth', __name__, url_prefix='/lab/auth')

@auth_bp.route('', methods=['GET', 'POST'])
def auth_lab():
    if request.method == 'POST':
        # Accept either JSON (AJAX) or Form submission
        if request.is_json:
            data = request.get_json() or {}
            username = data.get('username', '')
            password = data.get('password', '')
            mode = data.get('mode', 'vulnerable')
        else:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            mode = request.form.get('mode', 'vulnerable')

        result = SQLEngine.execute_login(username, password, mode=mode)
        
        if request.is_json:
            return jsonify(result)
            
        return render_template(
            'login_lab.html',
            result=result,
            username=username,
            password=password,
            mode=mode
        )

    return render_template('login_lab.html', result=None, mode='vulnerable')

