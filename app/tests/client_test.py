def test_create_client(client):
    response = client.post("/clients", json={"name": "Alice"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"


def test_get_created_clients(client):
    client.post("/clients", json={"name": "Alice"})
    client.post("/clients", json={"name": "Bob"})

    response = client.get("/clients")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"