"""create Tg user table

Revision ID: 783d5f75107f
Revises: 6993b906e0ec
Create Date: 2025-09-01 17:06:57.966313

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "783d5f75107f"
down_revision: Union[str, None] = "6993b906e0ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tg_users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.VARCHAR(length=15), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("username", sa.VARCHAR(length=50), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tg_users")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_tg_users_phone_number")),
        sa.UniqueConstraint("telegram_id", name=op.f("uq_tg_users_telegram_id")),
    )

    op.add_column("booking", sa.Column("tg_user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_booking_tg_user_id_tg_users"),
        "booking",
        "tg_users",
        ["tg_user_id"],
        ["id"],
        ondelete="SET DEFAULT",
    )
    op.drop_column("booking", "telegram_id")


def downgrade() -> None:
    op.add_column(
        "booking",
        sa.Column("telegram_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_booking_tg_user_id_tg_users"), "booking", type_="foreignkey"
    )
    op.drop_column("booking", "tg_user_id")
    op.drop_table("tg_users")
