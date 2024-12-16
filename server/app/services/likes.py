from schemas.likes import LikeSchemaAddModel, LikeSchemaModel
from services.base import BaseService
from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class LikeService(BaseService):
    """
    Класс предоставляет сервис работы с БД
    для операций с лайками на твитты
    """

    def __init__(self, like_repo: AbstractRepository):
        super().__init__(like_repo)

    async def get_like_by_id(self, id: int) -> LikeSchemaModel | None:
        """
        Метод позволяет получить из БД информацию
        о лайке на твитт по id лайка
        :param id: id лайка
        :return: объект с данными лайка на твитт
        """
        try:
            like = await self.repo.find_one_or_none(id=id)
            if like:
                return like.to_read_model()
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных лайка с id={id} из БД."
            )

    async def get_like_by_tweet_id_with_user_id(
        self, tweet_id: int, user_id: int
    ) -> LikeSchemaModel | None:
        """
        Метод позволяет получить из БД информацию
        о лайке на твитт по id твитта и id пользователя
        :param tweet_id: id твитта
        :param user_id: id пользователя
        :return: объект с данными лайка на твитт
        """
        try:
            like = await self.repo.find_one_or_none(
                tweet_id=tweet_id, user_id=user_id
            )
            if like:
                return like.to_read_model()
            return None
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении данных лайка с id={id} и "
                f"user_id={user_id} из БД. "
            )

    async def add_like(self, like: LikeSchemaAddModel) -> int | None:
        """
        Метод добавления лайка к твитту в БД
        :param like: объект с информацией о новом лайке
        :return: id нового лайка или None если операция не прошла
        """
        try:
            return await self.repo.add_one(like.model_dump())
        except Exception:
            raise DatabaseException(
                message="При добавлении данных лайка в БД произошла ошибка."
            )

    async def delete_like(self, tweet_id: int, user_id: int) -> bool:
        """
        Метод удаления лайка с твитта в БД по
        id твитта и id пользователя
        :param tweet_id: id твитта
        :param user_id: id пользователя
        :return: True если операция прошла успешно, иначе False
        """
        try:
            return await self.repo.delete_all(
                tweet_id=tweet_id, user_id=user_id
            )
        except Exception:
            raise DatabaseException(
                message="При удалении данных лайка из БД произошла ошибка."
            )
