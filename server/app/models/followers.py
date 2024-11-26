from db.db import Base
from schemas.followers import FollowerSchemaModel
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Follower(Base):
    __tablename__ = "followers"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    user_id_follower: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    user_id_following: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    user_follower: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys="Follower.user_id_follower",
        back_populates="user_list_follower",
        lazy="joined",
    )

    user_following: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys="Follower.user_id_following",
        back_populates="user_list_following",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id_follower", "user_id_following", name="_user_follower_uc"
        ),
        CheckConstraint(
            "user_id_follower != user_id_following", name="_user_follower_neq"
        ),
    )

    def to_read_model(self) -> FollowerSchemaModel:
        return FollowerSchemaModel(
            id=self.id,
            user_id_follower=self.user_id_follower,
            user_id_following=self.user_id_following,
        )
