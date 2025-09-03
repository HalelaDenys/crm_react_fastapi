from infrastructure import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Employee


class Position(Base):
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True, default="emp")

    employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="position"
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
