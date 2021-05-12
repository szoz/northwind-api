from fastapi.testclient import TestClient
import pytest
from secrets import  token_hex

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
    """Test GET '/categories' endpoint."""
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


def test_products_extended(client):
    """Test '/products_extended' endpoint."""
    test_path = '/products_extended'
    product_short_path = '/products'
    test_product = {"id": 1, "name": "Chai", "category": "Beverages", "supplier": "Exotic Liquids"}

    response = client.get(test_path)
    payload = response.json()
    expected_length = client.get(product_short_path).json()['products_counter']

    assert response.status_code == 200
    assert type(payload) is dict
    assert type(payload.get('products_extended')) is list
    assert test_product in payload['products_extended']
    assert sorted(payload['products_extended'], key=lambda item: item['id']) == payload['products_extended']
    assert len(payload['products_extended']) == expected_length


def test_products_orders(client):
    """Test '/products/{id}/orders endpoint."""
    test_path = '/products/{}/orders'
    test_order = {"id": 10273, "customer": "QUICK-Stop", "quantity": 24, "total_price": 565.44}

    response_invalid = client.get(test_path.format(999))
    response_valid = client.get(test_path.format(10))
    payload = response_valid.json()

    assert response_invalid.status_code == 404
    assert response_valid.status_code == 200
    assert type(payload) is dict
    assert type(payload.get('orders')) is list
    assert test_order in payload['orders']


def test_create_category(client):
    """Test POST '/categories' endpoint."""
    test_path = '/categories'
    test_category = {'name': token_hex(8)}

    response = client.post(test_path, json=test_category)
    response_all = client.get(test_path)

    assert response.status_code == 201
    assert response.json() == response_all.json()['categories'][-1]
    assert response.json().get('name') == test_category['name']


def test_update_category(client):
    """Test PUT '/categories' endpoint."""
    test_path = '/categories/{}'
    all_categories_path = '/categories'
    test_category = {'name': token_hex(8)}

    last_id = client.get(all_categories_path).json()['categories'][-1]['id']
    response = client.put(test_path.format(last_id), json=test_category)
    response_all = client.get(all_categories_path)
    response_invalid = client.put(test_path.format(999), json=test_category)

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert response.json() == response_all.json()['categories'][-1]
    assert response.json().get('name') == test_category['name']


def test_remove_category(client):
    """Test DELETE '/categories' endpoint."""
    test_path = '/categories/{}'
    all_categories_path = '/categories'

    initial_categories = client.get(all_categories_path).json()['categories']
    last_id = initial_categories[-1]['id']
    response = client.delete(test_path.format(last_id))
    response_all = client.get(all_categories_path)
    response_invalid = client.delete(test_path.format(999))

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert initial_categories[-1] not in response_all.json()['categories']
    assert response.json() == {'deleted': 1}
