"""updated the telegram_id column in the tg_user table

Revision ID: 521a5f542737
Revises: 0c5a16686def
Create Date: 2025-10-22 18:11:18.986626

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "521a5f542737"
down_revision: Union[str, None] = "0c5a16686def"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "tg_users",
        "telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "tg_users",
        "telegram_id",
        existing_type=sa.BIGINT(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
