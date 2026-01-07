# Resumen del Flujo de Ejecución - FinanceFlow

## Descripción General
FinanceFlow es una aplicación web para el control y análisis de finanzas personales. Permite importar movimientos bancarios, categorizarlos automáticamente y visualizar datos mediante gráficos interactivos.

## Arquitectura
- **Backend**: FastAPI con SQLAlchemy ORM y base de datos SQLite.
- **Frontend**: React 18 con Vite, Chart.js para visualizaciones.
- **Flujo de Datos**: Importación de archivos bancarios → Parsing con Pandas → Auto-categorización con reglas regex → Almacenamiento de transacciones → Agregación para dashboard.

## Pasos para Ejecutar la Aplicación

### 1. Prerrequisitos
- Python 3.10 o superior (instalado y disponible en PATH).
- Node.js 18 o superior (instalado y disponible en PATH).

### 2. Configuración del Backend
1. Navegar al directorio del backend:
   ```
   cd backend
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
   - Esto instala FastAPI, SQLAlchemy, Pandas, etc.

3. Inicializar la base de datos:
   ```
   python -m app.db.init_db
   ```
   - Crea las tablas en SQLite (finance.db).

4. Cargar datos iniciales (opcional, pero recomendado):
   ```
   python -m app.db.seed
   ```
   - Crea cuentas, categorías e invoice categories por defecto.

5. Ejecutar el servidor backend:
   ```
   cd backend
   $env:PYTHONPATH = "d:\Programas\Temp\Gastos\backend"
   uvicorn app.main:app --reload
   ```
   - El servidor estará disponible en `http://localhost:8000`.
   - Documentación API en `http://localhost:8000/docs`.

### 3. Configuración del Frontend
1. Navegar al directorio del frontend:
   ```
   cd frontend
   ```

2. Instalar dependencias:
   ```
   npm install
   ```
   - Instala React, Vite, Axios, Chart.js, etc.

3. Ejecutar el servidor de desarrollo:
   ```
   npm run dev
   ```
   - La aplicación web estará disponible en `http://localhost:5173`.

### 4. Uso de la Aplicación
1. **Acceder a la aplicación**: Abrir `http://localhost:5173` en el navegador.
2. **Dashboard**: Visualizar balance, ingresos, gastos y gráficos de flujo de caja.
3. **Importar datos**:
   - Ir a la pestaña "Import".
   - Seleccionar el banco (CaixaBank, ING, Sabadell, Revolut).
   - Subir el archivo Excel/CSV descargado del banco.
   - El sistema parsea, categoriza automáticamente y guarda las transacciones.
4. **Ver transacciones**: En la pestaña "Transactions", ver tabla filtrable de movimientos.
5. **Gestionar facturas**: En "Invoices", subir y gestionar facturas con categorías específicas.

### 4.1 Acceso Externo vía API
La aplicación permite acceso externo seguro para crear facturas e importar archivos mediante API keys.

- **API Key por defecto**: `financeflow-api-key-2026` (configurada en seed data).
- **Headers requeridos**: `X-API-Key: <tu-api-key>`
- **Endpoints protegidos**:
  - `POST /api/v1/upload/` - Importar transacciones bancarias.
  - `POST /api/v1/invoices/upload` - Crear facturas con archivo adjunto.
- **Ejemplo de uso**:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/upload/" \
    -H "X-API-Key: financeflow-api-key-2026" \
    -F "file=@archivo.xlsx" \
    -F "bank_name=CAIXA" \
    -F "account_id=1"
  ```

### 5. Desarrollo y Testing
- **Ejecutar tests**: Desde `backend`, correr `pytest`.
- **API Endpoints**: Ver en `/docs` para endpoints de accounts, categories, transactions, upload, invoices.
- **Base de datos**: Archivo `finance.db` en el directorio backend.

### 6. Notas Importantes
- El backend debe estar corriendo para que el frontend funcione (llamadas API).
- Los archivos subidos se almacenan temporalmente y luego permanentemente en `backend/uploads/invoices/`.
- La auto-categorización usa reglas regex definidas en la tabla `import_rules`.
- Para detener los servidores: Ctrl+C en las terminales respectivas.

### 7. Posibles Problemas y Soluciones
- **Error de módulo 'app'**: Asegurarse de que PYTHONPATH esté configurado correctamente al ejecutar uvicorn.
- **Dependencias faltantes**: Verificar que pip y npm instalen correctamente.
- **Puerto ocupado**: Cambiar puertos si 8000 o 5173 están en uso.
- **Base de datos**: Si hay problemas, eliminar `finance.db` y reinicializar.

¡La aplicación está lista para usar! Disfruta gestionando tus finanzas personales.</content>
<parameter name="filePath">d:\Programas\Temp\Gastos\resumen-flujo.md