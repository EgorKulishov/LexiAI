"""empty message

Revision ID: e8724e716c41
Revises: 65bc312348f1
Create Date: 2024-10-17 20:40:53.942469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8724e716c41'
down_revision: Union[str, None] = '65bc312348f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'books', ['book_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='unique')
    # ### end Alembic commands ###
