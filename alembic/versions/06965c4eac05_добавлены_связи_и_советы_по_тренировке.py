"""Добавлены связи и советы по тренировке

Revision ID: 06965c4eac05
Revises: 359127789f0c
Create Date: 2025-04-25 17:01:45.077695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06965c4eac05'
down_revision: Union[str, None] = '359127789f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
