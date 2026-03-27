from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes.clients import router as clients_router
from app.routes.rooms import router as rooms_router
from app.routes.bookings import router as bookings_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(clients_router)
app.include_router(rooms_router)
app.include_router(bookings_router)

@app.get("/")
def root():
    return {"message": "Studio Booking API running"}

# tests (pytest) 

# Add pytest
# Add API tests for bookings
# Prove these cases:
# booking is created successfully
# missing client returns 404
# missing room returns 404
# invalid time range returns 400
# overlapping booking returns 400

# Overlap check in booking_service (two request at the same time)
# Add simple field validation for ClientCreate and RoomCreate
# Schema migrations with Alembic (?)
# Add pydantic validation in schemas (more precise data parsing)
# Improve booking conflic handling at the DB/Transaction level

