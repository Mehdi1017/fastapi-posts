"""empty message

Revision ID: 838190f0f081
Revises: c385954cd30a
Create Date: 2023-02-12 16:59:05.139985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '838190f0f081'
down_revision = 'c385954cd30a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
