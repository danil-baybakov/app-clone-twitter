from fastapi import UploadFile
from schemas.medias import MediaSchemaAddModel, MediaSchemaModel
from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class MediaService:
    """
    Класс предоставляет сервис работы с БД
    для операций с медиа
    """

    def __init__(self, media_repo: AbstractRepository):
        self.media_repo: AbstractRepository = media_repo()

    async def add_media(self, file: UploadFile) -> int:
        """
        Метод позволяет добавить новый медиафайл в БД
        :param file: новый медиафайл
        :return: id нового медиафайла
        """
        try:
            new_media_dict = MediaSchemaAddModel(
                file_name=file.filename, file_body=file.file.read()
            ).model_dump()
            return await self.media_repo.add_one(new_media_dict)
        except Exception:
            raise DatabaseException(
                message="Ошибка при добавлении медиафайла в БД."
            )

    async def get_media_by_id(self, id: int) -> MediaSchemaModel | None:
        """
        Метод позволяет получить данные медиафайла из БД по id
        :param id: id медиафайла
        :return: объект с данными медиафайла или
        None если медиафайла в БД нет
        """
        try:
            media = await self.media_repo.find_one_or_none(id=id)
            if media:
                return media.to_read_model()
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении медиафайла с id={id} из БД."
            )

    async def add_tweet_id_for_medias(
        self, ids: list[int], tweet_id: int
    ) -> bool:
        """
        Метод позволяет добавить списку медиафайлов
        в БД id твитта которому они принадлежат
        :param ids: список id медиафайлов
        :param tweet_id: id твитта
        :return: True если операция успешна, иначе False
        """
        try:
            return await self.media_repo.update_all_by_ids(
                ids, tweet_id=tweet_id
            )
        except Exception:
            raise DatabaseException(
                message="Ошибка при добавлении id твита в медиафайлы в БД."
            )
