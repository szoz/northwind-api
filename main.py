from fastapi import FastAPI, HTTPException, Path, status
from fastapi.responses import RedirectResponse
from sqlite3 import connect
from typing import Optional

from schemas import EmployeesOrderEnum

DATABASE_URL = 'northwind.db'

app = FastAPI()


@app.on_event('startup')
async def startup():
    """Initiate database connection on app startup. Global unicode decode ignoring is added specifically for used db."""
    app.db_connection = connect(DATABASE_URL)
    app.db_connection.text_factory = lambda b: b.decode(errors='ignore')


@app.on_event('shutdown')
async def shutdown():
    """Terminate database connection on app shutdown."""
    app.db_connection.close()


@app.get('/')
async def index():
    """Redirect from root endpoint to Open API documentation endpoint."""
    return RedirectResponse('/docs')


@app.get('/products')
async def get_products():
    """Return list of all Products and their count."""
    query = 'SELECT ProductName FROM Products'
    products = [row[0] for row in app.db_connection.execute(query).fetchall()]
    payload = {'products': products, 'products_counter': len(products)}

    return payload


@app.get('/products/{id}')
async def get_product(product_id: int = Path(-1, alias='id')):
    """Return product with given id."""
    query = 'SELECT ProductID, ProductName FROM Products WHERE ProductID=:id'
    product = app.db_connection.execute(query, {'id': product_id}).fetchone()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    payload = {'id': product[0], 'name': product[1]}

    return payload


@app.get('/categories')
async def get_categories():
    """Return list all Categories with ids."""
    query = 'SELECT CategoryID, CategoryName FROM Categories'
    records = app.db_connection.execute(query).fetchall()
    categories = [{'id': record[0], 'name': record[1]}
                  for record in records]
    payload = {'categories': categories}

    return payload


@app.get('/customers')
async def get_customers():
    """Return list all customers with details."""
    query = 'SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers'
    records = app.db_connection.execute(query).fetchall()
    customers = []
    for record in records:
        address = [item if item is not None else ''
                   for item in record[2:]]
        customer = {'id': record[0], 'name': record[1], 'full_address': ' '.join(address)}
        customers.append(customer)
    payload = {'customers': customers}

    return payload


def parse_employees_order(order: str):
    """Helper function for parsing and validating '/employees' order from query params"""
    if order is not None:
        try:
            parsed_order = EmployeesOrderEnum(order).name
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid order option, permitted: 'first_name', 'last_name', 'city'")
    else:
        parsed_order = 'EmployeeID'

    return parsed_order


@app.get('/employees')
async def get_employees(order: Optional[str] = None, limit: int = -1, offset: int = -1):
    """Return list all employees with given sorting order and pagination."""
    order_query = parse_employees_order(order)
    query = f"""SELECT EmployeeID, LastName, FirstName, City 
                FROM Employees ORDER BY {order_query} LIMIT {limit} OFFSET {offset}"""
    records = app.db_connection.execute(query).fetchall()
    employees = [{'id': record[0], 'last_name': record[1], 'first_name': record[2], 'city': record[3]}
                 for record in records]
    payload = {'employees': employees}

    return payload


@app.get('/products_extended')
async def products_extended():
    """Return list of products with detailed information."""
    query = """SELECT ProductID, ProductName, Categories.CategoryName, Suppliers.CompanyName FROM Products
               JOIN Categories ON Categories.CategoryID = Products.ProductID
               JOIN Suppliers on Products.SupplierID = Suppliers.SupplierID;"""
    records = app.db_connection.execute(query).fetchall()
    products = [{'id': record[0], 'name': record[1], 'category': record[2], 'supplier': record[3]}
                for record in records]
    payload = {'products_extended': products}

    return payload
