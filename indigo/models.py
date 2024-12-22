from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase): ...


class Address(Base): 
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)

    street: Mapped[str] = mapped_column(String(50))
    town: Mapped[str] = mapped_column(String(50))
    county: Mapped[str] = mapped_column(String(50))
    postcode: Mapped[str] = mapped_column(String(10))


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    trade: Mapped[str] = mapped_column(String(50))
    rate: Mapped[float] = mapped_column()
    address: Mapped[Address] = mapped_column(ForeignKey("address.id"), nullable=True)
    phone: Mapped[str] = mapped_column(String(20))
    # email: str

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=True)
    client: Mapped["Client"] = relationship("Client", back_populates="workers")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    trade: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))

    workers: Mapped[List["Worker"]] = relationship(
        "Worker", back_populates="client", cascade="all, delete-orphan"
    )

    address: Mapped[Address] = mapped_column(ForeignKey("address.id"), nullable=True)
    # contact: Contact
    # is_agency: bool

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"




class ClientContact: ...


class ClientPayroll: ...


class WorkerPayroll: ...
