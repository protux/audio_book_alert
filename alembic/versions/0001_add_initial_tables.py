"""add initial tables

Revision ID: 0001
Revises: 
Create Date: 2021-05-11 21:19:47.756539

"""
from alembic import op
import sqlalchemy as sa

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
        sa.Column(
            "time_added",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "telegram_subscriptions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chat_id"),
        sa.UniqueConstraint("chat_id"),
    )


def downgrade():
    op.drop_table("telegram_subscriptions")
    op.drop_table("audio_books")
