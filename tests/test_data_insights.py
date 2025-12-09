# tests/test_data_insights.py

def test_home_redirects_to_login_when_anonymous(client):
    """
    The landing route should not show data to anonymous users.
    It should redirect them to the login page.
    """
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")


def test_protected_data_route_redirects_when_anonymous(client):
    """
    Example of a protected data-related route: patients list.
    This stands in for insights/analytics behaviour in tests.
    """
    resp = client.get("/patients/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")
