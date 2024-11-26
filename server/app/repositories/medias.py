from models.medias import Media
from utils.repository import SQLAlchemyRepository


class MediaRepository(SQLAlchemyRepository):
    model = Media
