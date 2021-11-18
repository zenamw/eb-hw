import pytest

from flask_app import app

@pytest.fixture
def client():
    yield app.test_client()
