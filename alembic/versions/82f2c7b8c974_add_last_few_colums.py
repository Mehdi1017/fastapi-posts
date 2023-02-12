"""add last few colums

Revision ID: 82f2c7b8c974
Revises: 376696b0bb06
Create Date: 2023-02-12 17:22:22.646782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82f2c7b8c974'
down_revision = '376696b0bb06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
