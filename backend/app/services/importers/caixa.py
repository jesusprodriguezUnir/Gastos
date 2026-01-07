from typing import List
from app.db.schemas import TransactionCreate
from app.services.importers.base import BaseImporter
import pandas as pd
from datetime import datetime

class CaixaImporter(BaseImporter):
    def parse(self, file_path: str, account_id: int) -> List[TransactionCreate]:
        df = self.read_file(file_path)
        # Logic for CaixaBank format
        # Expected columns (example): 'Fecha', 'Concepto', 'Importe'
        transactions = []
        for _, row in df.iterrows():
            # Adjust column names based on real Caixa format
            date_str = row.get('Fecha', datetime.now().strftime('%Y-%m-%d'))
            amount = row.get('Importe', 0.0)
            description = row.get('Concepto', 'No description')
            
            # Basic cleanup
            try:
                date_obj = datetime.strptime(str(date_str).split(" ")[0], '%Y-%m-%d').date()
            except:
                date_obj = datetime.now().date()

            transaction = TransactionCreate(
                date=date_obj,
                amount=float(str(amount).replace(',', '.')), # Handle European formats
                description=description,
                account_id=account_id,
                raw_import_data=str(row.to_dict())
            )
            transactions.append(transaction)
        return transactions
