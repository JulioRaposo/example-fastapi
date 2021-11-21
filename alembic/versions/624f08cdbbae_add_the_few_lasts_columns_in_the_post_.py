"""add the few lasts columns in the post table

Revision ID: 624f08cdbbae
Revises: a697e0a28a5d
Create Date: 2021-11-20 19:00:59.196123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '624f08cdbbae'
down_revision = 'a697e0a28a5d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
