"""Add tokens relationship

Revision ID: 359127789f0c
Revises: ad62e474c434
Create Date: 2025-04-24 12:42:25.832736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '359127789f0c'
down_revision: Union[str, None] = 'ad62e474c434'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
