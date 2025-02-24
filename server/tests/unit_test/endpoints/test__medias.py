import pytest
from httpx import AsyncClient
from models.medias import Media
from sqlalchemy.ext.asyncio import AsyncSession
from utils.fake_data import mock_image, rand_image, static_image

from tests.conftest import get_count_row_db

load_files_from_tweet_params = [
    (
        {"api-key": "unauthorized_user"},
        True,
        3,
        3,
        401,
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Не авторизированный пользователь.",
        },
    ),
    (
        None,
        False,
        3,
        3,
        422,
        {
            "result": False,
            "error_type": "RequestValidationError",
            "error_message": [
                {
                    "type": "missing",
                    "loc": ["body", "file"],
                    "msg": "Field required",
                    "input": None,
                }
            ],
        },
    ),
    (None, True, 3, 4, 200, {"result": True, "media_id": 4}),
]


@pytest.mark.parametrize(
    "endpoint_headers, endpoint_request_validate, "
    "expected_prev_count_medias_db, expected_next_count_medias_db, "
    "expected_status_code, expected_response",
    load_files_from_tweet_params,
)
async def test_load_files_from_tweet(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    endpoint_headers: dict[str, any] | None,
    endpoint_request_validate: bool,
    expected_prev_count_medias_db: int,
    expected_next_count_medias_db: int,
    expected_status_code: int,
    expected_response: dict[str, any],
):
    """
    Тест проверки эндпоинта загрузки файлов из твитта
    таблице медиафайлов твиттов БД
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param endpoint_headers: заголовок запроса
    :param endpoint_request_validate: флаг отправки валидного тела
    запроса
    :param expected_prev_count_medias_db: ожидаемое кол-во записей в
    таблице медиафайлов твиттов БД до запроса
    :param expected_next_count_medias_db: ожидаемое кол-во записей в
    таблице медиафайлов твиттов БД после запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    assert (
        await get_count_row_db(async_db, Media)
        == expected_prev_count_medias_db
    )

    if endpoint_request_validate:
        files = {"file": mock_image(rand_image)}
    else:
        files = {"invalidate": mock_image(rand_image)}

    response = await ac.post("/medias", files=files, headers=endpoint_headers)
    assert response.status_code == expected_status_code

    assert (
        await get_count_row_db(async_db, Media)
        == expected_next_count_medias_db
    )

    assert response.json() == expected_response


params_get_files_from_tweet_by_id = [
    (
        3,
        "bytes",
        None,
        mock_image(static_image),
        200,
    ),
    (
        5,
        "json",
        None,
        {
            "result": False,
            "error_type": "ClientHTTPException",
            "error_message": "Медиафайл с id=5 не найден.",
        },
        404,
    ),
    (
        -1,
        "json",
        None,
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
        "json",
        None,
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
]


@pytest.mark.parametrize(
    "media_id, type_response, endpoint_headers, "
    "expected_response, expected_status_code",
    params_get_files_from_tweet_by_id,
)
async def test_get_files_from_tweet_by_id(
    ac: AsyncClient,
    async_db: AsyncSession,
    prepare_gen_full_tables_db: None,
    media_id: int | str,
    type_response: str,
    endpoint_headers: dict[str, any] | None,
    expected_response: dict[str, any],
    expected_status_code: int,
):
    """
    Тест проверки эндпоинта получения медиафайла по id
    :param ac: фикстура асинхронного тестового клиента приложения
    :param async_db: фикстура cессии БД
    :param prepare_gen_full_tables_db: фикстура добавляет в БД фейковые
    записи для всех таблиц
    :param media_id: id медиафайла в пути запроса
    :param type_response: тип ответа
    :param endpoint_headers: заголовок запроса
    :param expected_status_code: ожидаемый статус выполнения запроса
    :param expected_response: ожидаемый ответ запроса
    :return:
    """
    response = await ac.get(f"/medias/{media_id}", headers=endpoint_headers)

    assert response.status_code == expected_status_code

    if type_response == "json":
        assert response.json() == expected_response

    if type_response == "bytes":
        assert response.content == expected_response
