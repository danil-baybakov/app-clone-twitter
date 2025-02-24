import os
from contextlib import asynccontextmanager

import uvicorn
from api.dependencies import user_service
from api.routers import all_routers
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from schemas.errors import ErrorSchemaResponse, ErrorSchemaValidation
from utils.exceptions import (
    ClientHTTPException,
    CustomHTTPException,
    ServerHTTPException,
)
from utils.fake_data import USERS

tags_metadata = [
    {"name": "tweets", "description": "Операции с твитами"},
    {"name": "medias", "description": "Операции с файлами"},
    {"name": "users", "description": "Операции с пользователями"},
]

responses = {
    500: {"model": ErrorSchemaResponse},
    422: {"model": ErrorSchemaValidation},
    401: {"model": ErrorSchemaResponse},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.environ["ENV"] = "MAIN"
    if await user_service().is_empty():
        await user_service().add_all(USERS)
    yield
    pass


app = FastAPI(
    title="Application Clone Twitter",
    description="",
    summary="Бэкенд корпоративного сервиса микроблогов",
    version="0.0.1",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    responses=responses,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # print(request.headers)
    pass
    return await call_next(request)
    pass


@app.exception_handler(ServerHTTPException)
@app.exception_handler(ClientHTTPException)
async def http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.error_type,
            "error_message": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "result": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        },
    )


@app.exception_handler(RequestValidationError)
@app.exception_handler(ResponseValidationError)
async def request_validation_exception_handler(
    request: Request, exc: ValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "result": False,
            "error_type": type(exc).__name__,
            "error_message": jsonable_encoder(exc.errors()),
        },
    )


for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=5000)
