from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72d4af6a294b"
down_revision: Union[str, None] = "783d5f75107f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tg_users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("tg_users", "is_active")
