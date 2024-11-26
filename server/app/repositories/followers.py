from models.followers import Follower
from utils.repository import SQLAlchemyRepository


class FollowerRepository(SQLAlchemyRepository):
    model = Follower
