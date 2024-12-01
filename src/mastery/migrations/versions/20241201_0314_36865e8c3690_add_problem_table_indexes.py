"""Add problem table indexes

Revision ID: 36865e8c3690
Revises: 0b775e4148ba
Create Date: 2024-12-01 03:14:45.046716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36865e8c3690'
down_revision: Union[str, None] = '0b775e4148ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_problem_topic', 'problem', ['topic'])
    op.create_index('ix_problem_week', 'problem', ['week'])


def downgrade() -> None:
    op.drop_index('ix_problem_topic')
    op.drop_index('ix_problem_week')
