"""add is_chat_with_manager_active to client table

Revision ID: 57244ef263d5
Revises: 10f76efc9bfd
Create Date: 2024-02-17 20:11:41.179898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '57244ef263d5'
down_revision: Union[str, None] = '10f76efc9bfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('is_chat_with_manager_active', sa.Boolean(), nullable=True))

    op.execute(
        """
        UPDATE client
        SET is_chat_with_manager_active = false;
        """
    )
    op.alter_column('client', 'is_chat_with_manager_active', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'is_chat_with_manager_active')
    # ### end Alembic commands ###
