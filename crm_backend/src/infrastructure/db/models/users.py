from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Booking


class User(Base):
    first_name: Mapped[str] = mapped_column(VARCHAR(50))
    last_name: Mapped[str] = mapped_column(VARCHAR(50))
    phone_number: Mapped[str] = mapped_column(VARCHAR(15), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, is_active={self.is_active})"
