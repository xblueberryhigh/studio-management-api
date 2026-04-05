from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


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

class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    client: ClientResponse
    room: RoomResponse