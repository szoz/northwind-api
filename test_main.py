from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_products_old(client):
    """Test '/products' endpoint with no path parameters."""
    test_path = '/products'

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload.get('products')) is list
    assert len(payload['products']) == payload['products_counter']


def test_products(client):
    """Test '/products' endpoint with given id."""
    test_path = '/products/'
    test_product = {'id': 1, 'name': 'Chai'}

    response_invalid = client.get(f'{test_path}999')
    response_valid = client.get(f'{test_path}1')

    assert response_invalid.status_code == 404
    assert response_valid.status_code == 200
    assert response_valid.json() == test_product


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


def test_employees(client):
    """Test '/employees' endpoint."""
    test_path = '/employees'
    test_employee = {'id': 1, 'last_name': 'Davolio', 'first_name': 'Nancy', 'city': 'Seattle'}
    orders = ['first_name', 'last_name', 'city']

    response_invalid = client.get(test_path, params={'order': 'invalid'})
    response_default_order = client.get(test_path)
    responses_ordered = [client.get(test_path, params={'order': case}) for case in orders]

    assert response_invalid.status_code == 400
    assert response_default_order.status_code == 200
    payload = response_default_order.json()
    assert type(payload) is dict
    assert type(payload.get('employees')) is list
    assert test_employee in payload['employees']
    assert sorted(payload['employees'], key=lambda item: item['id']) == payload['employees']
    for response, order in zip(responses_ordered, orders):
        payload = response.json()
        assert sorted(payload['employees'], key=lambda item: item[order]) == payload['employees']
