from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserSchemaSimple(BaseModel):
    id: int = Field(
        ..., title="id пользователя", description="id пользователя", gt=0
    )
    name: str = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя",
        min_length=3,
        max_length=50,
    )


class UserSchemaLike(BaseModel):
    user_id: int = Field(
        ..., title="id пользователя", description="id пользователя", gt=0
    )
    name: str = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя",
        min_length=3,
        max_length=50,
    )


class UserSchema(BaseModel):
    id: int = Field(
        ..., title="id пользователя", description="id пользователя", gt=0
    )
    name: str = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя",
        min_length=3,
        max_length=50,
    )
    followers: list[UserSchemaSimple] = Field(
        ...,
        title="Список объектов с данными пользователей "
        "подписанных на данного пользователя",
        description="Список объектов с данными пользователей "
        "подписанных на данного пользователя",
    )
    following: list[UserSchemaSimple] = Field(
        ...,
        title="Список объектов с данными пользователей на "
        "которых подписан данный пользователь",
        description="Список объектов с данными пользователей на "
        "которых подписан данный пользователь",
    )


class UserSchemaResponse(BaseModel):
    result: Literal[True] = Field(
        ...,
        title="Положительный статус запроса",
        description="Положительный статус запроса",
    )
    user: UserSchema = Field(
        ...,
        title="Объект с полной информацией о пользователе",
        description="Объект с полной информацией о пользователе",
    )


class UserSchemaAddModel(BaseModel):
    name: str = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя",
        min_length=3,
        max_length=50,
    )

    model_config = ConfigDict(from_attributes=True)


class UserSchemaModel(UserSchemaAddModel):
    id: int = Field(
        ..., title="id пользователя", description="id пользователя", gt=0
    )
    api_key: str = Field(
        ...,
        title="api_key пользователя",
        description="api_key пользователя",
        min_length=3,
        max_length=50,
    )
