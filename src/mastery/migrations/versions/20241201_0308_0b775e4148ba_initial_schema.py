"""Initial schema

Revision ID: 0b775e4148ba
Revises: 
Create Date: 2024-12-01 03:08:02.923300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b775e4148ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('problem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.Column('week', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('test_cases', sa.JSON(), nullable=False),
    sa.Column('starter_code', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('problem')
    # ### end Alembic commands ###
