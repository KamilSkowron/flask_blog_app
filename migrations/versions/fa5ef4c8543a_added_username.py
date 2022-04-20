"""added username

Revision ID: fa5ef4c8543a
Revises: 6f82a24a12ed
Create Date: 2022-04-20 14:11:00.744473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa5ef4c8543a'
down_revision = '6f82a24a12ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=100), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###