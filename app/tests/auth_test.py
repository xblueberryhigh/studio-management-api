def test_register_user_success(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Sandler"
    assert data["email"] == "alicesandler@gmail.com"
    assert data["role"] == "user"
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    first_register = client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    assert first_register.status_code == 200

    second_register = client.post(
        "/auth/register",
        json={
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "alicesandler@gmail.com",
            "password": "54321",
        },
    )

    assert second_register.status_code == 400
    assert second_register.json()["detail"] == "Email already exists"


def test_register_rejects_blank_first_name(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "   ",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    assert response.status_code == 422
    assert "Cannot be blank" in str(response.json()["detail"])


def test_register_rejects_blank_last_name(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "   ",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    assert response.status_code == 422
    assert "Cannot be blank" in str(response.json()["detail"])


def test_register_rejects_blank_email(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "   ",
            "password": "12345",
        },
    )

    assert response.status_code == 422
    assert "Cannot be blank" in str(response.json()["detail"])


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "1234",
        },
    )

    assert response.status_code == 422
    assert "at least 5 characters" in str(response.json()["detail"])


def test_register_trims_names_and_email(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "  Alice  ",
            "last_name": "  Sandler  ",
            "email": "  alicesandler@gmail.com  ",
            "password": "12345",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Sandler"
    assert data["email"] == "alicesandler@gmail.com"


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"


def test_login_rejects_blank_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "   ",
            "password": "12345",
        },
    )

    assert response.status_code == 422
    assert "Email cannot be blank" in str(response.json()["detail"])


def test_login_rejects_blank_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "alicesandler@gmail.com",
            "password": "",
        },
    )

    assert response.status_code == 422
    assert "at least 1 character" in str(response.json()["detail"])


def test_login_accepts_email_with_surrounding_spaces(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "  alicesandler@gmail.com  ",
            "password": "12345",
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"



def test_login_unknown_email(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )
    
    response = client.post(
        "/auth/login",
        json={
            "email": "bobmarley@gmail.com",
            "password": "12345",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "Sandler",
            "email": "alicesandler@gmail.com",
            "password": "12345",
        },
    )
    
    response = client.post(
        "/auth/login",
        json={
            "email": "alicesandler@gmail.com",
            "password": "54321",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
