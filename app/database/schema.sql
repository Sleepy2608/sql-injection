-- Schema for SQL Injection Simulator Sandbox
-- SQLite Database

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    secret_note TEXT
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS secret_vault;
CREATE TABLE secret_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    flag_code TEXT NOT NULL,
    clearance_level TEXT NOT NULL
);

DROP TABLE IF EXISTS audit_logs;
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    module TEXT NOT NULL,
    mode TEXT NOT NULL,
    payload TEXT NOT NULL,
    executed_query TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

