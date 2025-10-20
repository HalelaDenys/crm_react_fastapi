from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Booking


class TgUser(Base):
    __tablename__ = "tg_users"

    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR(15), nullable=True, unique=True)

    first_name: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking", back_populates="tg_user"
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, telegram_id={self.telegram_id}, "
            f"phone_number={self.phone_number}, first_name={self.first_name}, "
            f"last_name={self.last_name}, username={self.username}, "
            f"is_active={self.is_active})"
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
