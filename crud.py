from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

import models
import schemas


def read_supplier(db: Session, supplier_id: int):
    """Return supplier with given id."""
    return db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()


def read_suppliers(db: Session):
    """Return list of all suppliers."""
    return db.query(models.Supplier).order_by(models.Supplier.supplier_id).all()


def create_supplier(db: Session, supplier: schemas.Supplier):
    """Create new supplier and return its details."""
    new_id = db.query(func.max(models.Supplier.supplier_id)).scalar() + 1
    supplier.supplier_id = new_id
    db.add(models.Supplier(**supplier.dict()))
    db.commit()

    return read_supplier(db, supplier_id=new_id)


def read_supplier_products(db: Session, supplier_id: int):
    """Return list of all products of supplier with given id"""
    return db.query(models.Product).filter(models.Product.supplier_id == supplier_id).\
        order_by(models.Product.product_id.desc()).all()
