"""make link unique

Revision ID: 0002
Revises: 0001
Create Date: 2021-05-13 15:45:33.957455

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(None, "audio_books", ["link"])


def downgrade() -> None:
    op.drop_constraint(None, "audio_books", type_="unique")
