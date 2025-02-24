from schemas.followers import FollowerSchemaAddModel, FollowerSchemaModel
from services.base import BaseService
from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class FollowerService(BaseService):
    """
    Класс предоставляет сервис работы с БД
    для операций подписок на пользователей
    """

    def __init__(self, follower_repo: AbstractRepository):
        super().__init__(follower_repo)

    async def add_following(self, following: FollowerSchemaAddModel) -> int:
        """
        Метод создает подписку на другого пользователя в БД
        :param following: объект с данными для подписки
        :return: id новой подписки если
        операция прошла успешно, иначе None
        """
        try:
            return await self.repo.add_one(following.model_dump())
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при добавлении данных подписки на"
                f"пользователя с id={following.user_id_following} в БД."
            )

    async def delete_following(
        self, user_id_follower: int, user_id_following: int
    ) -> bool:
        """
        Метод удаляет подписку на другого пользователя в БД
        :param user_id_follower: id пользователя подписывающего
        :param user_id_following: id пользователя подписываемого
        :return: True если операция прошла успешно, иначе False
        """
        try:
            return await self.repo.delete_all(
                user_id_follower=user_id_follower,
                user_id_following=user_id_following,
            )
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при удалении данных подписки на"
                f"пользователя с id={user_id_following} из БД."
            )

    async def get_following(
        self, user_id_follower: int, user_id_following: int
    ) -> FollowerSchemaModel:
        """
        Метод получения информации о подписке из БД по
        id пользователя подписывающего и id пользователя подписываемого
        :param user_id_follower: id пользователя подписывающего
        :param user_id_following: id пользователя подписываемого
        :return: объект с информации о подписке в
        случае успешной операции, иначе None
        """
        try:
            user_following = await self.repo.find_one_or_none(
                user_id_follower=user_id_follower,
                user_id_following=user_id_following,
            )
            if user_following:
                return user_following.to_read_model()
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных подписки"
                f"пользователя с id={user_id_follower} на"
                f"пользователя с id={user_id_following} из БД."
            )
