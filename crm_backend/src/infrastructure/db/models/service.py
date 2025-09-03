from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, CheckConstraint, ForeignKey
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from infrastructure import Category, Booking


class Service(Base):
    name: Mapped[str] = mapped_column(VARCHAR(length=255), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="services",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking", back_populates="service"
    )

    __table_args__ = (
        CheckConstraint(
            "duration_minutes BETWEEN 1 AND 999",
            name="duration_constraint",
        ),
        CheckConstraint(
            "price BETWEEN 1 AND 999999",
            name="price_constraint",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name}, duration_minutes={self.duration_minutes}, "
            f"price={self.price}, category_id={self.category_id}),"
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
