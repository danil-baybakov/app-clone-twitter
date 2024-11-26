from typing import Literal

from pydantic import BaseModel, Field


class SuccessSchemaResponse(BaseModel):
    result: Literal[True] = Field(
        ...,
        title="Положительный статус запроса",
        description="Положительный статус запроса",
    )
