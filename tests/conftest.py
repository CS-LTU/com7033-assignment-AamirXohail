# tests/conftest.py
import os
import sys

import pytest

# Ensure project root is on sys.path so "import app" works
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_hospital_app  # noqa: E402


@pytest.fixture
def app():
    """
    Create a fresh Flask app instance for tests.
    CSRF is disabled so tests can submit forms if needed.
    """
    flask_app = create_hospital_app()
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    return flask_app


@pytest.fixture
def client(app):
    """
    Flask test client.
    """
    with app.test_client() as client:
        with app.app_context():
            yield client
