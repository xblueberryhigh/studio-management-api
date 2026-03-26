from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Client, Room
from app.schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


#Bookings
@router.get("", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@router.post("", response_model=BookingResponse)
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
