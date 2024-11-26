from config import setting
from schemas.tweets import TweetSchema, TweetSchemaAddModel, TweetSchemaModel
from utils.exceptions import DatabaseException
from utils.repository import AbstractRepository


class TweetService:
    """
    Класс предоставляет сервис работы с БД для операций с твиттами
    """

    def __init__(self, tweet_repo: AbstractRepository):
        self.tweet_repo: AbstractRepository = tweet_repo()

    async def add_tweet(self, tweet: TweetSchemaAddModel) -> int | None:
        """
        Метод добавления твитта в БД
        :param tweet: объект с данными твитта
        :return: id нового твитта
        """
        try:
            return await self.tweet_repo.add_one(tweet.model_dump())
        except Exception:
            raise DatabaseException(
                message="Ошибка при добавлении твитта в БД."
            )

    async def get_tweets_full_info(self) -> list[TweetSchema]:
        """
        Метод получения списка твиттов из БД
        :return: список объектов в данными твитта
        """
        try:
            tweet_models = await self.tweet_repo.find_all()

            tweets = []
            for tweet in tweet_models:
                attachments = []
                for media in tweet.tweet_medias:
                    attachments.append(f"{setting.BASE_URI}/medias/{media.id}")
                likes = []
                for like in tweet.tweet_likes:
                    likes.append(
                        {
                            "user_id": like.user_like.id,
                            "name": like.user_like.name,
                        }
                    )
                tweets.append(
                    TweetSchema.model_validate(
                        {
                            "id": tweet.id,
                            "content": tweet.content,
                            "attachments": attachments,
                            "author": {
                                "id": tweet.user_tweet.id,
                                "name": tweet.user_tweet.name,
                            },
                            "likes": likes,
                        }
                    )
                )

            return tweets
        except Exception:
            raise DatabaseException(
                message="Ошибка при получении списка твиттов из БД."
            )

    async def get_tweet_by_id(self, id: int) -> TweetSchemaModel | None:
        """
        Метод получения твитта по id
        :param id: id твитта
        :return: объект с данными твитта
        """
        try:
            tweet = await self.tweet_repo.find_one_or_none(id=id)
            if tweet:
                return tweet.to_read_model()
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении твитта с id={id} из БД."
            )

    async def get_tweet_by_id_with_user_id(
        self, id: int, user_id: int
    ) -> TweetSchemaModel | None:
        """
        Метод получения твитта по id твитта и id пользователя
        :param id: id твитта
        :param user_id: id пользователя
        :return: объект с данными твитта
        """
        try:
            tweet = await self.tweet_repo.find_one_or_none(
                id=id, user_id=user_id
            )
            if tweet:
                return tweet.to_read_model()
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при получении твитта с id={id} "
                f"и user_id={user_id} из БД."
            )

    async def delete_tweet_by_id(self, id: int) -> bool:
        """
        Метод удаления твитта по id
        :param id: id твитта
        :return: если удаление произошло то True, иначе False
        """
        try:
            return await self.tweet_repo.delete_all(id=id)
        except Exception:
            raise DatabaseException(
                message=f"Ошибка при удалении твитта с id={id} из БД."
            )
