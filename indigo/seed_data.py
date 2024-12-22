from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker

from models import (
    Base,
    Worker,
    Client,
    Address
)  # Assuming your models are in a file named `models.py`
from database import init_db

# Configure the database URL (adjust as necessary)
DATABASE_URL = "sqlite:///indigo.db"  # Example: SQLite database

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables (if not already created)
Base.metadata.create_all(engine)

# Initialize Faker
fake = Faker()


# Function to create fake clients
def create_fake_clients(session, num_clients=10):
    clients = []
    for _ in range(num_clients):
        client = Client(
            name=fake.company(),
            trade=fake.job()[:20],  # Limit trade to 20 characters
        )
        session.add(client)
        clients.append(client)
    session.commit()
    return clients


# Function to create fake workers
def create_fake_workers(session, clients, num_workers=50):
    for _ in range(num_workers):
        client = fake.random.choice(clients)  # Assign worker to a random client
        worker = Worker(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            trade=fake.job()[:30],  # Limit trade to 30 characters
            rate=round(fake.random.uniform(15.0, 50.0), 2),  # Random hourly rate
            client_id=client.id,  # Link worker to client
        )
        session.add(worker)
    session.commit()


# Main script
if __name__ == "__main__":
    init_db()
    with Session(engine) as session:
        # Generate and insert fake clients
        clients = create_fake_clients(session, num_clients=10)

        # Generate and insert fake workers
        create_fake_workers(session, clients, num_workers=50)

    print("Test data inserted successfully!")
