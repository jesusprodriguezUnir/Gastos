from typing import List
from app.db.schemas import TransactionCreate
from app.services.importers.base import BaseImporter
from datetime import datetime

class SabadellImporter(BaseImporter):
    def parse(self, file_path: str, account_id: int) -> List[TransactionCreate]:
        df = self.read_file(file_path)
        transactions = []
        for _, row in df.iterrows():
            transaction = TransactionCreate(
                date=datetime.now().date(),
                amount=0.0,
                description="Imported from Sabadell",
                account_id=account_id,
                raw_import_data=str(row.to_dict())
            )
            transactions.append(transaction)
        return transactions
