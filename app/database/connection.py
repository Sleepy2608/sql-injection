import sqlite3
import os
from flask import g, current_app

def get_db(db_path=None):
    """
    Get a database connection.
    If running within a Flask request context, reuse connection in `g`.
    Otherwise, open and return a fresh connection.
    """
    if db_path is None:
        try:
            db_path = current_app.config['DATABASE_PATH']
        except RuntimeError:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'instance',
                'sqli_sandbox.db'
            )

    # Ensure parent directory exists if using a file path
    if db_path != ':memory:':
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    # If inside Flask context, cache in g
    try:
        if 'db' not in g:
            g.db = sqlite3.connect(
                db_path,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db
    except RuntimeError:
        conn = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        conn.row_factory = sqlite3.Row
        return conn

def close_db(e=None):
    """Closes the database connection stored in Flask g."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Register database teardown in Flask app."""
    app.teardown_appcontext(close_db)

