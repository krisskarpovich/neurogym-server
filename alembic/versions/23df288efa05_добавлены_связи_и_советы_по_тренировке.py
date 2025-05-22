"""Добавлены связи и советы по тренировке

Revision ID: 23df288efa05
Revises: 06965c4eac05
Create Date: 2025-04-25 17:04:53.743445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23df288efa05'
down_revision: Union[str, None] = '06965c4eac05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
