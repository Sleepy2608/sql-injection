from flask import Blueprint, render_template, request, jsonify
from app.core.sql_engine import SQLEngine
from app.core.defense_service import NaiveDefenseFilter, DefenseKnowledge

filter_bp = Blueprint('filter_lab', __name__, url_prefix='/lab/filter')

@filter_bp.route('', methods=['GET', 'POST'])
def filter_lab():
    username = ""
    password = ""
    mode = "naive"
    result = None

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            username = data.get('username', '')
            password = data.get('password', '')
            mode = data.get('mode', 'naive')
        else:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            mode = request.form.get('mode', 'naive')

        result = SQLEngine.execute_login(username, password, mode=mode)
        
        if request.is_json:
            return jsonify(result)

    return render_template(
        'filter_lab.html',
        result=result,
        username=username,
        password=password,
        mode=mode,
        defense_info=DefenseKnowledge.get_comparison(),
        blacklist_rules=NaiveDefenseFilter.NAIVE_BLACKLIST
    )

