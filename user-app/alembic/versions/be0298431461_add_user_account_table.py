"""Add user_account table

Revision ID: be0298431461
Revises: 
Create Date: 2023-08-25 21:50:56.336122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be0298431461'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_account',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String),
    )


def downgrade() -> None:
    op.drop_table('user_account')
