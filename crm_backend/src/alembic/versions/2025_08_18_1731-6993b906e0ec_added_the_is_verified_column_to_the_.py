"""Added the ‘is_verified’ column to the Booking model.

Revision ID: 6993b906e0ec
Revises: cc2a7b4be8b9
Create Date: 2025-08-18 17:31:42.322563

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6993b906e0ec"
down_revision: Union[str, None] = "cc2a7b4be8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "booking",
        sa.Column("is_verified", sa.Boolean(), server_default="False", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("booking", "is_verified")
