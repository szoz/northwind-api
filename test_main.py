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
    test_records = [{"SupplierID": 1, "CompanyName": "Exotic Liquids"},
                    {"SupplierID": 2, "CompanyName": "New Orleans Cajun Delights"}]

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is list
    assert sorted(payload, key=lambda item: item['SupplierID']) == payload
    assert payload[:2] == test_records


def test_supplier(client):
    """Test '/suppliers' endpoint with given id."""
    test_path = '/suppliers/{}'
    test_id = 5
    test_record = {
        'SupplierID': 5,
        'CompanyName': 'Cooperativa de Quesos \'Las Cabras\'',
        'ContactName': 'Antonio del Valle Saavedra',
        'ContactTitle': 'Export Administrator',
        'Address': 'Calle del Rosal 4',
        'City': 'Oviedo',
        'Region': 'Asturias',
        'PostalCode': '33007',
        'Country': 'Spain',
        'Phone': '(98) 598 76 54',
        'Fax': None,
        'HomePage': None,
    }

    response = client.get(test_path.format(test_id))
    payload = response.json()
    response_invalid = client.get(test_path.format(999))

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert type(payload) is dict
    assert payload == test_record



