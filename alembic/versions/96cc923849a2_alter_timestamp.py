"""alter timestamp

Revision ID: 96cc923849a2
Revises: 71752e8a6341
Create Date: 2025-02-05 20:09:58.263344

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '96cc923849a2'
down_revision: Union[str, None] = '71752e8a6341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('instances',
        column_name='timestamp',
        new_column_name='last_script_run',
        existing_type=sa.DateTime,
        existing_server_default=None,
        existing_nullable=False)
    op.alter_column('owners',
        column_name='timestamp',
        new_column_name='last_sync',
        existing_type=sa.DateTime,
        existing_server_default=None,
        existing_nullable=False)

def downgrade() -> None:
    op.alter_column('instances',
        column_name='last_script_run',
        new_column_name='timestamp',
        existing_type=sa.DateTime,
        existing_server_default=None,
        existing_nullable=False)
    op.alter_column('owners',
        column_name='last_sync',
        new_column_name='timestamp',
        existing_type=sa.DateTime,
        existing_server_default=None,
        existing_nullable=False)
