from fastapi.testclient import TestClient
import pytest

from main import app, startup


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_products(client):
    """Test '/products' endpoint."""
    test_path = '/products'

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload.get('products')) is list
    assert len(payload['products']) == payload['products_counter']


def test_categories(client):
    """Test '/categories' endpoint."""
    test_path = '/categories'
    test_category = {"id": 1, "name": "Beverages"}

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is dict
    assert type(payload.get('categories')) is list
    assert test_category in payload['categories']


def test_customers(client):
    """Test '/customers' endpoint."""
    test_path = '/customers'
    test_customer = {'id': 'ALFKI', 'name': 'Alfreds Futterkiste',
                     'full_address': 'Obere Str. 57 12209 Berlin Germany'}

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is dict
    assert type(payload.get('customers')) is list
    assert test_customer in payload['customers']
