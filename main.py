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


@app.get('/suppliers', response_model=List[schemas.Supplier], tags=['supplier'])
def get_suppliers(db: Session = Depends(get_db)):
    """Return list of all suppliers"""
    records = crud.read_suppliers(db)
    return [record.export() for record in records]


@app.get('/suppliers/{id}', response_model=schemas.Supplier, tags=['supplier'])
# @app.get('/suppliers/{id}', tags=['supplier'])
def get_supplier(supplier_id: int = Path(..., alias='id'), db: Session = Depends(get_db)):
    """Return supplier with given id."""
    db_user = crud.read_supplier(db, supplier_id=supplier_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')
    return db_user.export()
