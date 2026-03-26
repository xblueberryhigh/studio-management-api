from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate, ClientResponse

router=APIRouter(prefix="/clients", tags=["clients"])

#Clients
@router.get("", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client= Client(name=client.name)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
