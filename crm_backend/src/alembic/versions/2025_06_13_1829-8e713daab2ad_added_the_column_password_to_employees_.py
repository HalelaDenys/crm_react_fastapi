"""added the column password to employees table

Revision ID: 8e713daab2ad
Revises: 1380640658cf
Create Date: 2025-06-13 18:29:48.753831

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e713daab2ad"
down_revision: Union[str, None] = "1380640658cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "employees", sa.Column("password", sa.VARCHAR(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("employees", "password")
