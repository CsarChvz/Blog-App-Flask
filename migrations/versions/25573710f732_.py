"""empty message

Revision ID: 25573710f732
Revises: 6545a8ee9771
Create Date: 2021-07-02 20:41:12.624710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25573710f732'
down_revision = '6545a8ee9771'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'member_since')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('member_since', sa.TEXT(), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
