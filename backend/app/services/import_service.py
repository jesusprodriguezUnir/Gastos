from app.services.importers.caixa import CaixaImporter
from app.services.importers.ing import INGImporter
from app.services.importers.sabadell import SabadellImporter
from app.services.importers.revolut import RevolutImporter
from app.db.schemas import TransactionCreate
from typing import List

class ImportService:
    def __init__(self):
        self.importers = {
            "CAIXA": CaixaImporter(),
            "ING": INGImporter(),
            "SABADELL": SabadellImporter(),
            "REVOLUT": RevolutImporter()
        }

    def process_file(self, bank_name: str, file_path: str, account_id: int) -> List[TransactionCreate]:
        importer = self.importers.get(bank_name.upper())
        if not importer:
            raise ValueError(f"No importer found for bank: {bank_name}")
        
        return importer.parse(file_path, account_id)
