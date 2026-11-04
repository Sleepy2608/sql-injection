import os
import tempfile
import pytest
from app import create_app
from config import Config
from app.database import seed_data

@pytest.fixture
def app():
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    class TestConfig(Config):
        TESTING = True
        DATABASE_PATH = db_path
        SECRET_KEY = 'test-secret-key-123'

    app = create_app(TestConfig)

    with app.app_context():
        seed_data.init_db(db_path)

    yield app

    # Cleanup temporary test db file
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

