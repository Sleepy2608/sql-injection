import pytest

def test_tc01_valid_login(client):
    """TC01: Valid credentials authenticate successfully."""
    res = client.post('/lab/auth', json={
        'username': 'admin',
        'password': 'Admin@Secure2026!',
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data['user']['username'] == 'admin'

def test_tc02_invalid_password(client):
    """TC02: Wrong password fails in secure mode."""
    res = client.post('/lab/auth', json={
        'username': 'admin',
        'password': 'WrongPassword123',
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False

def test_tc03_admin_bypass_vulnerable(client):
    """TC03: Classic admin' -- payload succeeds in vulnerable mode."""
    res = client.post('/lab/auth', json={
        'username': "admin' --",
        'password': "",
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data['user']['username'] == 'admin'
    assert data['user']['role'] == 'admin'
    assert data['inspector']['injected_syntax_detected'] is True

def test_tc04_tautology_bypass_vulnerable(client):
    """TC04: ' OR '1'='1' -- tautology payload succeeds in vulnerable mode."""
    res = client.post('/lab/auth', json={
        'username': "' OR '1'='1' --",
        'password': "",
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data['user'] is not None

def test_tc05_admin_bypass_blocked_in_secure_mode(client):
    """TC05: Parameterized queries in secure mode neutralize admin' -- payload."""
    res = client.post('/lab/auth', json={
        'username': "admin' --",
        'password': "",
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data['user'] is None

def test_tc06_unclosed_quote_syntax_error(client):
    """TC06: Unclosed quote returns SQLite syntax error without 500 server crash."""
    res = client.post('/lab/auth', json={
        'username': "admin'",
        'password': "any",
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data.get('sql_syntax_error') is True
    assert 'unrecognized token' in data['error'].lower() or 'syntax error' in data['error'].lower()
