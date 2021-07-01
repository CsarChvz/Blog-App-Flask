"""empty message

Revision ID: 1ab0e9d10152
Revises: 78f2d199dc23
Create Date: 2021-07-01 14:44:08.409475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ab0e9d10152'
down_revision = '78f2d199dc23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###