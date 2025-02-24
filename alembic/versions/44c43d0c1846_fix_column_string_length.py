"""fix column length for instance name and kernel

Revision ID: 44c43d0c1846
Revises: 96cc923849a2
Create Date: 2025-02-24 12:59:26.995920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44c43d0c1846'
down_revision: Union[str, None] = '96cc923849a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('instances',
        column_name='name',
        type_=sa.String(255),
        existing_nullable=False)
    op.alter_column('instances',
        column_name='kernel',
        type_=sa.String(255))

def downgrade() -> None:
    op.alter_column('instances',
        column_name='name',
        type_=sa.String(127),
        existing_nullable=False)
    op.alter_column('instances',
        column_name='kernel',
        type_=sa.String(127))
