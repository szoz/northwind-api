from enum import Enum
from pydantic import BaseModel
from typing import Optional


class EmployeesOrderEnum(str, Enum):
    """Enumerator for employees ordering."""
    FirstName = 'first_name'
    LastName = 'last_name'
    City = 'city'


class Category(BaseModel):
    """Product category representation"""
    name: str
    id: Optional[int]
