from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase): ...


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    trade: Mapped[str] = mapped_column(String(30))
    rate: Mapped[float] = mapped_column()
    # address: Address
    # phone: str
    # email: str

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship("Client", back_populates="workers")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: str
    trade: str

    workers: Mapped[List["Worker"]] = relationship(
        "Worker", back_populates="client", cascade="all, delete-orphan"
    )

    # address: Address
    # contact: Contact
    # phone: str
    # is_agency: bool

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"


"""
Other tables:
    - Trade
    - Address
    - ClientContact
"""
