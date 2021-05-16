from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import schemas
import crud

app = FastAPI()


def get_db():
    """Dependency function returning new session for each request and closing session after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def get_root():
    """Redirect to Open API documentation."""
    return RedirectResponse('/docs')


@app.get('/suppliers', response_model=List[schemas.SupplierBrief], tags=['supplier'])
def get_suppliers(db: Session = Depends(get_db)):
    """Return list of all suppliers"""
    records = crud.read_suppliers(db)
    return [record.export() for record in records]


@app.post('/suppliers', status_code=status.HTTP_201_CREATED, tags=['supplier'])
def add_supplier(supplier: schemas.Supplier, db: Session = Depends(get_db)):
    """Add new supplier from request body and return it back."""
    record = crud.create_supplier(db, supplier)

    return record.export()


@app.get('/suppliers/{id}', response_model=schemas.Supplier, tags=['supplier'])
def get_supplier(supplier_id: int = Path(..., alias='id'), db: Session = Depends(get_db)):
    """Return supplier with given id."""
    record = crud.read_supplier(db, supplier_id=supplier_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

    return record.export()


@app.get('/suppliers/{id}/products', response_model=List[schemas.Product], tags=['supplier'])
def get_supplier_products(supplier_id: int = Path(..., alias='id'), db: Session = Depends(get_db)):
    """Return products with given supplier id."""
    records = crud.read_supplier_products(db, supplier_id=supplier_id)
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

    return [record.export() for record in records]
