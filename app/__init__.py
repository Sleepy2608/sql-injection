import os
from flask import Flask
from config import Config
from app.database import connection, seed_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database teardown hooks
    connection.init_app(app)

    # Auto-initialize SQLite database file if it does not exist
    with app.app_context():
        db_path = app.config['DATABASE_PATH']
        if db_path != ':memory:' and not os.path.exists(db_path):
            seed_data.init_db(db_path)

    # Register application blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.search_routes import search_bp
    from app.routes.filter_routes import filter_bp
    from app.routes.challenge_routes import challenge_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(filter_bp)
    app.register_blueprint(challenge_bp)
    app.register_blueprint(api_bp)

    return app

