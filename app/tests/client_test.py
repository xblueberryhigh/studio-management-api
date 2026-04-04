from app.tests.conftest import register_user, auth_headers


def test_create_client_without_token_returns_401(client):
    response = client.post("/clients", json={"name": "Alice"})

    assert response.status_code == 401


def test_create_client(client):
    register_user(client)
    headers = auth_headers(client)

    response = client.post("/clients", json={"name": "Alice"}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == "Alice"


def test_get_clients_without_token_returns_401(client):
    response = client.get("/clients")

    assert response.status_code == 401


def test_get_created_clients(client):
    register_user(client)
    headers = auth_headers(client)

    client.post("/clients", json={"name": "Alice"}, headers=headers)
    client.post("/clients", json={"name": "Bob"}, headers=headers)

    response = client.get("/clients", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"
