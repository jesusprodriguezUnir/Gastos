from fastapi.testclient import TestClient
from app.main import app
import io

def test_upload_file(client):
    # Create File
    file_content = b"Fecha,Concepto,Importe\n01/01/2026,Test,100"
    file = io.BytesIO(file_content)
    file.name = "test.csv"
    
    # We need an account to upload to
    # We can rely on seed or create one via API if possible, or fixture
    # But client fixture uses empty test db. We need to seed it.
    from app.db.models import Account
    # Access db session from client app? Hard with TestClient unless we use override.
    # The client fixture in conftest ALREADY overrides get_db with 'db' fixture.
    # So we can just use the 'db' fixture in parsing this test function if we passed it?
    # But test_upload_file(client) doesn't have db.
    pass

def test_upload_flow(client, db):
    # 1. Create Account
    from app.db.models import Account
    acc = Account(name="TestImport", bank_name="CAIXA", currency="EUR")
    db.add(acc)
    db.commit()
    db.refresh(acc)

    # 2. Upload File
    # Create valid Caixa excel? Or CSV if supported. Caixa Importer supports parsed DataFrame.
    # The pandas read_excel might fail if we send CSV bytes but claimed excel?
    # CaixaImporter calls read_file which calls pd.read_excel or pd.read_csv based on extension?
    # BaseImporter.read_file uses pd.read_excel for .xlsx and .xls, pd.read_csv for .csv
    
    csv_content = b"Fecha,Concepto,Importe\n01/01/2026,Test Transaction,120,50"
    files = {
        'file': ('test.csv', csv_content, 'text/csv')
    }
    data = {
        'bank_name': 'CAIXA',
        'account_id': str(acc.id)
    }
    
    response = client.post("/api/v1/upload/", files=files, data=data)
    
    # Debug if fails
    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] == 1
    assert json_data["message"] == "Import successful"
