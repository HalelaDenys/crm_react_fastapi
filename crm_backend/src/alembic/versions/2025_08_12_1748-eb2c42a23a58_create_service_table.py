"""create Service table

Revision ID: eb2c42a23a58
Revises: ab96bdd8904c
Create Date: 2025-08-12 17:48:31.452553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eb2c42a23a58"
down_revision: Union[str, None] = "ab96bdd8904c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
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
        sa.CheckConstraint(
            "duration_minutes BETWEEN 1 AND 999",
            name=op.f("ck_services_duration_constraint"),
        ),
        sa.CheckConstraint(
            "price BETWEEN 1 AND 999999", name=op.f("ck_services_price_constraint")
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_services_category_id_categories"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
    )


def downgrade() -> None:
    op.drop_table("services")
