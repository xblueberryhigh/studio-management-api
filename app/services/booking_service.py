from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models import Booking, Client, Room
from app.schemas import BookingCreate
from datetime import datetime

def create_booking(db: Session, booking: BookingCreate) -> Booking:
    get_client_or_404(db, booking.client_id)
    get_room_or_404(db, booking.room_id)
    validate_booking_time_range(booking.start_time, booking.end_time)
    ensure_room_is_available(
        db,
        booking.room_id,
        booking.start_time,
        booking.end_time,
    )

    new_booking = Booking(
        client_id=booking.client_id,
        room_id=booking.room_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status=booking.status.value,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return get_booking_with_relations(db, new_booking.id)


def get_client_or_404(db: Session, client_id: int) -> Client:
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def get_room_or_404(db: Session, room_id: int) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def validate_booking_time_range(start_time: datetime, end_time: datetime) -> None:
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Invalid time range")


def ensure_room_is_available(db: Session, room_id: int, start_time: datetime, end_time: datetime) -> None:
    existing_bookings = db.query(Booking).filter(Booking.room_id == room_id).all()

    for existing in existing_bookings:
        overlap = not (
            end_time <= existing.start_time or
            start_time >= existing.end_time
        )

        if overlap:
            raise HTTPException(status_code=400, detail="Room already booked for this time")


def get_booking_with_relations(db: Session, booking_id: int) -> Booking:
    booking = (
        db.query(Booking)
        .options(joinedload(Booking.client), joinedload(Booking.room))
        .filter(Booking.id == booking_id)
        .first()
    )
    return booking
