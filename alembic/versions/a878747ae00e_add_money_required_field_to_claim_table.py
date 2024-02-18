"""add money_required field to claim table

Revision ID: a878747ae00e
Revises: c53211901938
Create Date: 2024-02-15 13:36:09.868019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a878747ae00e'
down_revision: Union[str, None] = 'c53211901938'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('claim', sa.Column('money_required', sa.DECIMAL(precision=10, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('claim', 'money_required')
    # ### end Alembic commands ###
