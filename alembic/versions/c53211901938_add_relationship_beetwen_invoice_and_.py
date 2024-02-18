"""add relationship beetwen invoice and claim

Revision ID: c53211901938
Revises: a2693a4c5ca1
Create Date: 2024-02-15 13:23:08.734932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c53211901938'
down_revision: Union[str, None] = 'a2693a4c5ca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('claim', sa.Column('invoice_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'claim', 'invoice', ['invoice_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'claim', type_='foreignkey')
    op.drop_column('claim', 'invoice_id')
    # ### end Alembic commands ###
