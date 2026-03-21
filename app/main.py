from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from enum import Enum
from datetime import datetime

app = FastAPI()

class ClientCreate(BaseModel):
    name: str

class RoomCreate(BaseModel):
    name: str


class BookingStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    pending = "pending"

class BookingCreate(BaseModel):
    client_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus

clients = [
    {"id": 1,
    "name": "Client A"},

    {"id": 2, 
    "name": "Client B"}
]

rooms = [
        {"id": 1, 
        "name": "Room A"},

        {"id": 2,
        "name": "Room B"}
    ]

bookings = [
        {"id": 1, 
        "client_id": 1, 
        "room_id": 2,
        "start_time": datetime(2026, 3, 21, 14, 0),
        "end_time": datetime(2026, 3, 21, 16, 0),
        "status": "confirmed"}
    ]

@app.get("/")
def root():
    return {"message": "Studio Booking API running"}

#Clients
@app.get("/clients")
def get_clients():
    return clients

@app.post("/clients")
def create_client(client: ClientCreate):
    new_client= {
        "id": len(clients)+1,
        "name": client.name
    }
    clients.append(new_client)
    return {
        "message": "Client created successfully",
        "client": new_client
    }

#Rooms
@app.get("/rooms")
def get_rooms():
    return rooms

@app.post("/rooms")
def create_room(room: RoomCreate):
    new_room= {
        "id": len(rooms)+1,
        "name": room.name
    }
    rooms.append(new_room)
    return {
        "message": "Room created successfully",
        "room": new_room
    }

#Bookings
@app.get("/bookings")
def get_bookings():
    return bookings

@app.post("/bookings")
def create_booking(booking: BookingCreate):

    client_exists = any(c["id"] == booking.client_id for c in clients)
    room_exists = any(r["id"] == booking.room_id for r in rooms)


    if not client_exists:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if not room_exists:
        raise HTTPException(status_code=404, detail="Room not found")
    

    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="Invalid time range")
    
    for b in bookings:
        same_room = b["room_id"] == booking.room_id

        overlap = not (
            booking.end_time <= b["start_time"] or
            booking.start_time >= b["end_time"]
        )

        if same_room and overlap:
            raise HTTPException(
                status_code=400,
                detail="Room already booked for this time"
            )


    new_booking = {
        "id": len(bookings)+1,
        "client_id": booking.client_id,
        "room_id": booking.room_id,
        "start_time": booking.start_time,
        "end_time": booking.end_time,
        "status": booking.status.value
    }
    bookings.append(new_booking)
    return{
        "message": "Booking created successfully",
        "booking": new_booking
    }

# TODO: Split schemas.py out of main.py
# TODO: Implement databases