from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class BaseService:
    """
    Базовый класс сервиса работы с БД
    """

    def __init__(self, repo: AbstractRepository):
        self.repo: AbstractRepository = repo()

    async def count(self):
        """
        Метод подсчитывает кол-во записей в таблице БД
        :return: кол-во записей в таблице БД
        """
        try:
            return await self.repo.count()
        except Exception:
            raise DatabaseException(
                message="Подсчет кол-ва записей в таблице БД - ошибка запроса."
            )

    async def add_all(self, items: list[dict]):
        """
        Метод добавляет в таблицу БД список объектов с данными
        :param items: список объектов с данными
        :return:
        """
        try:
            return await self.repo.add_all(items)
        except Exception:
            raise DatabaseException(
                message="Добавление списка объектов в таблицу БД  "
                "- ошибка запроса."
            )

    async def is_empty(self):
        """
        Метод проверяет что таблица БД пуста
        :return: если таблица БД пуста возвращает True, иначе False
        """
        return await self.repo.count() == 0
