from app import create_app
from config import Config
from app.database.seed_data import init_db
import os

app = create_app(Config)

if __name__ == '__main__':
    # Ensure database is prepared
    db_file = app.config['DATABASE_PATH']
    if not os.path.exists(db_file):
        with app.app_context():
            print(f"[*] Initializing sandbox database at: {db_file}")
            init_db(db_file)

    print("=" * 65)
    print(" 🚀 SQL INJECTION ATTACK & DEFENSE SIMULATOR (SECURITY LAB)")
    print(" Server running locally at: http://127.0.0.1:5000")
    print(" Sandbox Mode: SAFE LOCAL SQLITE ENVIRONMENT")
    print("=" * 65)
    app.run(host='127.0.0.1', port=5000, debug=True)

