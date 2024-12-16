from schemas.users import UserSchema, UserSchemaModel
from services.base import BaseService
from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class UserService(BaseService):
    """
    Класс предоставляет сервис работы с БД
    для операций с пользователями
    """

    def __init__(self, user_repo: AbstractRepository):
        super().__init__(user_repo)

    async def get_user_by_api_key(
        self, api_key: str
    ) -> UserSchemaModel | None:
        """
        Метод получения информации о пользователе
        из БД по api_key
        :param api_key: api_key пользователя
        :return: объект с данными пользователя
        в случае успешной операции, иначе None
        """
        try:
            user = await self.repo.find_one_or_none(api_key=api_key)
            if user:
                return user.to_read_model()
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных пользователя "
                f"с api_key={api_key} из БД."
            )

    async def get_user_by_id(self, id: str) -> UserSchemaModel | None:
        """
        Метод получения информации о пользователе
        из БД по id
        :param id: id пользователя
        :return: объект с данными пользователя
        в случае успешной операции, иначе None
        """
        try:
            user = await self.repo.find_one_or_none(id=id)
            if user:
                return user.to_read_model()
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных пользователя "
                f"с id={id} из БД."
            )

    async def get_user_full_info_by_id(self, id: int) -> UserSchema | None:
        """
        Метод получения полной информации
        о пользователе из БД по id
        :param id: id пользователя
        :return: объект с полной информацией о пользователе
        в случае успешной операции, иначе None
        """
        try:
            user = await self.repo.find_one_or_none(id=id)
            if user:
                list_user_following = []
                for row_user_following in user.user_list_follower:
                    list_user_following.append(
                        {
                            "id": row_user_following.user_following.id,
                            "name": row_user_following.user_following.name,
                        }
                    )
                list_user_follower = []
                for row_user_follower in user.user_list_following:
                    list_user_follower.append(
                        {
                            "id": row_user_follower.user_follower.id,
                            "name": row_user_follower.user_follower.name,
                        }
                    )
                return UserSchema.model_validate(
                    {
                        "id": user.id,
                        "name": user.name,
                        "followers": list_user_follower,
                        "following": list_user_following,
                    }
                )
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных пользователя "
                f"с id={id} из БД."
            )
