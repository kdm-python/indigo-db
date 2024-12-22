from fastapi import APIRouter
from sqlalchemy.orm import Session
from indigo.models import Worker

from indigo.database import connect_to_db

router = APIRouter(
    prefix="/workers", 
    tags=["workers"],
)

# Dependency inject db connection

router.get("/")
def get_all_workers():
    engine = connect_to_db()
    with Session(engine) as session:
        workers = session.query(Worker).all()
        return workers

