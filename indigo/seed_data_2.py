from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
import random

# Import your model classes here
from models import Base, Address, Worker, Client  # Adjust import path as needed

# Initialize Faker
fake = Faker('en_GB')  # Using UK locale for appropriate postcodes etc.

MYSQL_URL = "mysql+pymysql://root:blackmore@172.17.0.3:3306/indigo"

# Create engine
# engine = create_engine("sqlite:///indigo.db")
engine = create_engine(MYSQL_URL)

# List of common trades for workers
WORKER_TRADES = [
    "Electrician", "Plumber", "Carpenter", "Painter", 
    "Bricklayer", "Plasterer", "Roofer", "General Builder"
]

# List of common trades for clients
CLIENT_TRADES = [
    "Construction", "Property Development", "Estate Management",
    "Facilities Management", "Building Maintenance"
]

def create_address():
    """Create a fake address"""
    return Address(
        street=fake.street_address(),
        town=fake.city(),
        county=fake.county(),
        postcode=fake.postcode()
    )

def create_client(session, address):
    """Create a fake client with the given address"""
    return Client(
        name=fake.company(),
        trade=random.choice(CLIENT_TRADES),
        phone=fake.phone_number(),
        address=address.id
    )

def create_worker(session, client):
    """Create a fake worker associated with the given client"""
    address = create_address()
    session.add(address)
    session.flush()  # To get the address ID
    
    return Worker(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        trade=random.choice(WORKER_TRADES),
        rate=round(random.uniform(20.0, 100.0), 2),
        address=address.id,
        phone=fake.phone_number(),
        client_id=client.id
    )

def seed_database(num_clients=5, min_workers_per_client=2, max_workers_per_client=5):
    """Seed the database with fake data"""
    with Session(engine) as session:
        # Create clients with addresses
        for _ in range(num_clients):
            # Create client address
            client_address = create_address()
            session.add(client_address)
            session.flush()  # To get the address ID
            
            # Create client
            client = create_client(session, client_address)
            session.add(client)
            session.flush()  # To get the client ID
            
            # Create workers for this client
            num_workers = random.randint(min_workers_per_client, max_workers_per_client)
            for _ in range(num_workers):
                worker = create_worker(session, client)
                session.add(worker)
            
        # Commit all changes
        session.commit()

if __name__ == "__main__":
    print("Starting database seeding...")
    seed_database()
    print("Database seeding completed!")
