def test_create_room(client):
    response = client.post("/rooms", json={"name": "Room A"})

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Room A"


def test_forbid_duplicate_room_name(client):
    first_response = client.post("/rooms", json={"name": "Room A"})
    second_response = client.post("/rooms", json={"name": "Room A"})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Room name already exists"


def test_get_created_rooms(client):
    client.post("/rooms", json={"name": "Room A"})
    client.post("/rooms", json={"name": "Room B"})

    response = client.get("/rooms")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Room A"
    assert data[1]["name"] == "Room B"
