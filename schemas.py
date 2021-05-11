from enum import Enum


class EmployeesOrderEnum(str, Enum):
    """Enumerator for employees ordering."""
    FirstName = 'first_name'
    LastName = 'last_name'
    City = 'city'
