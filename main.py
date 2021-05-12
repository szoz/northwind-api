from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.responses import RedirectResponse
from sqlite3 import connect
from typing import Optional

from schemas import AllProducts, Product, Categories, Category, Customers, Employees, ProductsExtended, Orders, Deleted

from utils import parse_employees_sort, calculate_total_price

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


@app.get('/', tags=['root'])
async def index():
    """Redirect from root endpoint to Open API documentation endpoint."""
    return RedirectResponse('/docs')


@app.get('/products', response_model=AllProducts, tags=['products'])
async def get_products():
    """Return list of all Products and their count."""
    query = 'SELECT ProductName FROM Products'
    products = [row[0] for row in app.db_connection.execute(query).fetchall()]

    return {'products': products, 'products_counter': len(products)}


@app.get('/products/{id}', response_model=Product, tags=['products'])
async def get_product(product_id: int = Path(-1, alias='id')):
    """Return product with given id."""
    query = 'SELECT ProductID, ProductName FROM Products WHERE ProductID = :id'
    product = app.db_connection.execute(query, {'id': product_id}).fetchone()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    return {'id': product[0], 'name': product[1]}


@app.get('/categories', response_model=Categories, tags=['categories'])
async def get_categories():
    """Return list all Categories with ids."""
    query = 'SELECT CategoryID, CategoryName FROM Categories'
    records = app.db_connection.execute(query).fetchall()
    categories = [{'id': record[0], 'name': record[1]}
                  for record in records]

    return {'categories': categories}


@app.get('/customers', response_model=Customers, tags=['customers'])
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

    return {'customers': customers}


@app.get('/employees', response_model=Employees, tags=['employees'])
async def get_employees(sort: Optional[str] = Query(None, alias='order'), limit: int = -1, offset: int = -1):
    """Return list all employees with given sorting and pagination."""
    sort_sub_query = parse_employees_sort(sort)
    query = f"""SELECT EmployeeID, LastName, FirstName, City 
                FROM Employees ORDER BY {sort_sub_query} LIMIT {limit} OFFSET {offset}"""
    records = app.db_connection.execute(query).fetchall()
    employees = [{'id': record[0], 'last_name': record[1], 'first_name': record[2], 'city': record[3]}
                 for record in records]

    return {'employees': employees}


@app.get('/products_extended', response_model=ProductsExtended, tags=['products'])
async def get_products_extended():
    """Return list of products with detailed information."""
    query = """SELECT ProductID, ProductName, Categories.CategoryName, Suppliers.CompanyName FROM Products
               LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
               LEFT JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID"""
    records = app.db_connection.execute(query).fetchall()
    products = [{'id': record[0], 'name': record[1], 'category': record[2], 'supplier': record[3]}
                for record in records]

    return {'products_extended': products}


@app.get('/products/{id}/orders', response_model=Orders, tags=['products'])
async def get_products_orders(product_id: int = Path(-1, alias='id')):
    """Return list of all orders with product of given id."""
    query = """SELECT Orders.OrderID, Customers.CompanyName, "Order Details".Quantity, "Order Details".Discount, 
                   "Order Details".UnitPrice FROM Orders
               LEFT JOIN "Order Details" ON Orders.OrderID = "Order Details".OrderID
               LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID
               WHERE ProductID = :id"""
    records = app.db_connection.execute(query, {'id': product_id}).fetchall()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    orders = [{'id': record[0], 'customer': record[1], 'quantity': record[2],
               'total_price': calculate_total_price(*record[2:])}
              for record in records]

    return {'orders': orders}


@app.post('/categories', response_model=Category, tags=['categories'], status_code=status.HTTP_201_CREATED)
async def create_category(category: Category):
    """Create new product category"""
    query = 'INSERT INTO Categories (CategoryName) VALUES (:name)'
    query_read = 'SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = :id'
    cursor = app.db_connection.cursor()
    cursor.execute(query, {'name': category.name})
    app.db_connection.commit()

    record = cursor.execute(query_read, {'id': cursor.lastrowid}).fetchone()

    return Category(id=record[0], name=record[1])


@app.put('/categories/{id}', response_model=Category, tags=['categories'])
async def update_category(category: Category, category_id: int = Path(-1, alias='id')):
    """Update category with given id."""
    query = 'UPDATE Categories SET CategoryName = :name WHERE CategoryID = :id'
    query_read = 'SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = :id'
    cursor = app.db_connection.cursor()
    if not cursor.execute(query_read, {'id': category_id}).fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    cursor.execute(query, {'name': category.name, 'id': category_id})
    app.db_connection.commit()

    record = cursor.execute(query_read, {'id': category_id}).fetchone()

    return Category(id=record[0], name=record[1])


@app.delete('/categories/{id}', response_model=Deleted, tags=['categories'])
async def remove_category(category_id: int = Path(-1, alias='id')):
    """Remove category with given id."""
    query = 'DELETE FROM Categories WHERE CategoryID = :id'
    query_read = 'SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = :id'
    cursor = app.db_connection.cursor()
    if not cursor.execute(query_read, {'id': category_id}).fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    return {'deleted': cursor.execute(query, {'id': category_id}).rowcount}
