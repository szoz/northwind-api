from fastapi import HTTPException, status

from schemas import EmployeesOrderEnum


def parse_employees_sort(sort: str):
    """Helper function for validating and parsing '/employees' sort and pagination parameters."""
    if sort is not None:
        try:
            parsed_sort = EmployeesOrderEnum(sort).name
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid order option, permitted: 'first_name', 'last_name', 'city'")
    else:
        parsed_sort = 'EmployeeID'

    return parsed_sort


def calculate_total_price(quantity: int, discount: int, unit_price: int):
    """Helper function for calculating product total price for '/products/{id}/orders' endpoint"""
    total_price = unit_price * quantity * (1 - discount)
    return round(total_price, ndigits=2)
