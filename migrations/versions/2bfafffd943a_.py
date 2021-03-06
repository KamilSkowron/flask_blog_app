"""empty message

Revision ID: 2bfafffd943a
Revises: 2b7882faef73
Create Date: 2022-05-12 15:50:43.959457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bfafffd943a'
down_revision = '2b7882faef73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_author', sa.Text(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'about_author')
    # ### end Alembic commands ###
