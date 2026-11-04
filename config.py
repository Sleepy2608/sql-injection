import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sqli-edu-secret-key-2026-safe-sandbox')
    DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'sqli_sandbox.db')
    TESTING = False
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'

