"""create interviews table

Revision ID: c539c9d3e83d
Revises: 3dec8c5196cf
Create Date: 2026-08-07 12:15:59.657452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c539c9d3e83d'
down_revision: Union[str, Sequence[str], None] = '3dec8c5196cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # interviews table already included in initial migration — no-op
    pass


def downgrade() -> None:
    pass
