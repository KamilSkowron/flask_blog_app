"""added profile pic

Revision ID: 5478d276d26a
Revises: 2bfafffd943a
Create Date: 2022-05-12 19:04:35.896372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5478d276d26a'
down_revision = '2bfafffd943a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###