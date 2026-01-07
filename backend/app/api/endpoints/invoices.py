from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.db import models, schemas
import shutil
import os
import uuid
from datetime import datetime

router = APIRouter()

# --- INVOICE CATEGORIES ---

@router.get("/categories/", response_model=List[schemas.InvoiceCategory])
def read_invoice_categories(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    categories = db.query(models.InvoiceCategory).offset(skip).limit(limit).all()
    return categories

@router.post("/categories/", response_model=schemas.InvoiceCategory)
def create_invoice_category(category: schemas.InvoiceCategoryCreate, db: Session = Depends(deps.get_db)):
    db_category = models.InvoiceCategory(name=category.name, icon=category.icon)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- INVOICES ---

@router.get("/", response_model=List[schemas.Invoice])
def read_invoices(
    skip: int = 0, 
    limit: int = 100, 
    vendor: Optional[str] = None,
    invoice_category_id: Optional[int] = None,
    db: Session = Depends(deps.get_db)
):
    query = db.query(models.Invoice)
    if vendor:
        query = query.filter(models.Invoice.vendor.ilike(f"%{vendor}%"))
    if invoice_category_id:
        query = query.filter(models.Invoice.invoice_category_id == invoice_category_id)
    
    invoices = query.offset(skip).limit(limit).all()
    return invoices

@router.post("/upload", response_model=schemas.Invoice)
def upload_invoice(
    vendor: str = Form(...),
    date: str = Form(...), # YYYY-MM-DD
    amount: float = Form(...),
    invoice_category_id: int = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    api_key = Depends(deps.get_api_key)
):
    # Validations
    category = db.query(models.InvoiceCategory).filter(models.InvoiceCategory.id == invoice_category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Invoice category not found")

    # Save file
    upload_dir = "uploads/invoices"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Create Invoice Record
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    db_invoice = models.Invoice(
        vendor=vendor,
        date=date_obj,
        amount=amount,
        description=description,
        invoice_category_id=invoice_category_id,
        file_path=file_path
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.delete("/{invoice_id}", response_model=schemas.Invoice)
def delete_invoice(invoice_id: int, db: Session = Depends(deps.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Delete file
    if os.path.exists(invoice.file_path):
        os.remove(invoice.file_path)
    
    db.delete(invoice)
    db.commit()
    return invoice
