# FinanceFlow - Personal Expense Manager

## Architecture Overview
- **Backend**: FastAPI with SQLAlchemy ORM, SQLite database. Core models: `Account`, `Category`, `Transaction`, `Invoice`, `ImportRule`.
- **Frontend**: React 18 with Vite, Chart.js for visualizations, Axios for API calls.
- **Data Flow**: Bank CSV/Excel imports → Pandas parsing → Auto-categorization (regex rules) → Transaction storage → Dashboard aggregation.

## Key Patterns
- **Importers**: Bank-specific classes (e.g., `CaixaImporter`) inherit from `BaseImporter`, use Pandas to parse files into `TransactionCreate` schemas. Detect headers dynamically.
- **Categorization**: `Categorizer.predict_category()` applies regex patterns from `ImportRule` models to transaction descriptions.
- **Transactions**: Always linked to an `Account`; optionally to `Category` and `Invoice`.
- **Invoices**: Store uploaded files in `backend/uploads/invoices/`, reference via `file_path` in `Invoice` model.
- **API Authentication**: External access to upload and invoice endpoints requires `X-API-Key` header with valid `ApiKey` from database.

## Development Workflows
- **Init DB**: `cd backend && python -m app.db.init_db` (creates tables).
- **Seed Data**: Run `python -m app.db.seed` for default accounts/categories (not in README but exists in `seed.py`).
- **Run Backend**: `uvicorn app.main:app --reload` (API at `http://localhost:8000`, docs at `/docs`).
- **Run Frontend**: `cd frontend && npm run dev` (app at `http://localhost:5173`).
- **Tests**: `cd backend && pytest` (uses in-memory SQLite, fixtures in `conftest.py`).

## Conventions
- **File Uploads**: Use `tempfile.NamedTemporaryFile` for processing, clean up after. Store permanent files in `uploads/` subdirs.
- **Error Handling**: Log full tracebacks to files like `import_error.log` for debugging imports.
- **API Responses**: Return dicts with `"message"` and relevant data (e.g., `{"message": "Import successful", "count": len(saved)}`).
- **Frontend Routing**: Use React Router with nested routes under `Layout` component.

## Examples
- **Adding New Importer**: Create class in `services/importers/` inheriting `BaseImporter`, implement `parse()` to return `List[TransactionCreate]`.
- **New Category Rule**: Insert `ImportRule(pattern=r"regex", category_id=1)` via DB or API.
- **Transaction Creation**: Use `transaction_service.create_transactions_bulk(db, transactions)` for bulk inserts.
- **API Key Authentication**: Protect endpoints with `api_key = Depends(deps.get_api_key)` to require `X-API-Key` header.</content>
<parameter name="filePath">d:\Programas\Temp\Gastos\.github\copilot-instructions.md