from db.db import Base
from schemas.likes import LikeSchemaModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="cascade")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )

    tweet_like: Mapped["Tweet"] = relationship(  # noqa: F821
        back_populates="tweet_likes", lazy="selectin"
    )

    user_like: Mapped["User"] = relationship(  # noqa: F821
        back_populates="user_likes", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("tweet_id", "user_id", name="user_tweet_uc"),
    )

    def to_read_model(self) -> LikeSchemaModel:
        return LikeSchemaModel(
            id=self.id,
            tweet_id=self.tweet_id,
            user_id=self.user_id,
        )
