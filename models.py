from sqlalchemy import Column, Integer, String

from database import Base
from utils import CaseMixin


class Supplier(Base, CaseMixin):
    __tablename__ = 'suppliers'

    supplier_id = Column(Integer, primary_key=True, nullable=False)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    contact_title = Column(String)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    postal_code = Column(String)
    country = Column(String)
    phone = Column(String)
    fax = Column(String)
    homepage = Column(String)
