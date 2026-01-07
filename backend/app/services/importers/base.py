from abc import ABC, abstractmethod
from typing import List
from app.db.schemas import TransactionCreate
import pandas as pd

class BaseImporter(ABC):
    @abstractmethod
    def parse(self, file_path: str, account_id: int) -> List[TransactionCreate]:
        pass

    def read_file(self, file_path: str) -> pd.DataFrame:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
