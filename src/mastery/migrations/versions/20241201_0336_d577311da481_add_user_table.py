"""Add user table

Revision ID: d577311da481
Revises: e60e3e3373e2
Create Date: 2024-12-01 03:36:54.585361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd577311da481'
down_revision: Union[str, None] = 'e60e3e3373e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(100),
                              unique=True, nullable=False),
                    sa.Column('password_hash', sa.String(200), nullable=False),
                    sa.Column('is_admin', sa.Boolean(),
                              nullable=False, server_default='false'),
                    sa.Column('created_at', sa.DateTime(), nullable=False,
                              server_default=sa.text('CURRENT_TIMESTAMP')),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_user_username')
    op.drop_table('user')
