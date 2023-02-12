"""add foreign key to post table

Revision ID: 376696b0bb06
Revises: 838190f0f081
Create Date: 2023-02-12 17:14:54.671345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '376696b0bb06'
down_revision = '838190f0f081'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
     local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
