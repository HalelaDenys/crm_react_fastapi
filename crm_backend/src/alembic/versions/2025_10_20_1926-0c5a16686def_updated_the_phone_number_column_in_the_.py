"""updated the phone_number column in the tg_user table

Revision ID: 0c5a16686def
Revises: 72d4af6a294b
Create Date: 2025-10-20 19:26:32.242747

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c5a16686def"
down_revision: Union[str, None] = "72d4af6a294b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "tg_users", "phone_number", existing_type=sa.VARCHAR(length=15), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "tg_users", "phone_number", existing_type=sa.VARCHAR(length=15), nullable=False
    )
