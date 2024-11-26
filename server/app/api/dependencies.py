from typing import Annotated

from fastapi import Depends, Header, HTTPException
from repositories.followers import FollowerRepository
from repositories.likes import LikeRepository
from repositories.medias import MediaRepository
from repositories.tweets import TweetRepository
from repositories.users import UserRepository
from services.followers import FollowerService
from services.likes import LikeService
from services.medias import MediaService
from services.tweets import TweetService
from services.users import UserService
from utils.exceptions import ClientHTTPException


async def get_token_header(x_token: Annotated[str, Header()]) -> None:
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str) -> None:
    if token != "****":
        raise HTTPException(status_code=400, detail="No **** token provided")


def user_service() -> UserService:
    return UserService(UserRepository)


def tweet_service() -> TweetService:
    return TweetService(TweetRepository)


def media_service() -> MediaService:
    return MediaService(MediaRepository)


def follower_service() -> FollowerService:
    return FollowerService(FollowerRepository)


def like_service() -> LikeService:
    return LikeService(LikeRepository)


async def get_user(
    api_key: Annotated[
        str, Header(description="api_key текущего пользователя")
    ],
    user_service: Annotated[UserService, Depends(user_service)],
) -> int:
    user = await user_service.get_user_by_api_key(api_key)
    if not user:
        raise ClientHTTPException(status_code=401, detail="Unauthorised user")
    return user.id
