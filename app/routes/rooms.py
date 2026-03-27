from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Room
from app.schemas import RoomCreate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.post("", response_model=RoomResponse)
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
