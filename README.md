# 💰 FinanceFlow - Gestor de Gastos Personales

Aplicación web moderna para el control y análisis de finanzas personales. Permite importar movimientos bancarios, categorizarlos automáticamente y visualizar el estado financiero mediante gráficos interactivos.

## 🚀 Características

- **Dashboard Interactivo**: Visualización de Balance, Ingresos y Gastos con gráficos de flujo de caja.
- **Importación Bancaria**: Soporte para archivos Excel/CSV de:
  - CaixaBank
  - ING
  - Sabadell
  - Revolut
- **Auto-categorización**: Motor inteligente (basado en reglas Regex) para clasificar movimientos automáticamente.
- **Gestión de Transacciones**: Tabla filtrable y ordenable de todos los movimientos.
- **Diseño Responsive**: Interfaz moderna (Modo Oscuro/Premium) adaptada a distintos dispositivos.

## 🛠️ Tecnologías

### Backend
- **Python 3.10+**
- **FastAPI**: Framework API de alto rendimiento.
- **SQLAlchemy & SQLite**: Base de datos relacional ligera.
- **Pandas**: Procesamiento eficiente de archivos Excel/CSV.

### Frontend
- **React 18** (Vite): SPA rápida y optimizada.
- **Chart.js**: Visualización de datos.
- **Axios**: Comunicación HTTP con el backend.
- **CSS Modules**: Estilizado moderno y modular.

## 📂 Estructura del Proyecto

```
Gastos/
├── backend/            # API Servidor (FastAPI)
│   ├── app/
│   │   ├── api/        # Endpoints (Routes)
│   │   ├── db/         # Modelos y Schemas (SQLAlchemy/Pydantic)
│   │   ├── services/   # Lógica de negocio (Importadores, Categorizador)
│   │   └── main.py     # Punto de entrada
│   └── requirements.txt
│
├── frontend/           # Cliente Web (React)
│   ├── src/
│   │   ├── components/ # Componentes UI reutilizables
│   │   ├── pages/      # Vistas principales (Dashboard, Import, etc)
│   │   └── services/   # Cliente API
│   └── package.json
│
└── README.md
```

## ⚙️ Instalación y Ejecución

### Prerrequisitos
- Python 3.10 o superior
- Node.js 18 o superior

### 1. Configurar y Arrancar el Backend

Desde la carpeta raíz del proyecto:

```bash
cd backend

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Inicializar la Base de Datos (crea finance.db)
python -m app.db.init_db

# 3. Arrancar el servidor
uvicorn app.main:app --reload
```
El servidor estará disponible en `http://localhost:8000`.  
Documentación API (Swagger): `http://localhost:8000/docs`.

### 2. Configurar y Arrancar el Frontend

Abrir una nueva terminal y navegar a la carpeta frontend:

```bash
cd frontend

# 1. Instalar dependencias
npm install

# 2. Arrancar el servidor de desarrollo
npm run dev
```
La aplicación web se abrirá en `http://localhost:5173`.

## 🧪 Uso Básico

1. **Crear Cuenta**: El sistema crea cuentas bancarias por defecto o puedes añadirlas vía API/Base de datos.
2. **Importar**: Ve a la pestaña "Import", selecciona tu banco y sube el archivo `.xlsx` o `.csv` descargado de tu entidad.
3. **Analizar**: Ve al "Dashboard" para ver tus métricas financieras actualizadas al instante.

---
Desarrollado con ❤️ para una mejor salud financiera.
