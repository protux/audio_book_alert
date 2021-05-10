"""add audio books table

Revision ID: 0001
Revises: 
Create Date: 2021-05-10 08:46:46.896115

"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "audio_books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subtitle", sa.String(), nullable=True),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("reader", sa.String(), nullable=False),
        sa.Column("play_time", sa.String(), nullable=True),
        sa.Column("release_date", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("link", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("audio_books")
