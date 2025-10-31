"""rename two column with booking table

Revision ID: 1d1fddd6e93f
Revises: 521a5f542737
Create Date: 2025-10-31 16:05:17.806999

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1d1fddd6e93f"
down_revision: Union[str, None] = "521a5f542737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("booking", sa.Column("start_time", sa.Time(), nullable=False))
    op.add_column("booking", sa.Column("end_time", sa.Time(), nullable=False))
    op.drop_column("booking", "end_date")
    op.drop_column("booking", "start_date")


def downgrade() -> None:
    op.add_column(
        "booking",
        sa.Column("start_date", postgresql.TIME(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "booking",
        sa.Column("end_date", postgresql.TIME(), autoincrement=False, nullable=False),
    )
    op.drop_column("booking", "end_time")
    op.drop_column("booking", "start_time")
