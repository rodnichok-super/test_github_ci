import asyncio

import pytest
from fastapi.testclient import TestClient

from fastapi_prod.database import Base, engine
from fastapi_prod.main import app


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    """
    Создаёт таблицы перед тестами и очищает их после тестов.
    Работает для всех тестов автоматически.
    """
    async def setup():
        async with engine.begin() as conn:
            # Drop tables на случай старых тестов
            await conn.run_sync(Base.metadata.drop_all)
            # Создаём заново
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(setup())
    yield


@pytest.fixture
def client():
    return TestClient(app)


def test_list_recipes(client):
    """
    Проверяем GET /recipes
    """
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_recipe(client):
    """
    Проверяем POST /recipes
    """
    payload = {
        "title": "Борщ",
        "cooking_time": 90,
        "ingredients": "свекла, картофель, капуста",
        "description": "1. Нарезать овощи\n2. Варить 40 минут"
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["count_views"] == 0
    assert "id" in data


def test_get_recipe(client):
    """
    Проверяем GET /recipes/{id} и увеличение count_views
    """
    payload = {
        "title": "Салат",
        "cooking_time": 10,
        "ingredients": "капуста, морковь",
        "description": "Нарезать и смешать"
    }
    post_resp = client.post("/recipes", json=payload)
    recipe_id = post_resp.json()["id"]

    get_resp = client.get(f"/recipes/{recipe_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == recipe_id
    assert data["count_views"] == 1
