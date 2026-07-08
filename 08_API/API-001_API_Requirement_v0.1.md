# API Requirement

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan kebutuhan API awal ResearchAI pada tahap MVP.

API Requirement menjadi dasar untuk pengembangan backend FastAPI, integrasi frontend React, dan komunikasi antar komponen sistem.

---

# 2. Prinsip API

Prinsip API ResearchAI:

1. API menggunakan HTTP.
2. Format request dan response utama menggunakan JSON.
3. File upload menggunakan multipart form data.
4. Endpoint mengikuti struktur resource-based.
5. Endpoint internal harus menggunakan authentication.
6. Akses data dibatasi berdasarkan role pengguna.
7. Response harus konsisten agar mudah digunakan frontend.

---

# 3. Base URL

Base URL development:

```text
http://localhost:8000/api/v1
```

Base URL production:

```text
https://researchai.example.com/api/v1
```

Catatan:

URL production masih placeholder dan akan diperbarui setelah deployment diputuskan.

---

# 4. Authentication

Authentication awal menggunakan token-based authentication.

Header request untuk endpoint yang membutuhkan login:

```text
Authorization: Bearer <access_token>
```

Endpoint publik:

- POST /auth/login

Endpoint internal:

- Semua endpoint selain login membutuhkan token.

---

# 5. Standard Response Format

## 5.1 Success Response

```json
{
  "success": true,
  "message": "Request successful",
  "data": {}
}
```

## 5.2 Error Response

```json
{
  "success": false,
  "message": "Error message",
  "errors": []
}
```

## 5.3 Paginated Response

```json
{
  "success": true,
  "message": "Request successful",
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

---

# 6. HTTP Status Code

Status code awal:

| Code | Meaning | Usage |
| --- | --- | --- |
| 200 | OK | Request berhasil |
| 201 | Created | Data berhasil dibuat |
| 400 | Bad Request | Input tidak valid |
| 401 | Unauthorized | Belum login atau token tidak valid |
| 403 | Forbidden | Tidak punya akses |
| 404 | Not Found | Data tidak ditemukan |
| 422 | Validation Error | Validasi data gagal |
| 500 | Server Error | Error internal server |

---

# 7. Authentication API

## POST /auth/login

Fungsi:

Login pengguna.

Request:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "token",
    "token_type": "bearer",
    "user": {
      "id": "uuid",
      "full_name": "User Name",
      "email": "user@example.com",
      "roles": ["Project Manager"]
    }
  }
}
```

Prioritas:

High

---

## POST /auth/logout

Fungsi:

Logout pengguna.

Authentication:

Required

Response:

```json
{
  "success": true,
  "message": "Logout successful",
  "data": null
}
```

Prioritas:

High

---

## GET /auth/me

Fungsi:

Mengambil profil pengguna yang sedang login.

Authentication:

Required

Response:

```json
{
  "success": true,
  "message": "User profile retrieved",
  "data": {
    "id": "uuid",
    "full_name": "User Name",
    "email": "user@example.com",
    "roles": ["Project Manager"]
  }
}
```

Prioritas:

High

---

# 8. Users API

## GET /users

Fungsi:

Menampilkan daftar pengguna.

Authentication:

Required

Role:

- System Administrator

Query parameters:

- page
- limit
- search
- status
- role

Prioritas:

High

---

## POST /users

Fungsi:

Membuat pengguna baru.

Authentication:

Required

Role:

- System Administrator

Request:

```json
{
  "full_name": "User Name",
  "email": "user@example.com",
  "password": "temporary_password",
  "role_ids": ["uuid"]
}
```

Prioritas:

High

---

## GET /users/{user_id}

Fungsi:

Melihat detail pengguna.

Authentication:

Required

Role:

- System Administrator

Prioritas:

High

---

## PATCH /users/{user_id}

Fungsi:

Mengubah data pengguna.

Authentication:

Required

Role:

- System Administrator

Prioritas:

High

---

## PATCH /users/{user_id}/status

Fungsi:

Mengaktifkan atau menonaktifkan pengguna.

Authentication:

Required

Role:

- System Administrator

Request:

```json
{
  "status": "active"
}
```

Prioritas:

High

---

# 9. Roles API

## GET /roles

Fungsi:

Menampilkan daftar role.

Authentication:

Required

Role:

- System Administrator
- Research Manager

Prioritas:

High

---

## POST /users/{user_id}/roles

Fungsi:

Mengatur role pengguna.

Authentication:

Required

Role:

- System Administrator

Request:

```json
{
  "role_ids": ["uuid"]
}
```

Prioritas:

High

---

# 10. Clients API

## GET /clients

Fungsi:

Menampilkan daftar klien.

Authentication:

Required

Query parameters:

- page
- limit
- search
- industry
- status

Prioritas:

High

---

## POST /clients

Fungsi:

Membuat data klien.

Authentication:

Required

Role:

- Marketing
- Project Manager
- Research Manager

Request:

```json
{
  "client_name": "Client Name",
  "industry": "Banking",
  "client_type": "prospect",
  "notes": "Initial client note",
  "primary_contact": {
    "contact_name": "Contact Name",
    "position": "Manager",
    "email": "contact@example.com",
    "phone": "08123456789"
  }
}
```

Prioritas:

High

---

## GET /clients/{client_id}

Fungsi:

Melihat detail klien.

Authentication:

Required

Response data:

- Client profile
- Client contacts
- Proposal history
- Project history

Prioritas:

High

---

## PATCH /clients/{client_id}

Fungsi:

Mengubah data klien.

Authentication:

Required

Role:

- Marketing
- Research Manager
- System Administrator

Prioritas:

Medium

---

## POST /clients/{client_id}/contacts

Fungsi:

Menambahkan kontak klien.

Authentication:

Required

Prioritas:

Medium

---

# 11. Proposals API

## GET /proposals

Fungsi:

Menampilkan daftar proposal.

Authentication:

Required

Query parameters:

- page
- limit
- search
- client_id
- status
- research_type

Prioritas:

High

---

## POST /proposals

Fungsi:

Membuat proposal baru.

Authentication:

Required

Request:

```json
{
  "client_id": "uuid",
  "proposal_title": "Customer Satisfaction Survey",
  "research_type": "Customer Satisfaction",
  "research_objective": "Measure customer satisfaction",
  "methodology_summary": "Quantitative survey",
  "estimated_timeline": "4 weeks",
  "estimated_budget": 50000000
}
```

Prioritas:

High

---

## GET /proposals/{proposal_id}

Fungsi:

Melihat detail proposal.

Authentication:

Required

Prioritas:

High

---

## PATCH /proposals/{proposal_id}

Fungsi:

Mengubah data proposal.

Authentication:

Required

Prioritas:

Medium

---

## PATCH /proposals/{proposal_id}/status

Fungsi:

Mengubah status proposal.

Authentication:

Required

Request:

```json
{
  "status": "Approved"
}
```

Status:

- Draft
- Sent
- Revised
- Approved
- Rejected

Prioritas:

High

---

## POST /proposals/{proposal_id}/files

Fungsi:

Upload file proposal.

Authentication:

Required

Request:

multipart form data

Prioritas:

Medium

---

## POST /proposals/{proposal_id}/generate-draft

Fungsi:

Membuat draft proposal dengan AI.

Authentication:

Required

Request:

```json
{
  "instruction": "Create proposal draft based on current proposal data"
}
```

Prioritas:

Medium

---

# 12. Projects API

## GET /projects

Fungsi:

Menampilkan daftar proyek.

Authentication:

Required

Query parameters:

- page
- limit
- search
- client_id
- status
- project_manager_id

Prioritas:

High

---

## POST /projects

Fungsi:

Membuat proyek baru.

Authentication:

Required

Request:

```json
{
  "client_id": "uuid",
  "proposal_id": "uuid",
  "project_name": "Customer Satisfaction Survey 2026",
  "project_code": "CSS-2026-001",
  "research_type": "Customer Satisfaction",
  "project_manager_id": "uuid",
  "start_date": "2026-07-08",
  "end_date": "2026-08-08"
}
```

Prioritas:

High

---

## POST /proposals/{proposal_id}/create-project

Fungsi:

Membuat proyek dari proposal yang sudah approved.

Authentication:

Required

Rule:

- Proposal harus berstatus Approved.

Prioritas:

High

---

## GET /projects/{project_id}

Fungsi:

Melihat detail proyek.

Authentication:

Required

Response data:

- Project summary
- Client information
- Team members
- Survey status
- Dataset status
- AI outputs
- Reports

Prioritas:

High

---

## PATCH /projects/{project_id}

Fungsi:

Mengubah data proyek.

Authentication:

Required

Prioritas:

Medium

---

## PATCH /projects/{project_id}/status

Fungsi:

Mengubah status proyek.

Authentication:

Required

Status:

- Project Active
- Research Design
- Fieldwork
- Quality Control
- Data Processing
- Analysis
- Report Draft
- Report Final
- Delivered
- Closed

Prioritas:

High

---

## POST /projects/{project_id}/members

Fungsi:

Menambahkan anggota tim proyek.

Authentication:

Required

Request:

```json
{
  "user_id": "uuid",
  "project_role": "Data Analyst"
}
```

Prioritas:

High

---

## POST /projects/{project_id}/notes

Fungsi:

Menambahkan catatan proyek.

Authentication:

Required

Request:

```json
{
  "note": "Fieldwork started today",
  "note_type": "progress"
}
```

Prioritas:

Medium

---

# 13. Survey API

## POST /projects/{project_id}/survey-plan

Fungsi:

Membuat survey plan untuk proyek.

Authentication:

Required

Request:

```json
{
  "survey_method": "Online survey",
  "target_respondent": "Bank customers",
  "sample_size": 400,
  "area": "Indonesia",
  "start_date": "2026-07-10",
  "end_date": "2026-07-30"
}
```

Prioritas:

Medium

---

## GET /projects/{project_id}/survey-plan

Fungsi:

Melihat survey plan proyek.

Authentication:

Required

Prioritas:

Medium

---

## POST /survey-plans/{survey_plan_id}/progress

Fungsi:

Mencatat progress fieldwork.

Authentication:

Required

Request:

```json
{
  "progress_date": "2026-07-15",
  "completed_sample": 120,
  "target_sample": 400,
  "issue_notes": "No major issue"
}
```

Prioritas:

Medium

---

# 14. Quality Control API

## GET /quality-checks

Fungsi:

Menampilkan daftar QC.

Authentication:

Required

Query parameters:

- project_id
- dataset_id
- status

Prioritas:

High

---

## POST /quality-checks

Fungsi:

Mencatat hasil QC.

Authentication:

Required

Request:

```json
{
  "project_id": "uuid",
  "dataset_id": "uuid",
  "total_checked": 100,
  "valid_count": 95,
  "invalid_count": 5,
  "status": "passed",
  "notes": "Data quality acceptable"
}
```

Prioritas:

High

---

## GET /quality-checks/{quality_check_id}

Fungsi:

Melihat detail QC.

Authentication:

Required

Prioritas:

High

---

# 15. Data Processing API

## GET /datasets

Fungsi:

Menampilkan daftar dataset.

Authentication:

Required

Query parameters:

- project_id
- status
- uploaded_by

Prioritas:

High

---

## POST /projects/{project_id}/datasets

Fungsi:

Upload dataset proyek.

Authentication:

Required

Request:

multipart form data

Prioritas:

High

---

## GET /datasets/{dataset_id}

Fungsi:

Melihat detail dataset.

Authentication:

Required

Prioritas:

High

---

## PATCH /datasets/{dataset_id}/status

Fungsi:

Mengubah status dataset.

Authentication:

Required

Request:

```json
{
  "status": "Ready for Analysis"
}
```

Status:

- Uploaded
- Cleaning
- Validated
- Ready for Analysis

Prioritas:

High

---

## POST /datasets/{dataset_id}/notes

Fungsi:

Menambahkan catatan data processing.

Authentication:

Required

Request:

```json
{
  "note": "Removed duplicate records"
}
```

Prioritas:

Medium

---

# 16. AI Analysis API

## POST /ai/project-summary

Fungsi:

Membuat ringkasan proyek dengan AI.

Authentication:

Required

Request:

```json
{
  "project_id": "uuid",
  "instruction": "Create a concise project summary"
}
```

Response:

```json
{
  "success": true,
  "message": "AI output generated",
  "data": {
    "ai_output_id": "uuid",
    "output_type": "Project Summary",
    "status": "Draft",
    "output_content": "Generated summary"
  }
}
```

Prioritas:

High

---

## POST /ai/insight-draft

Fungsi:

Membuat draft insight dengan AI.

Authentication:

Required

Request:

```json
{
  "project_id": "uuid",
  "dataset_id": "uuid",
  "instruction": "Generate key insights"
}
```

Prioritas:

High

---

## POST /ai/executive-summary

Fungsi:

Membuat executive summary dengan AI.

Authentication:

Required

Request:

```json
{
  "project_id": "uuid",
  "instruction": "Create executive summary"
}
```

Prioritas:

High

---

## POST /ai/recommendation-draft

Fungsi:

Membuat draft rekomendasi dengan AI.

Authentication:

Required

Request:

```json
{
  "project_id": "uuid",
  "instruction": "Generate strategic recommendations"
}
```

Prioritas:

Medium

---

## GET /projects/{project_id}/ai-outputs

Fungsi:

Menampilkan output AI untuk proyek.

Authentication:

Required

Prioritas:

High

---

## PATCH /ai-outputs/{ai_output_id}/review

Fungsi:

Mereview output AI.

Authentication:

Required

Request:

```json
{
  "status": "Approved",
  "edited_content": "Reviewed and edited content"
}
```

Prioritas:

High

---

# 17. Reports API

## GET /reports

Fungsi:

Menampilkan daftar laporan.

Authentication:

Required

Query parameters:

- project_id
- status

Prioritas:

High

---

## POST /projects/{project_id}/reports

Fungsi:

Membuat laporan proyek.

Authentication:

Required

Request:

```json
{
  "report_title": "Final Research Report",
  "report_type": "Final Report"
}
```

Prioritas:

High

---

## GET /reports/{report_id}

Fungsi:

Melihat detail laporan.

Authentication:

Required

Prioritas:

High

---

## POST /reports/{report_id}/sections

Fungsi:

Menambahkan section laporan.

Authentication:

Required

Request:

```json
{
  "section_title": "Executive Summary",
  "section_order": 1,
  "content": "Section content"
}
```

Prioritas:

High

---

## PATCH /report-sections/{section_id}

Fungsi:

Mengubah section laporan.

Authentication:

Required

Prioritas:

High

---

## PATCH /reports/{report_id}/status

Fungsi:

Mengubah status laporan.

Authentication:

Required

Status:

- Draft
- Review
- Revised
- Final
- Delivered

Prioritas:

Medium

---

# 18. Files API

## POST /files/upload

Fungsi:

Upload file umum.

Authentication:

Required

Request:

multipart form data

Prioritas:

Medium

---

## GET /files/{file_id}

Fungsi:

Mengambil metadata file.

Authentication:

Required

Prioritas:

Medium

---

## GET /files/{file_id}/download

Fungsi:

Download file.

Authentication:

Required

Prioritas:

Medium

---

# 19. Dashboard API

## GET /dashboard/summary

Fungsi:

Menampilkan ringkasan dashboard sesuai role pengguna.

Authentication:

Required

Response data:

- Active projects count
- Running proposals count
- Project status summary
- Dataset status summary
- Report status summary

Prioritas:

Medium

---

## GET /dashboard/my-tasks

Fungsi:

Menampilkan pekerjaan pengguna yang sedang login.

Authentication:

Required

Prioritas:

Medium

---

# 20. MVP Endpoint Priority

Endpoint yang wajib diprioritaskan untuk MVP awal:

- POST /auth/login
- POST /auth/logout
- GET /auth/me
- GET /users
- POST /users
- GET /roles
- GET /clients
- POST /clients
- GET /clients/{client_id}
- GET /proposals
- POST /proposals
- GET /proposals/{proposal_id}
- PATCH /proposals/{proposal_id}/status
- POST /proposals/{proposal_id}/create-project
- GET /projects
- POST /projects
- GET /projects/{project_id}
- PATCH /projects/{project_id}/status
- POST /projects/{project_id}/members
- POST /projects/{project_id}/survey-plan
- POST /quality-checks
- POST /projects/{project_id}/datasets
- PATCH /datasets/{dataset_id}/status
- POST /ai/project-summary
- POST /ai/insight-draft
- POST /ai/executive-summary
- POST /projects/{project_id}/reports
- GET /reports/{report_id}
- POST /reports/{report_id}/sections
- GET /dashboard/summary

---

# 21. Dokumen Terkait

- Functional Requirement v0.1
- Database Schema v0.1
- System Architecture v0.1
- UI/UX User Flow v0.1

---

# 22. Status

Dokumen ini masih berstatus draft dan akan diperbarui saat backend FastAPI mulai dikembangkan.
