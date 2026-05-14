def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client):
    response = client.post("/tasks", json={"title": "test"})
    assert response.status_code == 201


def test_create_task_fails(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
