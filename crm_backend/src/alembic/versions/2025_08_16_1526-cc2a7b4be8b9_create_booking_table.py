"""create Booking Table

Revision ID: cc2a7b4be8b9
Revises: eb2c42a23a58
Create Date: 2025-08-16 15:26:06.513940

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc2a7b4be8b9"
down_revision: Union[str, None] = "eb2c42a23a58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "booking",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("booking_date", sa.Date(), nullable=False),
        sa.Column("start_date", sa.Time(), nullable=False),
        sa.Column("end_date", sa.Time(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            name=op.f("fk_booking_service_id_services"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_booking_user_id_users"),
            ondelete="SET DEFAULT",
        ),
        sa.PrimaryKeyConstraint("service_id", "id", name=op.f("pk_booking")),
    )


def downgrade() -> None:
    op.drop_table("booking")
