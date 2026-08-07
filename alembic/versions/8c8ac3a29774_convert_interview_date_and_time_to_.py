"""convert interview date and time to proper types

Revision ID: 8c8ac3a29774
Revises: c539c9d3e83d
Create Date: 2026-08-07 13:40:27.342407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c8ac3a29774'
down_revision: Union[str, Sequence[str], None] = 'c539c9d3e83d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert date column from VARCHAR to Date with explicit USING clause
    op.execute("""
        ALTER TABLE interviews 
        ALTER COLUMN date TYPE DATE 
        USING CASE 
            WHEN date IS NULL OR date = '' THEN NULL 
            ELSE date::DATE 
        END
    """)
    
    # Convert time column from VARCHAR to Time with explicit USING clause
    op.execute("""
        ALTER TABLE interviews 
        ALTER COLUMN time TYPE TIME 
        USING CASE 
            WHEN time IS NULL OR time = '' THEN NULL 
            ELSE time::TIME 
        END
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Convert back to VARCHAR (cast to text)
    op.execute("ALTER TABLE interviews ALTER COLUMN time TYPE VARCHAR USING time::VARCHAR")
    op.execute("ALTER TABLE interviews ALTER COLUMN date TYPE VARCHAR USING date::VARCHAR")
