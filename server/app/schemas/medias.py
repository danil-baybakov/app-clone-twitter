from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MediaSchemaAddResponse(BaseModel):
    result: Literal[True] = Field(
        ...,
        title="Положительный статус запроса",
        description="Положительный статус запроса",
    )
    media_id: int = Field(
        ..., title="id медиафайла", description="id медиафайла", gt=0
    )


class MediaSchemaAddModel(BaseModel):
    file_name: str = Field(
        ...,
        title="Имя медиафайла",
        description="Ммя медиафайла",
    )
    file_body: bytes = Field(
        ...,
        title="Медиафайл",
        description="Медиафайл",
    )
    tweet_id: int = Field(
        None,
        title="id твитта которому принадлежит медиафайл",
        description="id твитта которому принадлежит медиафайл",
    )

    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )


class MediaSchemaModel(MediaSchemaAddModel):
    id: int = Field(
        ..., title="id медиафайла", description="id медиафайла", gt=0
    )
