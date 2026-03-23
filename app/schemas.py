from datetime import datetime
from enum import Enum

from pydantic import BaseModel


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
