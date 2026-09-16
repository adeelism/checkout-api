from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_example_from_brief():
    response = client.post("/checkout", json=["001", "002", "001", "004", "003"])
    assert response.status_code == 200
    assert response.json() == {"price": 380}


def test_single_item():
    response = client.post("/checkout", json=["003"])
    assert response.status_code == 200
    assert response.json() == {"price": 50}


def test_discount_applies_repeatedly():
    response = client.post("/checkout", json=["001"] * 6)
    assert response.json() == {"price": 400}


def test_empty_basket():
    response = client.post("/checkout", json=[])
    assert response.status_code == 200
    assert response.json() == {"price": 0}


def test_unknown_product_returns_400():
    response = client.post("/checkout", json=["001", "999"])
    assert response.status_code == 400


def test_non_array_body_returns_422():
    response = client.post("/checkout", json={"products": ["001"]})
    assert response.status_code == 422


def test_non_string_elements_return_422():
    response = client.post("/checkout", json=[1, 2, 3])
    assert response.status_code == 422
