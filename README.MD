# Employee Payroll Management API


### 1.Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 2.Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Database Setup

Ensure PostgreSQL is installed and running.

Open PostgreSQL using pgAdmin or the `psql` terminal.

Create the development and testing databases:

```sql
CREATE DATABASE employee_payroll_db;

CREATE DATABASE employee_payroll_test_db;
```

Ensure the application's existing database configuration points to the correct PostgreSQL database.

## 4. Run Database Migrations

From the project root directory, execute:

```bash
alembic upgrade head
```

This command:

- Creates the required database tables.
- Inserts sample employee and salary data.
- Creates the `sp_increase_salary` stored procedure.

## 5. Create Admin User

Run the admin creation script:

```bash
python create_admin.py
```

This initializes the administrator account using the configured admin credentials.

## 6. Start the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

**API Base URL:** http://127.0.0.1:8000

### API Documentation

FastAPI provides interactive API documentation.

**Swagger UI**

http://127.0.0.1:8000/docs

**ReDoc**

http://127.0.0.1:8000/redoc

## 7. Run Tests

Execute the endpoint tests using pytest:

```bash
python -m pytest tests/test_endpoints.py -v
```

This runs the API tests and displays detailed results.

## 8. Quick Start

After installing dependencies and configuring the existing database settings, use the following commands in order:

```bash
# Apply database migrations
alembic upgrade head

# Create administrator
python create_admin.py

#Generate Secret Key 
python -c "import secrets; print(secrets.token_hex(32))"

# Start FastAPI server
uvicorn app.main:app --reload
```

To run tests separately:

```bash
python -m pytest tests/test_endpoints.py -v
```