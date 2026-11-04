import pytest

def test_tc07_normal_product_search(client):
    """TC07: Normal search query finds products correctly."""
    res = client.post('/lab/search', json={
        'query': 'Firewall',
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data['count'] >= 1
    assert any('Firewall' in p['name'] for p in data['results'])

def test_tc08_union_users_exfiltration_vulnerable(client):
    """TC08: UNION SELECT dumps the users table in vulnerable mode."""
    payload = "' UNION SELECT id, username, role, password_hash, secret_note FROM users --"
    res = client.post('/lab/search', json={
        'query': payload,
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    # Verify that admin is among the results returned from search!
    usernames = [str(r.get('name') or r.get('username')) for r in data['results']]
    assert any('admin' in u for u in usernames)

def test_tc09_union_secret_vault_flag_exfiltration(client):
    """TC09: UNION SELECT dumps the secret_vault table and retrieves CTF Flag."""
    payload = "' UNION SELECT id, item_name, clearance_level, 0, flag_code FROM secret_vault --"
    res = client.post('/lab/search', json={
        'query': payload,
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    # Verify that CTF Flag is exfiltrated
    all_texts = [str(val) for r in data['results'] for val in r.values()]
    assert any('FLAG{SQLI_UNION_DATA_EXFIL_2026}' in t for t in all_texts)

def test_tc10_union_blocked_in_secure_mode(client):
    """TC10: Parameterized search treats UNION payload as literal substring (0 results)."""
    payload = "' UNION SELECT id, username, role, password_hash, secret_note FROM users --"
    res = client.post('/lab/search', json={
        'query': payload,
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data['count'] == 0  # No product named with the UNION payload

def test_tc11_union_column_mismatch_error(client):
    """TC11: UNION with mismatched column count produces SQLite operational error."""
    payload = "' UNION SELECT 1, 2 --"  # Only 2 columns while products has 5
    res = client.post('/lab/search', json={
        'query': payload,
        'mode': 'vulnerable'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data.get('sql_syntax_error') is True
    assert 'number of result columns' in data['error'].lower()

