from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Position


class Employee(Base):
    first_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    position_id: Mapped[int] = mapped_column(
        ForeignKey("positions.id", ondelete="SET DEFAULT"),
        nullable=False,
        server_default="1",
        default=1,
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)

    position: Mapped["Position"] = relationship(
        "Position",
        back_populates="employees",
    )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, is_active={self.is_active}, "
            f"is_admin={self.is_admin}, phone_number={self.phone_number})"
        )
