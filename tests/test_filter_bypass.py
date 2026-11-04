import pytest

def test_tc12_naive_filter_blocks_uppercase_or(client):
    """TC12: Naive regex blacklist blocks uppercase 'OR' keyword."""
    res = client.post('/lab/filter', json={
        'username': "admin' OR 1=1 --",
        'password': "",
        'mode': 'naive'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data['blocked_by_filter'] is True
    assert 'bị cấm' in data['filter_reason']

def test_tc13_mixed_case_bypasses_naive_filter(client):
    """TC13: Mixed-case 'oR' bypasses naive regex filter and achieves login."""
    res = client.post('/lab/filter', json={
        'username': "admin' oR '1'='1' --",
        'password': "",
        'mode': 'naive'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data.get('bypassed_filter') is True
    assert data['user'] is not None

def test_tc14_inline_comment_bypasses_naive_filter(client):
    """TC14: Inline comments 'admin'/**/oR/**/1=1--' bypasses whitespace and keyword checks."""
    res = client.post('/lab/filter', json={
        'username': "admin'/**/oR/**/1=1--",
        'password': "",
        'mode': 'naive'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    assert data.get('bypassed_filter') is True
    assert data['user']['username'] == 'admin'

def test_tc15_secure_mode_neutralizes_all_bypasses(client):
    """TC15: Secure mode parameterized queries stop obfuscated payload completely."""
    res = client.post('/lab/filter', json={
        'username': "admin'/**/oR/**/1=1--",
        'password': "",
        'mode': 'secure'
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is False
    assert data['user'] is None
