import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Report a Community Issue" in response.data

def test_post_issue(client):
    response = client.post("/", data={"description": "Pothole on Main St.", "location": "Main St."})
    assert response.status_code == 200
    assert b"Pothole on Main St." in response.data

