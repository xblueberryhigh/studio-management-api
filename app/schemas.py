from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class UserRegister(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr
    password: str = Field(min_length=5, max_length=100)

    @field_validator("first_name", "last_name", "email", mode="before")
    @classmethod
    def strip_and_validate_strings(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Cannot be blank")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value == "":
            raise ValueError("Cannot be blank")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=100)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Email cannot be blank")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value == "":
            raise ValueError("Password cannot be blank")
        return value


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class ClientCreate(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value


class RoomCreate(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value


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

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


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
