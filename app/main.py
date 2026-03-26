from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import Base, engine, get_db
from app import models
from app.models import Client, Room, Booking
from app.schemas import ClientCreate, RoomCreate, BookingCreate, ClientResponse, RoomResponse, BookingResponse

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Studio Booking API running"}

#Clients
@app.get("/clients", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.post("/clients", response_model=list[ClientResponse])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client= Client(name=client.name)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

#Rooms
@app.get("/rooms", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@app.post("/rooms", response_model=list[RoomResponse])
def create_room(room: RoomCreate, db: Session = Depends(get_db)):

    new_room= Room(name=room.name)
    db.add(new_room)

    try: 
        db.commit()
        db.refresh(new_room)
        return new_room
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room name already exists")

#Bookings
@app.get("/bookings", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@app.post("/bookings", response_model=list[BookingResponse])
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == booking.client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="Invalid time range")
    
    existing_bookings = db.query(Booking).filter(Booking.room_id == booking.room_id).all()
    for existing in existing_bookings:
        overlap = not (
            booking.end_time <= existing.start_time or
            booking.start_time >= existing.end_time
        )

        if overlap:
            raise HTTPException(status_code=400, detail="Room already booked for this time")


    new_booking = Booking(client_id=booking.client_id, room_id=booking.room_id, start_time=booking.start_time, end_time=booking.end_time, status=booking.status.value)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# Split routes into seperate files
# Add realtionships layer using SQLAlchemy
# Refactor into OOP logic