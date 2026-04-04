import os
import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv(".env.test")

DATABASE_URL=os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

from app.database import Base, get_db
from app.main import app
from app.models import User
from app.security import hash_password

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
    command.upgrade(alembic_cfg, "head")

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def register_user(
    client,
    first_name: str = "Alice",
    last_name: str = "Sandler",
    email: str = "alicesandler@gmail.com",
    password: str = "12345",
):
    return client.post(
        "/auth/register",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )

def login_user(
    client,
    email: str = "alicesandler@gmail.com",
    password: str = "12345",
):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

def auth_headers(client):
    response = login_user(client)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client, db):
    admin_user = User(
        first_name="Admin",
        last_name="User",
        email="admin@gmail.com",
        hashed_password=hash_password("admin123"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    response = login_user(client, email="admin@gmail.com", password="admin123")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
