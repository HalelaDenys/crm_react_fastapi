from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from infrastructure import Service


class Category(Base):
    __tablename__ = "categories"

    """
    Table for service categories
    """

    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True)

    services: Mapped[list["Service"]] = relationship(
        "Service",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
