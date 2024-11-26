from db.db import Base
from schemas.tweets import TweetSchemaModel
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    content = mapped_column(TEXT, nullable=True)

    tweet_medias: Mapped[list["Media"]] = relationship(  # noqa: F821
        back_populates="tweet_media",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    tweet_likes: Mapped[list["Like"]] = relationship(  # noqa: F821
        back_populates="tweet_like",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    user_tweet: Mapped["User"] = relationship(  # noqa: F821
        back_populates="user_tweets", lazy="selectin"
    )

    def to_read_model(self) -> TweetSchemaModel:
        return TweetSchemaModel(
            id=self.id,
            user_id=self.user_id,
            content=self.content,
        )
