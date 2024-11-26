from typing import Annotated

from api.dependencies import (
    get_user,
    like_service,
    media_service,
    tweet_service,
)
from config import setting
from fastapi import APIRouter, Depends, Path, status
from schemas.common import SuccessSchemaResponse
from schemas.errors import ErrorSchemaResponse
from schemas.likes import LikeSchemaAddModel
from schemas.tweets import (
    TweetSchemaAddModel,
    TweetSchemaAddRequest,
    TweetSchemaAddResponse,
    TweetSchemaResponse,
)
from services.likes import LikeService
from services.medias import MediaService
from services.tweets import TweetService
from utils.exceptions import ClientHTTPException

router = APIRouter(
    prefix=f"{setting.BASE_URI}/tweets",
    redirect_slashes=False,
    tags=["tweets"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet: TweetSchemaAddRequest,
    tweet_service: Annotated[TweetService, Depends(tweet_service)],
    media_service: Annotated[MediaService, Depends(media_service)],
    user_id=Depends(get_user),
) -> TweetSchemaAddResponse:
    """
    Эндпоинт добавления нового твитта
    :param tweet: объект с данными нового твитта
    :param tweet_service: сервис работы с БД для твиттов
    :param media_service: сервис работы с БД для медиафайлов твитта
    :param user_id: id текущего пользователя
    :return:
    """
    new_tweet_schema = TweetSchemaAddModel(
        user_id=user_id, content=tweet.tweet_data
    )
    # добавляем в таблицу твиттов БД новый твитт
    tweet_id = await tweet_service.add_tweet(new_tweet_schema)

    # в записи таблицы медиафайлов БД для нового твитта добавляем id твитта
    await media_service.add_tweet_id_for_medias(
        tweet.tweet_media_ids, tweet_id
    )

    return {"result": True, "tweet_id": tweet_id}


@router.get("")
async def get_tweets(
    tweet_service: Annotated[TweetService, Depends(tweet_service)],
    user_id=Depends(get_user),
) -> TweetSchemaResponse:
    """
    Эндпоинт получения списка твиттов
    :param tweet_service: сервис работы с БД для твиттов
    :param user_id: id текущего пользователя
    :return:
    """
    # делаем запрос в БД для получения списка твиттов
    tweets = await tweet_service.get_tweets_full_info()
    return {
        "result": True,
        "tweets": tweets,
    }


@router.delete("/{id}", responses={404: {"model": ErrorSchemaResponse}})
async def delete_tweet_by_id(
    tweet_service: Annotated[TweetService, Depends(tweet_service)],
    id: int = Path(..., title="id твитта", description="id твитта"),
    user_id=Depends(get_user),
) -> SuccessSchemaResponse:
    """
    Эндпоинт удаления твитта
    :param id: id твитта
    :param tweet_service: сервис работы с БД для твиттов
    :param user_id: id текущего пользователя
    :return:
    """
    # делаем запрос в БД для удаления твитта
    result = await tweet_service.delete_tweet_by_id(id)
    # если результат запроса отрицательный
    # значит твитта с таким id нет, сообщаем об этом на фронтенд
    if not result:
        raise ClientHTTPException(
            status_code=404, detail=f"Tweet with id={id} not found."
        )
    return {"result": result}


@router.post("/{id}/likes")
async def like_tweet_by_id(
    like_service: Annotated[LikeService, Depends(like_service)],
    tweet_service: Annotated[TweetService, Depends(tweet_service)],
    id: int = Path(..., title="id твитта", description="id твитта"),
    user_id=Depends(get_user),
) -> SuccessSchemaResponse:
    """
    Эндпоинт для добавления пользователем лайка твитту
    :param id: id твитта
    :param like_service: сервис работы с БД для лайков
    :param tweet_service: сервис работы с БД для твиттов
    :param user_id: id текущего пользователя
    :return:
    """
    # делаем проверку на то что пользователь еще не ставил лайк на этот твитт
    # если проверка не пройдена, то ничего не меняем в БД
    # выводим положительный результат на фронтенд
    like = await like_service.get_like_by_tweet_id_with_user_id(
        tweet_id=id, user_id=user_id
    )
    if like:
        return {"result": True}

    # делаем проверку на то что пользователь на свой твитт не ставил лайк
    # если проверка не пройдена, то ничего не меняем в БД
    # выводим положительный результат на фронтенд
    tweet = await tweet_service.get_tweet_by_id_with_user_id(
        id=id, user_id=user_id
    )
    if tweet:
        return {"result": True}

    # делаем запрос к БД для добавления лайка к твитту
    # выводим положительный результат на фронтенд
    new_like_schema = LikeSchemaAddModel(tweet_id=id, user_id=user_id)
    await like_service.add_like(new_like_schema)
    return {"result": True}


@router.delete("/{id}/likes", responses={404: {"model": ErrorSchemaResponse}})
async def unlike_tweet_by_id(
    like_service: Annotated[LikeService, Depends(like_service)],
    tweet_service: Annotated[TweetService, Depends(tweet_service)],
    id: int = Path(..., title="id твитта", description="id твитта"),
    user_id=Depends(get_user),
) -> SuccessSchemaResponse:
    """
    Эндпоинт для удаления пользователем лайка с твитта
    :param id: id твитта
    :param like_service: сервис работы с БД для лайков
    :param tweet_service: сервис работы с БД для твиттов
    :param user_id: id текущего пользователя
    :return:
    """
    # делаем проверку на то что пользователь удаляет лайк не со своего твитта
    # если проверка не пройдена, то ничего не меняем в БД
    # выводим положительный результат на фронтенд
    tweet = await tweet_service.get_tweet_by_id_with_user_id(
        id=id, user_id=user_id
    )
    if tweet:
        return {"result": True}

    # делаем запрос в БД для удаления лайка с твитта
    result = await like_service.delete_like(id, user_id)
    if not result:
        raise ClientHTTPException(
            status_code=404,
            detail=f"Пользователь с id={user_id} не ставил лайк"
            f"на твитт с id={id}.",
        )
    return {"result": result}
