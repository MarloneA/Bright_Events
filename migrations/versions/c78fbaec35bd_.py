"""empty message

Revision ID: c78fbaec35bd
Revises: 0f168eb74fcb
Create Date: 2018-01-18 08:47:50.276463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c78fbaec35bd'
down_revision = '0f168eb74fcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_unique_constraint(None, 'user', ['public_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('blacklist_token')
    # ### end Alembic commands ###
