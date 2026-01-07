from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services.import_service import ImportService
from app.services.categorizer import apply_categorization
from app.services import transaction_service
import shutil
import os
import tempfile

router = APIRouter()

@router.post("/")
def upload_file(
    file: UploadFile = File(...),
    bank_name: str = Form(...),
    account_id: int = Form(...),
    db: Session = Depends(deps.get_db)
):
    # Save temp file
    # In a real app, handle file types carefully
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # 1. Parse
        importer_service = ImportService()
        transactions = importer_service.process_file(bank_name, tmp_path, account_id)
        
        # 2. Categorize
        transactions = apply_categorization(db, transactions)

        # 3. Save
        saved_transactions = transaction_service.create_transactions_bulk(db, transactions)
        
        return {"message": "Import successful", "count": len(saved_transactions)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
