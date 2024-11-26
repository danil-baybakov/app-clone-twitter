from db.db import Base
from schemas.users import UserSchemaModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    user_tweets: Mapped[list["Tweet"]] = relationship(  # noqa: F821
        back_populates="user_tweet", cascade="all, delete-orphan"
    )

    user_likes: Mapped[list["Like"]] = relationship(  # noqa: F821
        back_populates="user_like", cascade="all, delete-orphan"
    )

    user_list_follower: Mapped[list["Follower"]] = relationship(  # noqa: F821
        back_populates="user_follower",
        primaryjoin="User.id==Follower.user_id_follower",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    user_list_following: Mapped[list["Follower"]] = relationship(  # noqa: F821
        back_populates="user_following",
        primaryjoin="User.id==Follower.user_id_following",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_read_model(self) -> UserSchemaModel:
        return UserSchemaModel(
            id=self.id,
            api_key=self.api_key,
            name=self.name,
        )

    __table_args__ = {"keep_existing": True}
