"""Add user progress table

Revision ID: e60e3e3373e2
Revises: 36865e8c3690
Create Date: 2024-12-01 03:17:40.553414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e60e3e3373e2'
down_revision: Union[str, None] = '36865e8c3690'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_progress',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.String(50), nullable=False),
                    sa.Column('problem_id', sa.Integer(), nullable=False),
                    sa.Column('attempts', sa.Integer(),
                              nullable=False, server_default='0'),
                    sa.Column('solved', sa.Boolean(), nullable=False,
                              server_default='false'),
                    sa.Column('last_attempt', sa.DateTime(), nullable=False,
                              server_default=sa.text('CURRENT_TIMESTAMP')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['problem_id'], ['problem.id']),
                    sa.UniqueConstraint('user_id', 'problem_id',
                                        name='unique_user_problem')
                    )
    op.create_index('ix_user_progress_user_id', 'user_progress', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_progress_user_id')
    op.drop_table('user_progress')
