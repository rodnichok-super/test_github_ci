from fastapi.testclient import TestClient

from fastapi_prod.main import app

client = TestClient(app)


def test_list_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
