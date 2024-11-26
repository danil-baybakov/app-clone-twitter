from pydantic import BaseModel, ConfigDict, Field


class LikeSchemaAddModel(BaseModel):
    tweet_id: int = Field(
        ...,
        title="id твитта которому принадлежит лайк",
        description="id твитта которому принадлежит лайк",
        gt=0,
    )
    user_id: int = Field(
        ...,
        title="id пользователя который поставил лайк на данный твитт",
        description="id пользователя который поставил лайк на данный твитт",
        gt=0,
    )

    model_config = ConfigDict(from_attributes=True)


class LikeSchemaModel(LikeSchemaAddModel):
    id: int = Field(..., title="id лайка", description="id лайка", gt=0)
