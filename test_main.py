from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_suppliers(client):
    """Test '/suppliers' endpoint."""
    test_path = '/suppliers'

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is list
    assert 'supplier_id' in payload[0].keys()
    assert sorted(payload, key=lambda item: item['supplier_id']) == payload


def test_supplier(client):
    """Test '/suppliers' endpoint with given id."""
    test_path = '/suppliers/{}'
    test_id = 1

    response = client.get(test_path.format(test_id))
    payload = response.json()
    response_invalid = client.get(test_path.format(999))

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert type(payload) is dict
    assert payload['supplier_id'] == test_id
