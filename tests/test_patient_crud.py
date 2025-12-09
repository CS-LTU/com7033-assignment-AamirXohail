# tests/test_patient_crud.py

def test_patients_list_requires_login(client):
    """
    Unauthenticated user should be redirected when trying to access patient list.
    """
    resp = client.get("/patients/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")


def test_add_patient_requires_login(client):
    """
    Unauthenticated user should be redirected when trying to access add-patient form.
    """
    resp = client.get("/patients/add", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers.get("Location", "")
