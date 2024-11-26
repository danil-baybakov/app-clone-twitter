from typing import Literal

from pydantic import BaseModel, Field


class ValidationErrorSchema(BaseModel):
    loc: list[str | int] = Field(
        ...,
        title="Местоположение ошибки валидации данных",
        description="Местоположение ошибки валидации данных",
    )
    msg: str = Field(
        ...,
        title="Описание ошибки валидации данных",
        description="Описание ошибки валидации данных",
    )
    type: str = Field(
        ...,
        title="Тип ошибки валидации данных",
        description="Тип ошибки валидации данных",
    )


class ErrorSchema(BaseModel):
    result: Literal[False] = Field(
        ...,
        title="Отрицательный статус запроса",
        description="Отрицательный статус запроса",
    )
    error_type: str = Field(..., title="Тип ошибки", description="Тип ошибки")


class ErrorSchemaResponse(ErrorSchema):
    error_message: str = Field(
        ..., title="Описание ошибки", description="Описание ошибки"
    )


class ErrorSchemaValidation(ErrorSchema):
    error_message: list[ValidationErrorSchema] = Field(
        ...,
        title="Список ошибок валидации данных",
        description="Список ошибок валидации данных",
    )
