# Development Setup Guide

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan panduan awal untuk menyiapkan environment development ResearchAI.

Development Setup Guide digunakan sebagai acuan sebelum mulai membangun backend, frontend, database, dan integrasi AI.

---

# 2. Target Environment

Environment awal:

- Operating System: Windows
- Project Folder: D:\ResearchAI
- Version Control: Git + GitHub
- Backend: Python + FastAPI
- Frontend: React
- Database: PostgreSQL
- Styling: Tailwind CSS
- AI: OpenAI API
- Deployment Preparation: Docker

---

# 3. Tools Yang Dibutuhkan

Tools utama:

- Git
- GitHub account
- Visual Studio Code
- Python
- Node.js
- PostgreSQL
- Docker Desktop
- Browser

Tools tambahan yang berguna:

- Postman atau Insomnia untuk testing API
- DBeaver atau pgAdmin untuk melihat database

---

# 4. Repository

Repository GitHub:

```text
https://github.com/saharailal2020-code/ResearchAI
```

Folder lokal:

```text
D:\ResearchAI
```

Perintah umum Git:

```powershell
git status
git add .
git commit -m "Commit message"
git push
```

---

# 5. Struktur Aplikasi Yang Direncanakan

Struktur folder development yang disarankan:

```text
D:\ResearchAI
├── backend
├── frontend
├── database
├── storage
├── docs
├── docker
├── 00_Project_Management
├── 01_Product_Management
├── 02_UI_UX
├── 03_Database
├── 04_Backend
├── 05_Frontend
├── 06_AI
├── 07_Report_Generator
├── 08_API
├── 09_Testing
├── 10_Deployment
├── 11_Documentation
└── 12_Assets
```

Catatan:

Folder dokumentasi yang sudah ada tetap dipertahankan. Folder `backend`, `frontend`, `database`, `storage`, dan `docker` dapat dibuat saat mulai coding.

---

# 6. Backend Setup Plan

Backend menggunakan:

- Python
- FastAPI
- Uvicorn
- SQLAlchemy atau SQLModel
- Alembic untuk migration
- Pydantic untuk schema validation
- python-dotenv untuk environment variable

Folder backend yang disarankan:

```text
backend
├── app
│   ├── main.py
│   ├── core
│   ├── models
│   ├── schemas
│   ├── api
│   ├── services
│   └── utils
├── alembic
├── requirements.txt
└── .env.example
```

Perintah awal yang akan digunakan saat backend dibuat:

```powershell
cd D:\ResearchAI\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary pydantic python-dotenv
pip freeze > requirements.txt
uvicorn app.main:app --reload
```

Backend development URL:

```text
http://localhost:8000
```

API base URL:

```text
http://localhost:8000/api/v1
```

---

# 7. Frontend Setup Plan

Frontend menggunakan:

- React
- Vite
- Tailwind CSS
- React Router
- Axios atau fetch API

Folder frontend yang disarankan:

```text
frontend
├── src
│   ├── app
│   ├── components
│   ├── pages
│   ├── layouts
│   ├── services
│   ├── hooks
│   └── styles
├── public
├── package.json
└── .env.example
```

Perintah awal yang akan digunakan saat frontend dibuat:

```powershell
cd D:\ResearchAI
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npm install react-router-dom axios
npm run dev
```

Frontend development URL:

```text
http://localhost:5173
```

---

# 8. Database Setup Plan

Database menggunakan:

- PostgreSQL

Database development:

```text
researchai_dev
```

Database user contoh:

```text
researchai_user
```

Connection string contoh:

```text
postgresql://researchai_user:password@localhost:5432/researchai_dev
```

Catatan:

Password asli tidak boleh ditulis di dokumentasi publik atau di-commit ke GitHub.

---

# 9. Environment Variables

Backend `.env.example`:

```text
APP_ENV=development
DATABASE_URL=postgresql://researchai_user:password@localhost:5432/researchai_dev
SECRET_KEY=change_this_secret_key
OPENAI_API_KEY=your_openai_api_key
FILE_STORAGE_PATH=../storage
FRONTEND_URL=http://localhost:5173
```

Frontend `.env.example`:

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Aturan penting:

- File `.env` tidak boleh di-commit ke GitHub.
- File `.env.example` boleh di-commit sebagai contoh.
- API key asli tidak boleh ditulis di dokumen.

---

# 10. File Storage Setup

Folder storage lokal:

```text
D:\ResearchAI\storage
```

Subfolder yang disarankan:

```text
storage
├── proposals
├── datasets
├── reports
└── temp
```

Catatan:

Folder `storage` dapat dimasukkan ke `.gitignore` agar file upload tidak masuk GitHub.

---

# 11. Docker Setup Plan

Docker akan digunakan untuk menjalankan beberapa service secara konsisten.

Service awal:

- backend
- frontend
- postgres

File yang direncanakan:

```text
docker-compose.yml
backend/Dockerfile
frontend/Dockerfile
```

Perintah Docker yang akan digunakan:

```powershell
docker compose up --build
docker compose down
```

Catatan:

Docker setup dapat dibuat setelah backend dan frontend basic sudah tersedia.

---

# 12. Recommended Development Order

Urutan setup dan coding yang disarankan:

1. Buat folder backend.
2. Setup FastAPI basic.
3. Buat endpoint health check.
4. Setup PostgreSQL connection.
5. Buat migration awal users dan roles.
6. Buat authentication basic.
7. Buat folder frontend.
8. Setup React basic.
9. Buat login page.
10. Hubungkan frontend ke backend.
11. Buat client management.
12. Buat proposal management.
13. Buat project management.

---

# 13. Health Check

Backend perlu memiliki endpoint health check:

```text
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "ResearchAI API"
}
```

Tujuan:

- Memastikan backend berjalan.
- Memudahkan testing awal.
- Menjadi titik awal sebelum endpoint lain dibuat.

---

# 14. Git Ignore Plan

File dan folder yang sebaiknya tidak masuk Git:

```text
.env
.venv
node_modules
__pycache__
.pytest_cache
dist
build
storage
*.log
```

File yang boleh masuk Git:

```text
.env.example
requirements.txt
package.json
README.md
documentation files
source code
```

---

# 15. Testing Plan Awal

Testing awal:

- Backend health check
- Auth login
- User creation
- Client creation
- Proposal creation
- Project creation

Tools:

- Browser untuk frontend
- Postman atau Insomnia untuk API
- Pytest untuk backend pada tahap berikutnya

---

# 16. Development Checklist

Checklist sebelum mulai coding:

- Git repository sudah aktif.
- GitHub repository sudah tersambung.
- Technology Stack sudah diputuskan.
- System Architecture sudah dibuat.
- Database Schema sudah dibuat.
- API Requirement sudah dibuat.
- Python tersedia.
- Node.js tersedia.
- PostgreSQL tersedia.
- Docker Desktop tersedia atau direncanakan.
- `.env.example` dibuat saat backend/frontend mulai dibuat.
- `.gitignore` dibuat sebelum ada file secret atau dependency besar.

---

# 17. Catatan Untuk Developer

Catatan penting:

- Jangan commit API key.
- Jangan commit password database asli.
- Jangan commit file upload user.
- Mulai dari backend paling kecil dulu.
- Pastikan setiap modul punya dokumentasi.
- Commit perubahan kecil secara bertahap.
- Push ke GitHub setelah perubahan stabil.

---

# 18. Dokumen Terkait

- Technology Stack v0.1
- System Architecture v0.1
- Database Schema v0.1
- API Requirement v0.1
- Module Roadmap v0.1

---

# 19. Status

Dokumen ini masih berstatus draft dan akan diperbarui ketika backend, frontend, Docker, dan database mulai dibuat.
