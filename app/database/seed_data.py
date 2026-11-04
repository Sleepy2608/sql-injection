import os
import sqlite3
from werkzeug.security import generate_password_hash
from app.database.connection import get_db

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db(db_path=None):
    """Initializes the database schema and seeds initial mock data."""
    conn = get_db(db_path)
    
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn.executescript(schema_sql)
    seed_mock_data(conn)
    conn.commit()
    return True

def seed_mock_data(conn):
    """Seeds the initial datasets into tables."""
    cursor = conn.cursor()
    
    # 1. Users table
    users = [
        ('admin', generate_password_hash('Admin@Secure2026!'), 'System Administrator', 'admin', 'Master Key: KEY-99482-ROOT'),
        ('john_dev', generate_password_hash('DevPassword123!'), 'John Doe (Dev Lead)', 'developer', 'Staging DB: 192.168.1.50'),
        ('alice_hr', generate_password_hash('AliceHr2026#'), 'Alice Smith (HR)', 'manager', 'HR Payroll Portal Clearance'),
        ('bob_guest', generate_password_hash('GuestPass123'), 'Bob Vance (Guest)', 'guest', 'Temporary trial account')
    ]
    cursor.executemany(
        'INSERT INTO users (username, password_hash, full_name, role, secret_note) VALUES (?, ?, ?, ?, ?)',
        users
    )
    
    # 2. Products table (Searchable catalog)
    products = [
        ('Enterprise Hardware Firewall', 'Network Security', 1899.99, 'Next-generation deep packet inspection appliance.'),
        ('SIEM Log Analyzer Pro', 'Software License', 3450.00, 'Real-time security analytics and behavioral anomaly detection.'),
        ('Hardware FIDO2 Security Key', 'Authentication', 55.00, 'FIPS 140-3 Level 3 certified USB-C 2FA authenticator.'),
        ('Vulnerability Scanner Suite', 'Security Tools', 1200.00, 'Automated static and dynamic web app security assessment.'),
        ('Air-Gapped Encrypted Drive 2TB', 'Secure Storage', 280.00, 'AES-XTS 256-bit hardware encrypted solid-state drive.'),
        ('Wireless Rogue AP Detector', 'IoT & Wireless', 420.00, 'Continuous spectrum analyzer for rogue Wi-Fi/Bluetooth devices.')
    ]
    cursor.executemany(
        'INSERT INTO products (name, category, price, description) VALUES (?, ?, ?, ?)',
        products
    )
    
    # 3. Secret Vault (Target for CTF challenges)
    secrets = [
        ('Classified Challenge Flag #1', 'FLAG{SQLI_AUTH_BYPASS_MASTER}', 'LEVEL_1'),
        ('Classified Challenge Flag #2', 'FLAG{SQLI_UNION_DATA_EXFIL_2026}', 'LEVEL_2'),
        ('Classified Challenge Flag #3', 'FLAG{SQLI_FILTER_EVASION_HERO}', 'LEVEL_3')
    ]
    cursor.executemany(
        'INSERT INTO secret_vault (item_name, flag_code, clearance_level) VALUES (?, ?, ?)',
        secrets
    )
    
    # 4. Initial Audit Log
    cursor.execute(
        '''INSERT INTO audit_logs (module, mode, payload, executed_query, status, risk_level)
           VALUES (?, ?, ?, ?, ?, ?)''',
        ('SYSTEM', 'SETUP', 'N/A', 'Database initialized and seeded successfully.', 'INITIALIZED', 'INFO')
    )

def reset_db(db_path=None):
    """Convenience alias to re-initialize and seed database."""
    return init_db(db_path)

