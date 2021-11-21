"""add a column to posts table

Revision ID: 2cd0fbc9e083
Revises: a5496d7582b8
Create Date: 2021-11-20 13:05:24.692754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd0fbc9e083'
down_revision = 'a5496d7582b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', "content")
    pass
