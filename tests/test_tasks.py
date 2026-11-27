import pytest


def test_create_task_returns_201(client):
    response = client.post("/tasks", json={"title": "Write report"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Write report"
    assert body["status"] == "todo"


def test_invalid_status_is_rejected(client):
    response = client.post(
        "/tasks", json={"title": "Write report", "status": "invalid"}
    )

    assert response.status_code == 422


def test_blank_title_is_rejected(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_title_too_long_is_rejected(client):
    response = client.post("/tasks", json={"title": "x" * 201})

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_unknown_id_returns_404(client, method):
    kwargs = {"json": {"status": "done"}} if method == "patch" else {}
    response = getattr(client, method)("/tasks/42", **kwargs)

    assert response.status_code == 404


def test_non_positive_id_is_rejected(client):
    response = client.get("/tasks/0")

    assert response.status_code == 422


def test_client_cannot_set_id(client):
    response = client.post("/tasks", json={"title": "Write report", "id": 999})

    assert response.status_code == 422


def test_patch_status_changes_only_status(client):
    client.post("/tasks", json={"title": "Write report", "description": "v1"})

    response = client.patch("/tasks/1", json={"status": "done"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "done"
    assert body["title"] == "Write report"
    assert body["description"] == "v1"


def test_patch_null_title_is_rejected(client):
    client.post("/tasks", json={"title": "Write report"})

    response = client.patch("/tasks/1", json={"title": None})

    assert response.status_code == 422


def test_delete_then_get_returns_404(client):
    client.post("/tasks", json={"title": "Write report"})

    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404
