from app.tests.conftest import auth_headers, register_user


def test_create_booking_without_token_returns_401(client):
    response = client.post(
        "/bookings",
        json={
            "client_id": 1,
            "room_id": 1,
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
    )

    assert response.status_code == 401


def test_create_booking(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_create_response = client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_create_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    booking_create_response = client.post(
        "/bookings",
        json={
            "client_id": client_create_response.json()["id"],
            "room_id": room_create_response.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    assert booking_create_response.status_code == 200

    data = booking_create_response.json()
    assert data["client"]["id"] == client_create_response.json()["id"]
    assert data["room"]["id"] == room_create_response.json()["id"]
    assert data["start_time"] == "2026-04-02T10:00:00"
    assert data["end_time"] == "2026-04-02T12:00:00"
    assert data["status"] == "confirmed"


def test_get_bookings_without_token_returns_401(client):
    response = client.get("/bookings")

    assert response.status_code == 401


def test_get_created_bookings(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_1 = client.post("/clients", json={"name": "Alice"}, headers=headers)
    client_2 = client.post("/clients", json={"name": "Bob"}, headers=headers)
    client_3 = client.post("/clients", json={"name": "Charlie"}, headers=headers)

    room_1 = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)
    room_2 = client.post("/rooms", json={"name": "Room B"}, headers=admin_headers)

    client.post(
        "/bookings",
        json={
            "client_id": client_1.json()["id"],
            "room_id": room_1.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    client.post(
        "/bookings",
        json={
            "client_id": client_2.json()["id"],
            "room_id": room_1.json()["id"],
            "start_time": "2026-04-02T12:00:00",
            "end_time": "2026-04-02T14:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    client.post(
        "/bookings",
        json={
            "client_id": client_3.json()["id"],
            "room_id": room_2.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    response = client.get("/bookings", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3

    assert data[0]["client"]["name"] == "Alice"
    assert data[0]["room"]["name"] == "Room A"
    assert data[0]["status"] == "confirmed"

    assert data[1]["client"]["name"] == "Bob"
    assert data[1]["room"]["name"] == "Room A"
    assert data[1]["status"] == "confirmed"

    assert data[2]["client"]["name"] == "Charlie"
    assert data[2]["room"]["name"] == "Room B"
    assert data[2]["status"] == "confirmed"


def test_forbid_booking_with_unknown_client(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_1 = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": 999,
            "room_id": room_1.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_forbid_booking_with_unknown_room(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_1 = client.post("/clients", json={"name": "Alice"}, headers=headers)
    client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": client_1.json()["id"],
            "room_id": 999,
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found"


def test_forbid_booking_with_invalid_time_range(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_create_response = client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_create_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": client_create_response.json()["id"],
            "room_id": room_create_response.json()["id"],
            "start_time": "2026-04-02T12:00:00",
            "end_time": "2026-04-02T10:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )  

    assert response.status_code == 422
    assert "end_time must be after start_time" in str(response.json()["detail"])


def test_forbid_booking_with_equal_start_and_end_time(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_create_response = client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_create_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": client_create_response.json()["id"],
            "room_id": room_create_response.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T10:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 422
    assert "end_time must be after start_time" in str(response.json()["detail"])


def test_forbid_booking_with_invalid_status(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_create_response = client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_create_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": client_create_response.json()["id"],
            "room_id": room_create_response.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "rescheduled",
        },
        headers=headers,
    )

    assert response.status_code == 422
    assert "confirmed" in str(response.json()["detail"])
    assert "cancelled" in str(response.json()["detail"])
    assert "pending" in str(response.json()["detail"])


def test_create_booking_with_pending_status(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_create_response = client.post("/clients", json={"name": "Alice"}, headers=headers)
    room_create_response = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    response = client.post(
        "/bookings",
        json={
            "client_id": client_create_response.json()["id"],
            "room_id": room_create_response.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "pending",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_forbid_overlapping_booking_for_same_room(client, admin_headers):
    register_user(client)
    headers = auth_headers(client)

    client_1 = client.post("/clients", json={"name": "Alice"}, headers=headers)
    client_2 = client.post("/clients", json={"name": "Bob"}, headers=headers)
    room_1 = client.post("/rooms", json={"name": "Room A"}, headers=admin_headers)

    first_booking = client.post(
        "/bookings",
        json={
            "client_id": client_1.json()["id"],
            "room_id": room_1.json()["id"],
            "start_time": "2026-04-02T10:00:00",
            "end_time": "2026-04-02T12:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    response = client.post(
        "/bookings",
        json={
            "client_id": client_2.json()["id"],
            "room_id": room_1.json()["id"],
            "start_time": "2026-04-02T11:00:00",
            "end_time": "2026-04-02T13:00:00",
            "status": "confirmed",
        },
        headers=headers,
    )

    assert first_booking.status_code == 200
    assert response.status_code == 400
    assert response.json()["detail"] == "Room already booked for this time"
