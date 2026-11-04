import pytest

def test_tc21_boundary_empty_and_whitespace_login(client):
    """TC21: Empty and pure whitespace inputs handle gracefully without crashing."""
    res = client.post('/lab/auth', json={
        'username': '   ',
        'password': '   ',
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data['user'] is None

def test_tc22_boundary_unicode_vietnamese_characters(client):
    """TC22: Unicode and accented Vietnamese strings are handled properly."""
    res = client.post('/lab/search', json={
        'query': 'Thiết bị tường lửa bảo mật an toàn thông tin',
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert isinstance(data['results'], list)

def test_tc23_boundary_extremely_long_payload(client):
    """TC23: Extremely long strings (buffer fuzzing) are handled safely."""
    long_payload = "admin" + "' OR '1'='1" * 300 + " --"
    res = client.post('/lab/auth', json={
        'username': long_payload,
        'password': 'any',
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    # Audit log should truncate safely and system should not crash
    assert data['inspector'] is not None

def test_tc24_edge_case_missing_json_fields(client):
    """TC24: Malformed or missing JSON request fields return graceful responses."""
    res = client.post('/lab/auth', json={})
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False

def test_tc25_idempotent_multiple_db_resets(client):
    """TC25: Calling Reset DB multiple times in sequence maintains consistency."""
    # First reset
    res1 = client.post('/api/reset-db')
    assert res1.status_code == 200
    assert res1.get_json()['success'] is True

    # Second reset immediately
    res2 = client.post('/api/reset-db')
    assert res2.status_code == 200
    assert res2.get_json()['success'] is True

    # Verify tables still have exact seed count
    users_res = client.get('/api/database/users')
    assert users_res.status_code == 200
    assert users_res.get_json()['count'] == 4

    products_res = client.get('/api/database/products')
    assert products_res.status_code == 200
    assert products_res.get_json()['count'] == 6

