"""Изменение связей между моделями

Revision ID: 45189aca481b
Revises: 23df288efa05
Create Date: 2025-04-25 17:07:34.110154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45189aca481b'
down_revision: Union[str, None] = '23df288efa05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
