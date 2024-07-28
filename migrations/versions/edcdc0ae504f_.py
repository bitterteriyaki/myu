"""
Revision ID: edcdc0ae504f
Revises:
Create Date: 2024-07-28 17:37:41.203863
"""

from collections.abc import Sequence

from alembic.op import create_table, drop_table
from sqlalchemy import BigInteger, Column, PrimaryKeyConstraint

revision: str = "edcdc0ae504f"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    create_table(
        "users",
        Column("id", BigInteger(), nullable=False),
        Column("exp", BigInteger(), nullable=False),
        PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    drop_table("users")
