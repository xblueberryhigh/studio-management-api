from app.tests.conftest import register_user, auth_headers


def test_create_room(client, admin_headers):
    response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == "Room A"

def test_forbid_duplicate_room_name(client, admin_headers):
    first_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)
    second_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Room name already exists"


def test_create_room_rejects_blank_name(client, admin_headers):
    response = client.post("/rooms", json={"name": "   "}, headers=admin_headers)

    assert response.status_code == 422
    assert "Name cannot be blank" in str(response.json()["detail"])


def test_create_room_trims_name(client, admin_headers):
    response = client.post("/rooms", json={"name": "  Room A  "}, headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Room A"


def test_forbid_duplicate_room_name_after_trimming(client, admin_headers):
    first_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)
    second_response = client.post("/rooms", json={"name": "  Room A  "}, headers=admin_headers)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Room name already exists"


def test_get_created_rooms(client, admin_headers):
    client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)
    client.post("/rooms", json={"name": "Room B"}, headers=admin_headers)

    register_user(client)
    headers = auth_headers(client)
    response = client.get("/rooms", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Room A"
    assert data[1]["name"] == "Room B"

def test_create_room_without_token_returns_401(client):
    response = client.post("/rooms", json={"name": "Room A"})

    assert response.status_code == 401

def test_create_room_as_normal_user_returns_403(client):
    register_user(client)
    headers = auth_headers(client)

    response = client.post("/rooms", json={"name": "Room A"}, headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Access forbidden"


def test_get_rooms_without_token_returns_401(client):
    response = client.get("/rooms")
    assert response.status_code == 401
