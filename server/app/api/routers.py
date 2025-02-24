from api.default import router as default_router
from api.medias import router as medias_router
from api.tweets import router as tweets_router
from api.users import router as users_router

all_routers = [
    default_router,
    medias_router,
    tweets_router,
    users_router,
]
