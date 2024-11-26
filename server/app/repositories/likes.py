from models.likes import Like
from utils.repository import SQLAlchemyRepository


class LikeRepository(SQLAlchemyRepository):
    model = Like
