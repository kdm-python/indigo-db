from sqlalchemy import Engine

from indigo.database import connect_to_db

def test_database_connection():
    engine = connect_to_db()
    assert isinstance(engine, Engine)
