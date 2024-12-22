from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from indigo.database import init_db
from indigo.api.routers import client, worker

engine = init_db()

app = FastAPI()

# create_db_and_tables()
#
app.include_router(worker.router)
app.include_router(client.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def welcome():
    return {"message": "Welcome to the PySocial backend API"}
