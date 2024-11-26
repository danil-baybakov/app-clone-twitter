from models.tweets import Tweet
from utils.repository import SQLAlchemyRepository


class TweetRepository(SQLAlchemyRepository):
    model = Tweet
