from fastapi import APIRouter
from sqlalchemy.orm import Session
from indigo.models import Client

from indigo.database import connect_to_db

router = APIRouter(
    prefix="/clients", 
    tags=["clients"],
)


@router.get("/")
def get_all_clients():
    engine = connect_to_db()
    with Session(engine) as session:
        clients = session.query(Client).all()
        return clients

