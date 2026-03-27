# Studio Booking API

A backend API built with FastAPI and PostgreSQL to manage studio clients, rooms, and bookings.

## Features

- Create and list clients
- Create and list rooms
- Create and list bookings
- Validate booking status
- Prevent overlapping bookings for the same room
- Validate client and room existence before creating a booking

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## Project Structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
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
- `GET /clients`
- `POST /clients`
- `GET /rooms`
- `POST /rooms`
- `GET /bookings`
- `POST /bookings`

## Notes

- Tables are currently created automatically on startup with SQLAlchemy.
- Environment variables are loaded from the `.env` file.
- This project is still being refactored and improved as part of my backend learning journey.

## Future Improvements

- Handle database integrity errors cleanly
- Add tests
- Add Alembic migrations
- improve overlap check in booking_service (two request at the same time)
- Add pydantic validation in schemas
