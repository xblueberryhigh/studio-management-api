from fastapi import FastAPI
from app.routes.clients import router as clients_router
from app.routes.rooms import router as rooms_router
from app.routes.bookings import router as bookings_router
from app.routes.auth import router as auth_router

app = FastAPI()

app.include_router(clients_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Studio Booking API running"}

#TODO:
# Overlap check in booking_service (two request at the same time)
# Add simple field validation for ClientCreate and RoomCreate
# Add pydantic validation in schemas (more precise data parsing)
# Improve booking conflic handling at the DB/Transaction level

