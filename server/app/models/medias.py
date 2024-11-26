from db.db import Base
from schemas.medias import MediaSchemaModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    file_name: Mapped[str] = mapped_column(String(255))
    file_body = mapped_column(BYTEA)
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="cascade"), nullable=True
    )

    tweet_media: Mapped["Tweet"] = relationship(  # noqa: F821
        back_populates="tweet_medias", lazy="selectin"
    )

    def to_read_model(self) -> MediaSchemaModel:
        return MediaSchemaModel(
            id=self.id,
            file_name=self.file_name,
            file_body=self.file_body,
            tweet_id=self.tweet_id,
        )
