from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_task():
    response = client.post("/tasks", json={"id": 1, "title": "Test task"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_delete_task():
    client.post("/tasks", json={"id": 2, "title": "To delete"})
    response = client.delete("/tasks/2")
    assert response.status_code == 204