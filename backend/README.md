# ResearchAI Backend

Backend ResearchAI menggunakan Python dan FastAPI.

## Development URL

```text
http://localhost:8000
```

## Health Check

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ResearchAI API",
  "version": "0.1.0"
}
```

## Database Health Check

Start PostgreSQL:

```powershell
docker compose up -d postgres
```

Run backend:

```powershell
uvicorn app.main:app --reload
```

Check database:

```text
GET /api/v1/db/health
```

## Authentication Bootstrap

Create authentication tables and the local admin user:

```powershell
cd D:\ResearchAI\backend
.\.venv\Scripts\python.exe .\scripts\init_auth.py
```

Development admin:

```text
Email: admin@researchai.local
Password: Admin123!
```
