"""add relationship with client and product

Revision ID: 10f76efc9bfd
Revises: a878747ae00e
Create Date: 2024-02-15 20:15:59.219375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '10f76efc9bfd'
down_revision: Union[str, None] = 'a878747ae00e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('client_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'product', 'client', ['client_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'client_id')
    # ### end Alembic commands ###