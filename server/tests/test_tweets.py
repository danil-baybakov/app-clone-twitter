from httpx import AsyncClient


async def test_add_tweet(ac: AsyncClient):
    response = await ac.get("/tests")
    assert response.status_code == 200


async def test_create_tweet():
    assert 2 == 2
