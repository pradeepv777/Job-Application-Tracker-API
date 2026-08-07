"""convert interview date and time to proper types

Revision ID: 8c8ac3a29774
Revises: c539c9d3e83d
Create Date: 2026-08-07 13:40:27.342407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8c8ac3a29774'
down_revision: Union[str, Sequence[str], None] = 'c539c9d3e83d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # date and time already defined as Date/Time in initial migration — no-op
    pass


def downgrade() -> None:
    pass
