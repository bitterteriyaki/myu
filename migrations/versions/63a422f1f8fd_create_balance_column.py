"""
Revision ID: 63a422f1f8fd
Revises: edcdc0ae504f
Create Date: 2024-08-24 18:32:36.627827
"""

from collections.abc import Sequence

from alembic.op import add_column, alter_column, drop_column
from sqlalchemy import BigInteger, Column

revision: str = "63a422f1f8fd"
down_revision: str | None = "edcdc0ae504f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    add_column(
        "users",
        Column("balance", BigInteger(), server_default="0", nullable=False),
    )
    alter_column("users", "exp", server_default="0", nullable=False)


def downgrade() -> None:
    drop_column("users", "balance")
    alter_column("users", "exp", server_default=None, nullable=False)
