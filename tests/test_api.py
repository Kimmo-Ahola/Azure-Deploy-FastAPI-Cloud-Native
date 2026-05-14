def test_create_task(client):
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
    assert data["category"] is None
    assert "id" in data
    assert "created_at" in data
