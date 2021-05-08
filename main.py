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
    cursor = app.db_connection.cursor()
    products = [row[0] for row in cursor.execute("SELECT ProductName FROM Products").fetchall()]
    return {
        "products": products,
        "products_counter": len(products)
    }
