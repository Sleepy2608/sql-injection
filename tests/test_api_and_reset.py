import pytest

def test_tc16_reset_database_api(client):
    """TC16: Reset DB endpoint returns success."""
    res = client.post('/api/reset-db')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True

def test_tc17_table_inspection_api(client):
    """TC17: Table inspection API returns users data safely."""
    res = client.get('/api/database/users')
    assert res.status_code == 200
    data = res.get_json()
    assert data['table'] == 'users'
    assert data['count'] >= 4

def test_tc18_table_inspection_whitelist(client):
    """TC18: Table inspection blocks arbitrary/non-whitelisted table access."""
    res = client.get('/api/database/sqlite_master')
    assert res.status_code == 400
    data = res.get_json()
    assert 'không được phép' in data['error']

def test_tc19_submit_correct_flag(client):
    """TC19: Submitting correct flag succeeds and awards points."""
    res = client.post('/challenges/api/submit', json={
        'challenge_id': 'c1',
        'flag': 'FLAG{SQLI_AUTH_BYPASS_MASTER}'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['points'] == 100
    assert 'c1' in data['solved']

def test_tc20_submit_wrong_flag(client):
    """TC20: Submitting wrong flag fails gracefully."""
    res = client.post('/challenges/api/submit', json={
        'challenge_id': 'c1',
        'flag': 'FLAG{INVALID_FLAG_123}'
    })
    assert res.status_code == 400
    data = res.get_json()
    assert data['success'] is False

