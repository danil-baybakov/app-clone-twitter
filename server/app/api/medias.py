from typing import Annotated

from api.dependencies import get_user, media_service
from config import setting
from fastapi import APIRouter, Depends, Path, Response, UploadFile
from schemas.errors import ErrorSchemaResponse
from schemas.medias import MediaSchemaAddResponse
from services.medias import MediaService
from utils.exceptions import ClientHTTPException

router = APIRouter(
    prefix=f"{setting.BASE_URI}/medias",
    redirect_slashes=False,
    tags=["medias"],
)


@router.post("")
async def load_files_from_tweet(
    file: UploadFile,
    media_service: Annotated[MediaService, Depends(media_service)],
    user_id=Depends(get_user),
) -> MediaSchemaAddResponse:
    """
    Эндпоинт для добавления медиафайлов к твитту
    :param file: файл
    :param media_service: сервис работы с БД для медиа
    :param user_id: id текущего пользователя
    :return:
    """
    # делаем запрос к БД для добавления медиафайла
    media_id = await media_service.add_media(file)
    return {"result": True, "media_id": media_id}


@router.get("/{id}", responses={404: {"model": ErrorSchemaResponse}})
async def get_files_from_tweet_by_id(
    media_service: Annotated[MediaService, Depends(media_service)],
    id: int = Path(
        ..., title="id медиафайла", description="id медиафайла", gt=0
    ),
) -> bytes:
    """
    Эндпоинт для получения медиафайла по id
    :param id: id медиафайла
    :param media_service: сервис работы с БД для медиа
    :return:
    """
    # делаем запрос к БД для получения медиафайла
    media = await media_service.get_media_by_id(id)
    if media is None:
        raise ClientHTTPException(
            status_code=404, detail=f"Медиафайл с id={id} не найден."
        )
    return Response(
        content=media.file_body,
        headers={
            "Content-Disposition": f"attachment; filename={media.file_name}"
        },
    )
