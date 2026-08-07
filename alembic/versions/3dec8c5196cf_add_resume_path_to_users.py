"""add resume path to users

Revision ID: 3dec8c5196cf
Revises: a37e930e3e00
Create Date: 2026-08-07 11:53:44.423157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3dec8c5196cf'
down_revision: Union[str, Sequence[str], None] = 'a37e930e3e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # resume_path already included in initial migration — no-op
    pass


def downgrade() -> None:
    pass
