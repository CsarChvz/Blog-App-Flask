"""empty message

Revision ID: 4f8b381176e1
Revises: da20280410b8
Create Date: 2021-07-02 20:25:55.899256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8b381176e1'
down_revision = 'da20280410b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###
