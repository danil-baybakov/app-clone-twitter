from pydantic import BaseModel, ConfigDict, Field


class FollowerSchemaAddModel(BaseModel):
    user_id_follower: int = Field(
        ...,
        title="id подписывающего пользователя",
        description="id подписывающего пользователя",
        gt=0,
    )
    user_id_following: int = Field(
        ...,
        title="id подписываемого пользователя",
        description="id подписываемого пользователя",
        gt=0,
    )

    model_config = ConfigDict(from_attributes=True)


class FollowerSchemaModel(FollowerSchemaAddModel):
    id: int = Field(..., title="id подписки", description="id подписки", gt=0)
