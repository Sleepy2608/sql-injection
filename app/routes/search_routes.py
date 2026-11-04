from flask import Blueprint, render_template, request, jsonify
from app.core.sql_engine import SQLEngine

search_bp = Blueprint('search', __name__, url_prefix='/lab/search')

@search_bp.route('', methods=['GET', 'POST'])
def search_lab():
    search_term = ""
    mode = "vulnerable"
    result = None

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            search_term = data.get('query', '')
            mode = data.get('mode', 'vulnerable')
        else:
            search_term = request.form.get('query', '')
            mode = request.form.get('mode', 'vulnerable')

        result = SQLEngine.execute_search(search_term, mode=mode)
        
        if request.is_json:
            return jsonify(result)
    elif 'q' in request.args:
        search_term = request.args.get('q', '')
        mode = request.args.get('mode', 'vulnerable')
        result = SQLEngine.execute_search(search_term, mode=mode)

    return render_template(
        'search_lab.html',
        result=result,
        search_term=search_term,
        mode=mode
    )

