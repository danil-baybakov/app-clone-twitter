from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from schemas.users import UserSchemaLike, UserSchemaSimple


class TweetSchemaAddRequest(BaseModel):
    tweet_data: str = Field(
        ...,
        title="Содержание твитта",
        description="Содержание твитта",
    )
    tweet_media_ids: list[int] = Field(
        ...,
        title="Список id медиафайлов твитта",
        description="Список id медиафайлов твитта",
    )


class TweetSchemaAddResponse(BaseModel):
    result: Literal[True] = Field(
        ...,
        title="Положительный статус запроса",
        description="Положительный статус запроса",
    )
    tweet_id: int = Field(
        ..., title="id нового твитта", description="id нового твитта", gt=0
    )


class TweetSchema(BaseModel):
    id: int = Field(..., title="id твитта", description="id твитта", gt=0)
    content: str = Field(
        ...,
        title="Содержание твитта",
        description="Содержание твитта",
    )
    attachments: list[str] = Field(
        ...,
        title="Список ссылок на медиафайлы твитта",
        description="Список ссылок на медиафайлы твитта",
    )
    author: UserSchemaSimple = Field(
        ...,
        title="Объект с данными автора твитта",
        description="Объект с данными автора твитта",
    )
    likes: list[UserSchemaLike] = Field(
        ...,
        title="Список объектов с данными лайков на твитт",
        description="Список объектов с данными лайков на твитт",
    )


class TweetSchemaResponse(BaseModel):
    result: Literal[True] = Field(
        ...,
        title="Положительный статус запроса",
        description="Положительный статус запроса",
    )
    tweets: list[TweetSchema] = Field(
        ...,
        title="Список объектов с данными твиттов",
        description="Список объектов с данными твиттов",
    )


class TweetSchemaAddModel(BaseModel):
    content: str = Field(
        ...,
        title="Содержание твитта",
        description="Содержание твитта",
    )
    user_id: int = Field(
        ...,
        title="id пользователя создавшего твитт",
        description="id пользователя создавшего твитт",
        gt=0,
    )

    model_config = ConfigDict(from_attributes=True)


class TweetSchemaModel(TweetSchemaAddModel):
    id: int = Field(..., title="id твитта", description="id твитта", gt=0)
