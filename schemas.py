from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class AllProducts(BaseModel):
    """All products summary model."""
    products: List[str]
    products_counter: int


class Product(BaseModel):
    """Product model with basic info."""
    id: int
    name: str


class Category(BaseModel):
    """Product category model."""
    name: str
    id: Optional[int]


class Categories(BaseModel):
    """Product categories list model."""
    categories: List[Category]


class Customer(BaseModel):
    """Customer model."""
    id: str
    name: str
    full_address: str


class Customers(BaseModel):
    """Customers list model."""
    customers: List[Customer]


class Employee(BaseModel):
    """Employee model."""
    id: int
    last_name: str
    first_name: str
    city: str


class Employees(BaseModel):
    """Employees list model."""
    employees: List[Employee]


class EmployeesOrderEnum(str, Enum):
    """Enumerator for employees ordering."""
    FirstName = 'first_name'
    LastName = 'last_name'
    City = 'city'


class ProductExtended(BaseModel):
    """Product model with extended info."""
    id: int
    name: str
    category: str
    supplier: str


class ProductsExtended(BaseModel):
    """Products with extended info list model."""
    products_extended: List[ProductExtended]


class Order(BaseModel):
    """Order model."""
    id: int
    customer: str
    quantity: int
    total_price: float


class Orders(BaseModel):
    """Orders list model."""
    orders: List[Order]


class Deleted(BaseModel):
    """Deleting summaryi info model."""
    deleted: int
