"""Votes Migration

Revision ID: 8de688490f58
Revises: a091c1bd6e92
Create Date: 2022-03-09 18:42:48.915935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8de688490f58'
down_revision = 'a091c1bd6e92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('downvotes', sa.Column('downvote', sa.Integer(), nullable=True))
    op.add_column('upvotes', sa.Column('upvote', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('upvotes', 'upvote')
    op.drop_column('downvotes', 'downvote')
    # ### end Alembic commands ###