import pytest
from httpx import AsyncClient
from models.likes import Like
from models.medias import Media
from models.tweets import Tweet
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import (
    check_is_set_tweet_id_medias_db,
    check_row_table_db,
    get_count_row_db,
    get_last_row_id_db,
)

params_test_create_tweet = [
    (None, None, 6, 7, True, 201, {"result": True, "tweet_id": 7}),
    (
        {"api-key": "unauthorized_user"},
        None,
        6,
        6,
        True,
        401,
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
    ),
    (
        None,
        {"tweet_dat": "Тест", "tweet_media_ids": [1, 2, 3]},
        6,
        6,
        True,
        422,
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "input": {
                        "tweet_dat": "Тест",
                        "tweet_media_ids": [1, 2, 3],
                    },
                    "loc": ["body", "tweet_data"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        },
    ),
]


@pytest.mark.parametrize(
    "endpoint_headers, endpoint_request, expected_prev_count_tweets_db, "
    "expected_next_count_tweets_db, "
    "expected_status_check_is_set_tweet_id_medias_db, "
    "expected_status_code, expected_response",
    params_test_create_tweet,
)
async def test_create_tweet(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    gen_medias_db: list[Media],
    endpoint_headers: dict[str, any] | None,
    endpoint_request: dict[str, any] | None,
    expected_prev_count_tweets_db: int,
    expected_next_count_tweets_db: int,
    expected_status_check_is_set_tweet_id_medias_db: bool,
    expected_status_code: int,
    expected_response: dict[str, any],
):
    """
    Тест проверки эндпоинта создания твитта
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param gen_medias_db: фикстура создает в БД записи медиафайлов твитта
    :param endpoint_headers: заголовок запроса
    :param endpoint_request: тело запроса
    :param expected_next_count_tweets_db: ожидаемое кол-во записей в таблице
    твиттов БД до запроса
    :param expected_next_count_tweets_db: ожидаемое кол-во записей в таблице
    твиттов БД после запроса
    :param expected_status_check_is_set_tweet_id_medias_db:
    ожидаемый статус проверки созданных
    записей медиафайлов твитта в БД на наличие id твитта после
    запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    media_ids = [media.id for media in gen_medias_db]
    assert await check_is_set_tweet_id_medias_db(async_db, media_ids, None)

    assert (
        await get_count_row_db(async_db, Tweet)
        == expected_prev_count_tweets_db
    )

    request_success = {"tweet_data": "Тест", "tweet_media_ids": media_ids}

    request_json = endpoint_request

    if endpoint_request is None:
        request_json = request_success

    response = await ac.post(
        "/tweets", json=request_json, headers=endpoint_headers
    )

    next_count_tweets_db = await get_count_row_db(async_db, Tweet)
    assert next_count_tweets_db == expected_next_count_tweets_db

    new_tweet_id = await get_last_row_id_db(async_db, Tweet)

    check_id = None
    if next_count_tweets_db != expected_prev_count_tweets_db:
        check_id = new_tweet_id
    assert (
        await check_is_set_tweet_id_medias_db(async_db, media_ids, check_id)
        == expected_status_check_is_set_tweet_id_medias_db
    )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_get_tweets = [
    (
        None,
        {
            "result": True,
            "tweets": [
                {
                    "id": 1,
                    "content": "Hello",
                    "attachments": [],
                    "author": {"id": 2, "name": "Danil Baybakov"},
                    "likes": [],
                },
                {
                    "id": 2,
                    "content": "Hello",
                    "attachments": [],
                    "author": {"id": 3, "name": "Egor Egorov"},
                    "likes": [],
                },
                {
                    "id": 3,
                    "content": "Hello",
                    "attachments": [],
                    "author": {"id": 4, "name": "Sergey Sergeev"},
                    "likes": [],
                },
                {
                    "id": 4,
                    "content": "Test",
                    "attachments": ["/api/medias/1", "/api/medias/2"],
                    "author": {"id": 2, "name": "Danil Baybakov"},
                    "likes": [{"user_id": 3, "name": "Egor Egorov"}],
                },
                {
                    "id": 5,
                    "content": "Test2",
                    "attachments": ["/api/medias/3"],
                    "author": {"id": 3, "name": "Egor Egorov"},
                    "likes": [],
                },
                {
                    "id": 6,
                    "content": "Hello",
                    "attachments": [],
                    "author": {"id": 4, "name": "Sergey Sergeev"},
                    "likes": [{"user_id": 3, "name": "Egor Egorov"}],
                },
            ],
        },
        200,
    ),
    (
        {"api-key": "unauthorized_user"},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "endpoint_headers, expected_response, expected_status_code",
    params_test_get_tweets,
)
async def test_get_tweets(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    endpoint_headers: dict[str, any] | None,
    expected_status_code: int,
    expected_response: dict[str, any],
):
    """
    Тест проверки эндпоинта получения списка твиттов
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param endpoint_headers: заголовок запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """

    response = await ac.get("/tweets", headers=endpoint_headers)

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_delete_tweet_by_id = [
    (
        4,
        None,
        {"prev": [True, True, True], "next": [True, True, True]},
        {"result": True},
        200,
    ),
    (
        4,
        {"api-key": "danil"},
        {"prev": [True, True, True], "next": [False, False, False]},
        {"result": True},
        200,
    ),
    (
        7,
        None,
        {"prev": [False, False, False], "next": [False, False, False]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Твитта с id=7 не найден.",
        },
        404,
    ),
    (
        -3,
        None,
        {"prev": [False, False, False], "next": [False, False, False]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-3",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        None,
        {"prev": [False, False, False], "next": [False, False, False]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "id"],
                    "msg": "Input should be a valid integer, "
                    "unable to parse string as an integer",
                    "input": "test",
                }
            ],
        },
        422,
    ),
    (
        4,
        {"api-key": "unauthorized_user"},
        {"prev": [True, True, True], "next": [True, True, True]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "tweet_id, endpoint_headers, "
    "expected_check_exists, "
    "expected_response, expected_status_code",
    params_test_delete_tweet_by_id,
)
async def test_delete_tweet_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    tweet_id: any,
    endpoint_headers: dict[str, any] | None,
    expected_check_exists: dict[str, list[bool]],
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта удаления твитта по id
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param tweet_id: id удаляемого твитта в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_check_exists: словарь со списками ожидаемых
    параметров до и после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    if isinstance(tweet_id, int):
        assert (
            await check_row_table_db(async_db, Tweet, id=tweet_id)
            == expected_check_exists["prev"][0]
        )

        assert (
            await check_row_table_db(async_db, Media, tweet_id=tweet_id)
            == expected_check_exists["prev"][1]
        )

        assert (
            await check_row_table_db(async_db, Like, tweet_id=tweet_id)
            == expected_check_exists["prev"][2]
        )

    response = await ac.delete(f"/tweets/{tweet_id}", headers=endpoint_headers)

    if isinstance(tweet_id, int):
        assert (
            await check_row_table_db(async_db, Tweet, id=tweet_id)
            == expected_check_exists["next"][0]
        )

        assert (
            await check_row_table_db(async_db, Media, tweet_id=tweet_id)
            == expected_check_exists["next"][1]
        )

        assert (
            await check_row_table_db(async_db, Like, tweet_id=tweet_id)
            == expected_check_exists["next"][2]
        )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_like_tweet_by_id = [
    (
        1,
        None,
        {"prev": [2, False, 1], "next": [3, True, 1]},
        {"result": True},
        200,
    ),
    (
        7,
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Твитта с id=7 не найден.",
        },
        404,
    ),
    (
        4,
        {"api-key": "egor"},
        {"prev": [2, True, 3], "next": [2, True, 3]},
        {"result": True},
        200,
    ),
    (
        5,
        {"api-key": "egor"},
        {"prev": [2, False, 3], "next": [2, False, 3]},
        {"result": True},
        200,
    ),
    (
        -3,
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-3",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "id"],
                    "msg": "Input should be a valid integer, "
                    "unable to parse string as an integer",
                    "input": "test",
                }
            ],
        },
        422,
    ),
    (
        1,
        {"api-key": "unauthorized_user"},
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "tweet_id, endpoint_headers, "
    "expected_params_check, "
    "expected_response, expected_status_code",
    params_test_like_tweet_by_id,
)
async def test_like_tweet_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    tweet_id: int | str,
    endpoint_headers: dict[str, any] | None,
    expected_params_check: dict[str, list[any]],
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта добавления лайка твитту
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param tweet_id: id твитта в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_params_check: словарь со списками ожидаемых
    параметров до и после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    if isinstance(tweet_id, int):
        assert (
            await get_count_row_db(async_db, Like)
            == expected_params_check["prev"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Like,
                tweet_id=tweet_id,
                user_id=expected_params_check["prev"][2],
            )
            == expected_params_check["prev"][1]
        )

    response = await ac.post(
        f"/tweets/{tweet_id}/likes", headers=endpoint_headers
    )

    if isinstance(tweet_id, int):
        assert (
            await get_count_row_db(async_db, Like)
            == expected_params_check["next"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Like,
                tweet_id=tweet_id,
                user_id=expected_params_check["prev"][2],
            )
            == expected_params_check["next"][1]
        )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_unlike_tweet_by_id = [
    (
        4,
        {"api-key": "egor"},
        {"prev": [2, True, 3], "next": [1, False, 3]},
        {"result": True},
        200,
    ),
    (
        7,
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Твитта с id=7 не найден.",
        },
        404,
    ),
    (
        4,
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {"result": True},
        200,
    ),
    (
        -3,
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-3",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        None,
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "id"],
                    "msg": "Input should be a valid integer, "
                    "unable to parse string as an integer",
                    "input": "test",
                }
            ],
        },
        422,
    ),
    (
        4,
        {"api-key": "unauthorized_user"},
        {"prev": [2, False, 1], "next": [2, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "tweet_id, endpoint_headers, "
    "expected_params_check, "
    "expected_response, expected_status_code",
    params_test_unlike_tweet_by_id,
)
async def test_unlike_tweet_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    tweet_id: int | str,
    endpoint_headers: dict[str, any] | None,
    expected_params_check: dict[str, list[any]],
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта удаления лайка с твитта
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param tweet_id: id твитта в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_params_check: словарь со списками ожидаемых
    параметров до и после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    if isinstance(tweet_id, int):
        assert (
            await get_count_row_db(async_db, Like)
            == expected_params_check["prev"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Like,
                tweet_id=tweet_id,
                user_id=expected_params_check["prev"][2],
            )
            == expected_params_check["prev"][1]
        )

    response = await ac.delete(
        f"/tweets/{tweet_id}/likes", headers=endpoint_headers
    )

    if isinstance(tweet_id, int):
        assert (
            await get_count_row_db(async_db, Like)
            == expected_params_check["next"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Like,
                tweet_id=tweet_id,
                user_id=expected_params_check["next"][2],
            )
            == expected_params_check["next"][1]
        )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response
