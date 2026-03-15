"""add is_active to plans

Revision ID: a1b2c3d4e5f6
Revises: 6aef7ade5428
Create Date: 2026-03-15 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '65014483815f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('workout_plans', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('saved_diet_plans', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade() -> None:
    op.drop_column('saved_diet_plans', 'is_active')
    op.drop_column('workout_plans', 'is_active')
