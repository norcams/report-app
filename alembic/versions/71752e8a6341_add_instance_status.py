"""add instance status and created

Revision ID: 71752e8a6341
Revises: 5c7fb04297cc
Create Date: 2025-02-05 19:55:22.311106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71752e8a6341'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('owners', sa.Column('status', sa.String(16), nullable=False))
    op.add_column('owners', sa.Column('created', sa.DateTime, nullable=False))


def downgrade() -> None:
    op.drop_column('owners', 'status')
    op.drop_column('owners', 'created')
