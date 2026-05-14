from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    response = client.post("/tasks", json={"title": "test"})
    assert response.status_code == 201

def test_create_task_fails():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422