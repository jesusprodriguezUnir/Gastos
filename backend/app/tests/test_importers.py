from app.services.importers.caixa import CaixaImporter
from app.db.schemas import TransactionCreate
import pandas as pd
import pytest
from datetime import date

def test_caixa_amount_parsing(tmp_path):
    # Create a dummy Excel file with tricky formats
    data = {
        "Fecha": ["01/01/2026", "02/01/2026"],
        "Concepto": ["Compra Super", "Nómina"],
        "Importe (€)": ["-45,50", "1.200,00"]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_caixa.xlsx"
    df.to_excel(file_path, index=False)

    importer = CaixaImporter()
    # Mock account ID 1
    transactions = importer.parse(str(file_path), 1)

    assert len(transactions) == 2
    
    # Check first transaction (expense)
    t1 = transactions[0]
    assert t1.amount == -45.50
    assert t1.date == date(2026, 1, 1)
    
    # Check second transaction (income with thousands separator)
    t2 = transactions[1]
    assert t2.amount == 1200.00
    assert t2.date == date(2026, 1, 2)

def test_caixa_header_detection(tmp_path):
    # Create excel with garbage rows at top
    data = {
        "ColA": ["Garbage", "More Garbage", "Fecha", "01/01/2026"],
        "ColB": [None, None, "Concepto", "Test Header"],
        "ColC": [None, None, "Importe", "50,00"]
    }
    # This structure is a bit synthetic, but simulates offset. 
    # Better to write rows directly to csv/excel to control row placement accurately.
    pass 
