# tests/test_auth_flow.py

def test_login_page_loads(client):
    """
    Login page should be reachable.
    """
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    # Basic sanity check on page content
    assert b"<form" in resp.data


def test_register_page_loads(client):
    """
    Register page should be reachable.
    """
    resp = client.get("/auth/register")
    assert resp.status_code == 200
    # Basic sanity check on page content
    assert b"<form" in resp.data
