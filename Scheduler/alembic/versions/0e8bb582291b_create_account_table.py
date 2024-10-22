"""create account table

Revision ID: 0e8bb582291b
Revises: 
Create Date: 2024-10-21 13:49:55.048751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e8bb582291b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    'events',     
    sa.column('id', sa.Integer, primary_key=True),
    sa.column('name', sa.String(500), unique=True, index=True),
    sa.column("date", sa.Date, nullable=False),
    sa.column('area',sa.String(500), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('events')
