"""init db

Revision ID: 3683af61c4e1
Revises:
Create Date: 2025-02-25 10:20:34.877146

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3683af61c4e1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "followers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id_follower", sa.Integer(), nullable=False),
        sa.Column("user_id_following", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "user_id_follower != user_id_following", name="_user_follower_neq"
        ),
        sa.ForeignKeyConstraint(
            ["user_id_follower"], ["users.id"], ondelete="cascade"
        ),
        sa.ForeignKeyConstraint(
            ["user_id_following"], ["users.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint(
            "user_id_follower", "user_id_following", name="_user_follower_uc"
        ),
    )
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "likes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tweet_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tweet_id"], ["tweets.id"], ondelete="cascade"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("tweet_id", "user_id", name="user_tweet_uc"),
    )
    op.create_table(
        "medias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_body", postgresql.BYTEA(), nullable=True),
        sa.Column("tweet_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tweet_id"], ["tweets.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("medias")
    op.drop_table("likes")
    op.drop_table("tweets")
    op.drop_table("followers")
    op.drop_table("users")
    # ### end Alembic commands ###
