from fastapi.testclient import TestClient
import pytest

from main import app, startup


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_products(client):
    """Test '/products' endpoint with products list."""
    test_path = '/products'

    response = client.get(test_path)

    assert response.status_code == 200
    assert type(response.json().get('products')) is list
    assert len(response.json()['products']) == response.json()['products_counter']
