from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlite3 import connect

DATABASE_URL = "northwind.db"

app = FastAPI()


@app.on_event('startup')
async def startup():
    """Initiate database connection on app startup. Global unicode decode ignoring is added specifically for used db."""
    app.db_connection = connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")


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
    products = [row[0] for row in app.db_connection.execute("SELECT ProductName FROM Products").fetchall()]
    payload = {"products": products, "products_counter": len(products)}

    return payload


@app.get('/categories')
async def get_categories():
    """Return list all Categories with ids."""
    query = "SELECT CategoryID, CategoryName FROM Categories"
    records = app.db_connection.execute(query).fetchall()
    categories = [{'id': record[0], 'name': record[1]}
                  for record in records]
    payload = {'categories': categories}

    return payload


@app.get('/customers')
async def get_customers():
    """Return list all customers with details."""
    query = "SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers"
    records = app.db_connection.execute(query).fetchall()
    customers = []
    for record in records:
        address = [item if item is not None else ''
                   for item in record[2:]]
        customer = {'id': record[0], 'name': record[1], 'full_address': ' '.join(address)}
        customers.append(customer)
    payload = {'customers': customers}

    return payload
