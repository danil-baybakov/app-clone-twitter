import pytest
from httpx import AsyncClient
from models.followers import Follower
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import check_row_table_db, get_count_row_db

user_data = {
    "result": True,
    "user": {
        "id": 3,
        "name": "Egor Egorov",
        "followers": [
            {"id": 2, "name": "Danil Baybakov"},
            {"id": 4, "name": "Sergey Sergeev"},
        ],
        "following": [{"id": 2, "name": "Danil Baybakov"}],
    },
}

params_test_get_info_about_profile = [
    (3, {"api-key": ""}, user_data, 200),
    (
        5,
        {"api-key": ""},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Пользователь с id=5 не найден.",
        },
        404,
    ),
    (
        -1,
        {"api-key": ""},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-1",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        {"api-key": ""},
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
    ("me", {"api-key": "egor"}, user_data, 200),
    (
        "me",
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
    "user_id, endpoint_headers, expected_response, expected_status_code",
    params_test_get_info_about_profile,
)
async def test_get_info_about_profile(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    user_id: int | str,
    endpoint_headers: dict[str, any] | None,
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта получения
    информации о пользователе
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param user_id: id пользователя в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    response = await ac.get(f"/users/{user_id}", headers=endpoint_headers)

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_follow_user_by_id = [
    (
        2,
        None,
        {"prev": [3, False, 1], "next": [4, True, 1]},
        {"result": True},
        200,
    ),
    (
        5,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Пользователя с id=5 не найден.",
        },
        404,
    ),
    (
        3,
        {"api-key": "sergey"},
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {"result": True},
        200,
    ),
    (
        1,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {"result": True},
        200,
    ),
    (
        -1,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-1",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
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
        2,
        {"api-key": "unauthorized_user"},
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "user_id, endpoint_headers, expected_params_check, "
    "expected_response, expected_status_code",
    params_test_follow_user_by_id,
)
async def test_follow_user_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    user_id: int | str,
    endpoint_headers: dict[str, any] | None,
    expected_params_check: dict[str, list[any]],
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта добавления пользователя в читаемые
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param user_id: id пользователя добавляемого в читаемые
    в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_params_check: словарь со списками ожидаемых
    параметров до и после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    if isinstance(user_id, int):
        assert (
            await get_count_row_db(async_db, Follower)
            == expected_params_check["prev"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Follower,
                user_id_following=user_id,
                user_id_follower=expected_params_check["prev"][2],
            )
            == expected_params_check["prev"][1]
        )

    response = await ac.post(
        f"/users/{user_id}/follow", headers=endpoint_headers
    )

    if isinstance(user_id, int):
        assert (
            await get_count_row_db(async_db, Follower)
            == expected_params_check["next"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Follower,
                user_id_following=user_id,
                user_id_follower=expected_params_check["next"][2],
            )
            == expected_params_check["next"][1]
        )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response


params_test_unfollow_user_by_id = [
    (
        3,
        {"api-key": "danil"},
        {"prev": [3, True, 2], "next": [2, False, 2]},
        {"result": True},
        200,
    ),
    (
        5,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Пользователя с id=5 не найден.",
        },
        404,
    ),
    (
        3,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {"result": True},
        200,
    ),
    (
        1,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {"result": True},
        200,
    ),
    (
        -1,
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "-1",
                    "ctx": {"gt": 0},
                }
            ],
        },
        422,
    ),
    (
        "test",
        None,
        {"prev": [3, False, 1], "next": [3, False, 1]},
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
        2,
        {"api-key": "unauthorized_user"},
        {"prev": [3, False, 1], "next": [3, False, 1]},
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
        401,
    ),
]


@pytest.mark.parametrize(
    "user_id, endpoint_headers, expected_params_check, "
    "expected_response, expected_status_code",
    params_test_unfollow_user_by_id,
)
async def test_unfollow_user_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    user_id: int | str,
    endpoint_headers: dict[str, any] | None,
    expected_params_check: dict[str, list[any]],
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта удаления пользователя из читаемых
    :param id: id пользователя удаляемого из читаемых
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param user_id: id пользователя добавляемого в читаемые
    в пути запроса
    :param endpoint_headers: заголовок запроса
    :param expected_params_check: словарь со списками ожидаемых
    параметров до и после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    if isinstance(user_id, int):
        assert (
            await get_count_row_db(async_db, Follower)
            == expected_params_check["prev"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Follower,
                user_id_following=user_id,
                user_id_follower=expected_params_check["prev"][2],
            )
            == expected_params_check["prev"][1]
        )

    response = await ac.delete(
        f"/users/{user_id}/follow", headers=endpoint_headers
    )

    if isinstance(user_id, int):
        assert (
            await get_count_row_db(async_db, Follower)
            == expected_params_check["next"][0]
        )

        assert (
            await check_row_table_db(
                async_db,
                Follower,
                user_id_following=user_id,
                user_id_follower=expected_params_check["next"][2],
            )
            == expected_params_check["next"][1]
        )

    assert response.status_code == expected_status_code

    assert response.json() == expected_response
