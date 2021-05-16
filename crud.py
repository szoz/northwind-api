from sqlalchemy.orm import Session

import models


def read_supplier(db: Session, supplier_id: int):
    """Return supplier with given id."""
    return db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()


def read_suppliers(db: Session):
    """Return list of all suppliers."""
    return db.query(models.Supplier).order_by(models.Supplier.supplier_id).all()


def read_supplier_products(db: Session, supplier_id: int):
    """Return list of all products of supplier with given id"""
    return db.query(models.Product).filter(models.Product.supplier_id == supplier_id).\
        order_by(models.Product.product_id.desc()).all()
