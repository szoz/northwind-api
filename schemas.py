from pydantic import BaseModel
from typing import Optional
from utils import CaseMixin


class SupplierBrief(BaseModel):
    """Supplier schema with less information for all suppliers view."""
    supplier_id: int
    company_name: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = CaseMixin.to_pascal


class Supplier(SupplierBrief):
    """Supplier schema for detailed view."""
    contact_name: Optional[str]
    contact_title: Optional[str]
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    fax: Optional[str]
    homepage: Optional[str]
