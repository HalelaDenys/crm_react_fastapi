"""create employees table

Revision ID: 1380640658cf
Revises: bb46aa110880
Create Date: 2025-06-08 23:03:35.233404

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1380640658cf"
down_revision: Union[str, None] = "bb46aa110880"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "employees",
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("patronymic", sa.VARCHAR(length=50), nullable=True),
        sa.Column("email", sa.VARCHAR(length=50), nullable=True),
        sa.Column("phone_number", sa.VARCHAR(length=50), nullable=False),
        sa.Column(
            "position",
            sa.Enum(
                "manager",
                "painter",
                "accountant",
                "mechanic",
                name="employee_position_enum",
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_employees")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_employees_phone_number")),
    )


def downgrade() -> None:
    op.drop_table("employees")
