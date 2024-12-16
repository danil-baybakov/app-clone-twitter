import io
import random

from PIL import Image

rand_image = {
    "mode": "RGB",
    "size": (random.randint(100, 1000), random.randint(100, 1000)),
    "color": random.choice(["green", "red", "yellow"]),
}

static_image = {
    "mode": "RGB",
    "size": (5, 5),
    "color": "green",
}


def mock_image(image_params: dict[str, any]) -> bytes:
    image = Image.new(**image_params)
    byte_array = io.BytesIO()
    image.save(byte_array, format="png")
    return byte_array.getvalue()


USERS = [
    {"name": "TestUser", "api_key": "test"},
    {"name": "Danil Baybakov", "api_key": "danil"},
    {"name": "Egor Egorov", "api_key": "egor"},
    {"name": "Sergey Sergeev", "api_key": "sergey"},
]

TWEETS = [
    {"user_id": 2, "content": "Hello"},
    {"user_id": 3, "content": "Hello"},
    {"user_id": 4, "content": "Hello"},
    {"user_id": 2, "content": "Test"},
    {"user_id": 3, "content": "Test2"},
    {"user_id": 4, "content": "Hello"},
]

MEDIAS = [
    {
        "file_name": "image1.png",
        "file_body": mock_image(rand_image),
        "tweet_id": 4,
    },
    {
        "file_name": "image2.png",
        "file_body": mock_image(rand_image),
        "tweet_id": 4,
    },
    {
        "file_name": "image3.png",
        "file_body": mock_image(static_image),
        "tweet_id": 5,
    },
]

LIKES = [
    {"tweet_id": 4, "user_id": 3},
    {"tweet_id": 6, "user_id": 3},
]

FOLLOWERS = [
    {"user_id_follower": 2, "user_id_following": 3},
    {"user_id_follower": 4, "user_id_following": 3},
    {"user_id_follower": 3, "user_id_following": 2},
]
