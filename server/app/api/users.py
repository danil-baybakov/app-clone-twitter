from typing import Annotated

from api.dependencies import follower_service, get_user, user_service
from config import setting
from fastapi import APIRouter, Depends, Path
from schemas.common import SuccessSchemaResponse
from schemas.followers import FollowerSchemaAddModel
from schemas.users import UserSchemaResponse
from services.followers import FollowerService
from services.users import UserService
from utils.exceptions import ClientHTTPException

router = APIRouter(
    prefix=f"{setting.BASE_URI}/users", redirect_slashes=False, tags=["users"]
)


async def get_user_info(
    user_id: int, user_service: UserService
) -> UserSchemaResponse:
    """
    Функция для получения информации о пользователе по id
    :param user_id: id пользователя
    :param user_service: сервис работы с БД для пользователей
    :return:
    """
    # делаем запрос к БД для получения данных пользователя
    user = await user_service.get_user_full_info_by_id(user_id)
    # если нет такого пользователя
    # выдаем исключение и сообщение на фронтенд
    if user is None:
        raise ClientHTTPException(
            status_code=404,
            detail=f"Пользователь с id={user_id} " f"не найден.",
        )
    return {
        "result": True,
        "user": user,
    }


@router.get("/me")
async def get_info_about_your_profile(
    user_service: Annotated[UserService, Depends(user_service)],
    user_id=Depends(get_user),
) -> UserSchemaResponse:
    """
    Эндпоинт для получения информации о своем профиле
    :param user_service: сервис работы с БД для пользователей
    :param user_id: id текущего пользователя
    :return:
    """
    return await get_user_info(user_id, user_service)


@router.get("/{id}")
async def get_info_about_other_profile_by_id(
    user_service: Annotated[UserService, Depends(user_service)],
    id: int = Path(
        ..., title="id пользователя", description="id пользователя"
    ),
) -> UserSchemaResponse:
    """
    Эндпоинт для получения информации о произвольном пользователе по id
    :param id: id пользователя
    :param user_service: сервис работы с БД для пользователей
    :return:
    """
    return await get_user_info(id, user_service)


@router.post("/{id}/follow")
async def follow_user_by_id(
    follower_service: Annotated[FollowerService, Depends(follower_service)],
    id: int = Path(
        ...,
        title="id подписываемого пользователя",
        description="id подписываемого пользователя",
    ),
    user_id=Depends(get_user),
) -> SuccessSchemaResponse:
    """
    Эндпоинт позволяет добавить пользователя в читаемые
    :param id: id пользователя добавляемого в читаемые
    :param follower_service: сервис работы с БД для
    добавления/удаления пользователей в читаемые
    :param user_id: id текущего пользователя
    :return:
    """
    # проверяем добавлен ли уже пользователь в читаемые
    # если уже добавлен, то ничего не меняем в БД
    # выводим положительный результат на фронтенд
    following = await follower_service.get_following(
        user_id_follower=user_id, user_id_following=id
    )
    if following:
        return {"result": True}

    # делаем запрос к БД для добавления пользователя в читаемые
    await follower_service.add_following(
        FollowerSchemaAddModel(user_id_follower=user_id, user_id_following=id)
    )
    return {"result": True}


@router.delete("/{id}/follow")
async def unfollow_user_by_id(
    follower_service: Annotated[FollowerService, Depends(follower_service)],
    id: int = Path(
        ...,
        title="id подписанного пользователя",
        description="id подписанного пользователя",
    ),
    user_id=Depends(get_user),
):
    """
    Эндпоинт позволяет удалять пользователя из читаемых
    :param id: id пользователя удаляемого из читаемых
    :param follower_service: сервис работы с БД
    для добавления/удаления пользователей в читаемые
    :param user_id: id текущего пользователя
    :return:
    """
    result = await follower_service.delete_following(
        user_id_follower=user_id, user_id_following=id
    )
    # делаем запрос к БД для удаления пользователя из читаемых
    if not result:
        raise ClientHTTPException(
            status_code=404,
            detail=f"Пользователь с id={user_id} отсутствует в "
            f"списке читаемых для пользователя с id={id}",
        )
    return {"result": result}
