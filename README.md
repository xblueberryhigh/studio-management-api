# Studio Booking API

A backend API built with FastAPI and PostgreSQL to manage studio clients, rooms, bookings, and authentication.

## Features

- User registration and login with JWT tokens
- Protected routes with bearer-token authentication
- Admin-only room creation
- Create and list clients
- Create and list rooms
- Create and list bookings
- Request validation with Pydantic schemas
- Trim and reject blank values for user, client, and room input fields
- Validate booking status with enums
- Validate booking time ranges before service logic runs
- Prevent overlapping bookings for the same room
- Validate client and room existence before creating a booking
- Alembic migrations
- Pytest test suite covering auth, clients, rooms, bookings, and validation behavior

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic

## Project Structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  security.py
  routes/
  services/
  tests/
```

## Setup

1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create the PostgreSQL database

```sql
CREATE DATABASE studio_management;
```

4. Create a `.env` file in the project root

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/studio_management
SECRET_KEY=your_generated_secret_key
```

5. Apply database migrations

```bash
alembic upgrade head
```

## Run the Project

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, open:

- http://127.0.0.1:8000/docs

## Endpoints

- `GET /`
- `POST /auth/register`
- `POST /auth/login`
- `GET /clients`
- `POST /clients`
- `GET /rooms`
- `POST /rooms`
- `GET /bookings`
- `POST /bookings`

## Notes

- Database tables are managed through Alembic migrations.
- Environment variables are loaded from `.env` and `.env.test`.
- `GET /clients`, `POST /clients`, `GET /rooms`, `GET /bookings`, and `POST /bookings` require authentication.
- `POST /rooms` requires an authenticated admin user.
- Request-body validation errors are returned as `422 Unprocessable Entity`.
- This project is still being refactored and improved as part of my backend learning journey.

## Testing

Run the test suite with:

```bash
pytest -q
```

The test suite currently covers:

- successful and failing auth flows
- schema validation for blank and malformed input
- role-based room creation rules
- booking conflict and booking time validation
- authenticated access to protected routes

## Future Improvements

- Handle database integrity errors cleanly
- Run tests automatically in CI
- Improve overlap check in booking_service (two request at the same time)
- Add stronger password policy rules during registration
