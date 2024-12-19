import fire
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from indigo.database import init_db
from indigo.models import Worker

# TODO: Consider inheritance, passing in table class. 
# Insert, select and select all will all have the same code.

# Repository pattern
class WorkerRepository:
    """Repository of worker table related operations."""
    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def create_worker(self, firstname: str, lastname: str, trade: str, rate: float) -> Worker:
        with self.session_maker() as session:
            worker = Worker(firstname=firstname, lastname=lastname, trade=trade, rate=rate)
            session.add(worker)
            session.commit()
            return worker

    def get_by_id(self, worker_id: int) -> Optional[Worker]:
        with self.session_maker() as session:
            return session.get(Worker, worker_id)

    def get_all(self) -> List[Worker]:
        with self.session_maker() as session:
            return session.get(Worker)
    
    def find_by_trade(self, trade: str) -> List[Worker]:
        with self.session_maker() as session:
            stmt = select(Worker).where(Worker.trade == trade)
            return session.execute(stmt).scalars().all()
    
    # UPDATE operations
    def update_rate(self, worker_id: int, new_rate: float) -> Optional[Worker]:
        with self.session_maker() as session:
            worker = session.get(Worker, worker_id)
            if worker:
                worker.rate = new_rate
                session.commit()
            return worker
    
    # DELETE operations
    def delete(self, worker_id: int) -> bool:
        with self.session_maker() as session:
            worker = session.get(Worker, worker_id)
            if worker:
                session.delete(worker)
                session.commit()
                return True
            return False

class CLI:
    """The main CLI entry point for the application."""
    def create_worker(self, firstname: str, lastname: str, trade: str, rate: float) -> Worker:
        ...

    def get_worker_by_id(self, worker_id: int) -> Worker:
        ...

    def get_all_workers(self) -> list[Worker]:
        ...


def main():
    ...

if __name__ == "__main__":
    engine = init_db()
    session_maker = sessionmaker(bind=engine)
    worker_repo = WorkerRepository(session_maker)
    fire.Fire(CLI)