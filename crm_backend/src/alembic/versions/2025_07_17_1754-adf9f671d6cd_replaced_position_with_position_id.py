"""replaced position with position_id

Revision ID: adf9f671d6cd
Revises: cd12271b5f21
Create Date: 2025-07-17 17:54:16.694077

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "adf9f671d6cd"
down_revision: Union[str, None] = "cd12271b5f21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "employees",
        sa.Column("position_id", sa.Integer(), server_default="1", nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_employees_position_id_positions"),
        "employees",
        "positions",
        ["position_id"],
        ["id"],
        ondelete="SET DEFAULT",
    )
    op.drop_column("employees", "position")


def downgrade() -> None:
    op.add_column(
        "employees",
        sa.Column(
            "position",
            postgresql.ENUM(
                "manager",
                "painter",
                "accountant",
                "mechanic",
                name="employee_position_enum",
            ),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        op.f("fk_employees_position_id_positions"), "employees", type_="foreignkey"
    )
    op.drop_column("employees", "position_id")
