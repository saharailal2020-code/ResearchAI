# Database Schema

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan rancangan schema database awal ResearchAI untuk tahap MVP.

Database Schema menjadi dasar untuk membuat migration, backend model, API implementation, dan ERD.

---

# 2. Database Engine

Database yang digunakan:

PostgreSQL

Prinsip umum:

- Primary key menggunakan UUID.
- Waktu dibuat dan diubah disimpan dengan timestamp.
- Foreign key digunakan untuk menjaga hubungan antar tabel.
- Status disimpan sebagai string pada tahap awal agar mudah dikembangkan.
- Soft delete dapat ditambahkan pada tahap berikutnya jika dibutuhkan.

---

# 3. Standard Columns

Kolom standar yang disarankan untuk sebagian besar tabel:

| Column | Type | Description |
| --- | --- | --- |
| id | UUID | Primary key |
| created_at | TIMESTAMP | Waktu data dibuat |
| updated_at | TIMESTAMP | Waktu data terakhir diubah |

Kolom audit tambahan jika dibutuhkan:

| Column | Type | Description |
| --- | --- | --- |
| created_by | UUID | User yang membuat data |
| updated_by | UUID | User yang terakhir mengubah data |

---

# 4. User and Access Tables

## 4.1 users

Fungsi:

Menyimpan data pengguna ResearchAI.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID pengguna |
| full_name | VARCHAR(150) | NOT NULL | Nama lengkap |
| email | VARCHAR(150) | UNIQUE, NOT NULL | Email login |
| password_hash | TEXT | NOT NULL | Password yang sudah di-hash |
| status | VARCHAR(30) | NOT NULL | active, inactive |
| last_login_at | TIMESTAMP | NULL | Login terakhir |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- email
- status

---

## 4.2 roles

Fungsi:

Menyimpan daftar role pengguna.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID role |
| role_name | VARCHAR(100) | UNIQUE, NOT NULL | Nama role |
| description | TEXT | NULL | Deskripsi role |
| status | VARCHAR(30) | NOT NULL | active, inactive |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- role_name
- status

---

## 4.3 user_roles

Fungsi:

Menghubungkan users dan roles.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID user role |
| user_id | UUID | FK users.id, NOT NULL | ID user |
| role_id | UUID | FK roles.id, NOT NULL | ID role |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- user_id
- role_id
- user_id + role_id unique

---

# 5. Client Tables

## 5.1 clients

Fungsi:

Menyimpan data klien.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID klien |
| client_name | VARCHAR(200) | NOT NULL | Nama klien |
| industry | VARCHAR(100) | NULL | Industri klien |
| client_type | VARCHAR(50) | NULL | prospect, active, inactive |
| status | VARCHAR(30) | NOT NULL | active, inactive |
| notes | TEXT | NULL | Catatan klien |
| created_by | UUID | FK users.id | Pembuat data |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- client_name
- industry
- status

---

## 5.2 client_contacts

Fungsi:

Menyimpan kontak klien.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID kontak |
| client_id | UUID | FK clients.id, NOT NULL | ID klien |
| contact_name | VARCHAR(150) | NOT NULL | Nama kontak |
| position | VARCHAR(100) | NULL | Jabatan |
| email | VARCHAR(150) | NULL | Email kontak |
| phone | VARCHAR(50) | NULL | Nomor telepon |
| is_primary | BOOLEAN | NOT NULL | Kontak utama |
| notes | TEXT | NULL | Catatan kontak |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- client_id
- email
- is_primary

---

# 6. Proposal Tables

## 6.1 proposals

Fungsi:

Menyimpan data proposal riset.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID proposal |
| client_id | UUID | FK clients.id, NOT NULL | ID klien |
| proposal_title | VARCHAR(250) | NOT NULL | Judul proposal |
| research_type | VARCHAR(100) | NULL | Jenis riset |
| research_objective | TEXT | NULL | Tujuan riset |
| methodology_summary | TEXT | NULL | Ringkasan metodologi |
| estimated_timeline | VARCHAR(100) | NULL | Estimasi waktu |
| estimated_budget | NUMERIC(18,2) | NULL | Estimasi budget |
| status | VARCHAR(30) | NOT NULL | Status proposal |
| created_by | UUID | FK users.id | Pembuat proposal |
| approved_at | TIMESTAMP | NULL | Waktu disetujui |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Status:

- Draft
- Sent
- Revised
- Approved
- Rejected

Index:

- client_id
- status
- created_by

---

## 6.2 proposal_files

Fungsi:

Menghubungkan proposal dengan file.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID proposal file |
| proposal_id | UUID | FK proposals.id, NOT NULL | ID proposal |
| file_id | UUID | FK files.id, NOT NULL | ID file |
| file_type | VARCHAR(50) | NULL | draft, final, supporting |
| uploaded_by | UUID | FK users.id | Pengunggah |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- proposal_id
- file_id

---

# 7. Project Tables

## 7.1 projects

Fungsi:

Menyimpan data proyek riset.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID proyek |
| client_id | UUID | FK clients.id, NOT NULL | ID klien |
| proposal_id | UUID | FK proposals.id | ID proposal asal |
| project_name | VARCHAR(250) | NOT NULL | Nama proyek |
| project_code | VARCHAR(50) | UNIQUE | Kode proyek |
| research_type | VARCHAR(100) | NULL | Jenis riset |
| project_manager_id | UUID | FK users.id | Project manager |
| start_date | DATE | NULL | Tanggal mulai |
| end_date | DATE | NULL | Tanggal selesai |
| status | VARCHAR(50) | NOT NULL | Status proyek |
| created_by | UUID | FK users.id | Pembuat proyek |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

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

Index:

- client_id
- proposal_id
- project_manager_id
- status
- project_code

---

## 7.2 project_members

Fungsi:

Menyimpan anggota tim proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID anggota proyek |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| user_id | UUID | FK users.id, NOT NULL | ID user |
| project_role | VARCHAR(100) | NOT NULL | Role dalam proyek |
| assigned_at | TIMESTAMP | NOT NULL | Waktu ditugaskan |
| assigned_by | UUID | FK users.id | Pemberi tugas |

Index:

- project_id
- user_id
- project_id + user_id unique

---

## 7.3 project_milestones

Fungsi:

Menyimpan milestone proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID milestone |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| milestone_name | VARCHAR(200) | NOT NULL | Nama milestone |
| description | TEXT | NULL | Deskripsi |
| due_date | DATE | NULL | Tanggal target |
| status | VARCHAR(30) | NOT NULL | pending, in_progress, done |
| completed_at | TIMESTAMP | NULL | Waktu selesai |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- project_id
- status
- due_date

---

## 7.4 project_notes

Fungsi:

Menyimpan catatan proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID catatan |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| note | TEXT | NOT NULL | Isi catatan |
| note_type | VARCHAR(50) | NULL | progress, issue, decision |
| created_by | UUID | FK users.id | Pembuat catatan |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- project_id
- note_type
- created_by

---

# 8. Survey and Fieldwork Tables

## 8.1 survey_plans

Fungsi:

Menyimpan rencana survei per proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID survey plan |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| survey_method | VARCHAR(100) | NULL | Metode survei |
| target_respondent | TEXT | NULL | Target responden |
| sample_size | INTEGER | NULL | Jumlah sampel |
| area | TEXT | NULL | Area survei |
| start_date | DATE | NULL | Tanggal mulai |
| end_date | DATE | NULL | Tanggal selesai |
| status | VARCHAR(30) | NOT NULL | planned, active, completed |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- project_id
- status

---

## 8.2 fieldwork_progress

Fungsi:

Menyimpan progress fieldwork.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID progress |
| survey_plan_id | UUID | FK survey_plans.id, NOT NULL | ID survey plan |
| progress_date | DATE | NOT NULL | Tanggal progress |
| completed_sample | INTEGER | NOT NULL | Sampel selesai |
| target_sample | INTEGER | NULL | Target sampel |
| issue_notes | TEXT | NULL | Catatan kendala |
| reported_by | UUID | FK users.id | Pelapor |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- survey_plan_id
- progress_date
- reported_by

---

# 9. Quality Control Tables

## 9.1 quality_checks

Fungsi:

Menyimpan hasil quality control.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID quality check |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| dataset_id | UUID | FK datasets.id | ID dataset |
| checked_by | UUID | FK users.id | Pemeriksa |
| total_checked | INTEGER | NULL | Total dicek |
| valid_count | INTEGER | NULL | Jumlah valid |
| invalid_count | INTEGER | NULL | Jumlah tidak valid |
| status | VARCHAR(30) | NOT NULL | pending, passed, issue_found |
| notes | TEXT | NULL | Catatan QC |
| checked_at | TIMESTAMP | NULL | Waktu pemeriksaan |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- project_id
- dataset_id
- checked_by
- status

---

## 9.2 quality_check_items

Fungsi:

Menyimpan detail masalah QC.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID item QC |
| quality_check_id | UUID | FK quality_checks.id, NOT NULL | ID QC |
| issue_type | VARCHAR(100) | NULL | Jenis masalah |
| issue_description | TEXT | NULL | Deskripsi masalah |
| severity | VARCHAR(30) | NULL | low, medium, high |
| status | VARCHAR(30) | NOT NULL | open, resolved |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- quality_check_id
- severity
- status

---

# 10. Data Processing Tables

## 10.1 datasets

Fungsi:

Menyimpan metadata dataset proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID dataset |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| dataset_name | VARCHAR(200) | NOT NULL | Nama dataset |
| file_id | UUID | FK files.id | ID file |
| dataset_type | VARCHAR(50) | NULL | raw, cleaned, final |
| status | VARCHAR(50) | NOT NULL | Status dataset |
| uploaded_by | UUID | FK users.id | Pengunggah |
| uploaded_at | TIMESTAMP | NULL | Waktu upload |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Status:

- Uploaded
- Cleaning
- Validated
- Ready for Analysis

Index:

- project_id
- file_id
- status
- uploaded_by

---

## 10.2 data_processing_notes

Fungsi:

Menyimpan catatan data cleaning dan data processing.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID catatan |
| dataset_id | UUID | FK datasets.id, NOT NULL | ID dataset |
| note | TEXT | NOT NULL | Isi catatan |
| created_by | UUID | FK users.id | Pembuat catatan |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- dataset_id
- created_by

---

# 11. AI Analysis Tables

## 11.1 ai_outputs

Fungsi:

Menyimpan output yang dibuat dengan bantuan AI.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID output AI |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| source_type | VARCHAR(50) | NULL | proposal, dataset, report |
| source_id | UUID | NULL | ID sumber |
| output_type | VARCHAR(100) | NOT NULL | Jenis output AI |
| prompt_summary | TEXT | NULL | Ringkasan prompt |
| output_content | TEXT | NOT NULL | Hasil AI |
| status | VARCHAR(30) | NOT NULL | draft, reviewed, approved, rejected |
| generated_by | UUID | FK users.id | Pembuat request |
| reviewed_by | UUID | FK users.id | Reviewer |
| reviewed_at | TIMESTAMP | NULL | Waktu review |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- project_id
- output_type
- status
- generated_by

---

# 12. Report Tables

## 12.1 reports

Fungsi:

Menyimpan data laporan proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID laporan |
| project_id | UUID | FK projects.id, NOT NULL | ID proyek |
| report_title | VARCHAR(250) | NOT NULL | Judul laporan |
| report_type | VARCHAR(100) | NULL | Jenis laporan |
| status | VARCHAR(30) | NOT NULL | Status laporan |
| created_by | UUID | FK users.id | Pembuat laporan |
| reviewed_by | UUID | FK users.id | Reviewer |
| finalized_at | TIMESTAMP | NULL | Waktu final |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Status:

- Draft
- Review
- Revised
- Final
- Delivered

Index:

- project_id
- status
- created_by

---

## 12.2 report_sections

Fungsi:

Menyimpan bagian laporan.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID section |
| report_id | UUID | FK reports.id, NOT NULL | ID laporan |
| section_title | VARCHAR(200) | NOT NULL | Judul section |
| section_order | INTEGER | NOT NULL | Urutan section |
| content | TEXT | NULL | Konten section |
| ai_output_id | UUID | FK ai_outputs.id | Sumber AI |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- report_id
- section_order
- ai_output_id

---

## 12.3 report_files

Fungsi:

Menghubungkan report dengan file.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID report file |
| report_id | UUID | FK reports.id, NOT NULL | ID laporan |
| file_id | UUID | FK files.id, NOT NULL | ID file |
| file_type | VARCHAR(50) | NULL | draft, final, exported |
| uploaded_by | UUID | FK users.id | Pengunggah |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- report_id
- file_id

---

# 13. Knowledge Base Tables

## 13.1 knowledge_items

Fungsi:

Menyimpan knowledge dari proyek.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID knowledge |
| project_id | UUID | FK projects.id | ID proyek |
| client_id | UUID | FK clients.id | ID klien |
| title | VARCHAR(250) | NOT NULL | Judul knowledge |
| category | VARCHAR(100) | NOT NULL | Kategori |
| content | TEXT | NOT NULL | Isi knowledge |
| tags | TEXT | NULL | Tags sederhana |
| source_type | VARCHAR(50) | NULL | report, ai_output, manual |
| source_id | UUID | NULL | ID sumber |
| created_by | UUID | FK users.id | Pembuat |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |
| updated_at | TIMESTAMP | NOT NULL | Waktu diubah |

Index:

- project_id
- client_id
- category
- created_by

---

# 14. File and Activity Tables

## 14.1 files

Fungsi:

Menyimpan metadata file.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID file |
| file_name | VARCHAR(255) | NOT NULL | Nama file |
| file_path | TEXT | NOT NULL | Lokasi file |
| file_type | VARCHAR(100) | NULL | Tipe file |
| file_size | BIGINT | NULL | Ukuran file |
| module_name | VARCHAR(100) | NULL | Modul asal |
| uploaded_by | UUID | FK users.id | Pengunggah |
| uploaded_at | TIMESTAMP | NOT NULL | Waktu upload |
| created_at | TIMESTAMP | NOT NULL | Waktu dibuat |

Index:

- module_name
- uploaded_by
- uploaded_at

---

## 14.2 activity_logs

Fungsi:

Menyimpan aktivitas penting pengguna.

| Column | Type | Constraint | Description |
| --- | --- | --- | --- |
| id | UUID | PK | ID activity |
| user_id | UUID | FK users.id | ID user |
| activity_type | VARCHAR(100) | NOT NULL | Jenis aktivitas |
| module_name | VARCHAR(100) | NULL | Nama modul |
| entity_name | VARCHAR(100) | NULL | Nama entitas |
| entity_id | UUID | NULL | ID entitas |
| description | TEXT | NULL | Deskripsi aktivitas |
| created_at | TIMESTAMP | NOT NULL | Waktu aktivitas |

Index:

- user_id
- module_name
- entity_name
- entity_id
- created_at

---

# 15. MVP Table Priority

Tabel prioritas pertama:

- users
- roles
- user_roles
- clients
- client_contacts
- proposals
- projects
- project_members
- survey_plans
- quality_checks
- datasets
- ai_outputs
- reports
- report_sections
- files

Tabel prioritas kedua:

- proposal_files
- project_milestones
- project_notes
- fieldwork_progress
- quality_check_items
- data_processing_notes
- report_files
- knowledge_items
- activity_logs

---

# 16. Foreign Key Summary

Relasi utama:

- user_roles.user_id -> users.id
- user_roles.role_id -> roles.id
- client_contacts.client_id -> clients.id
- proposals.client_id -> clients.id
- projects.client_id -> clients.id
- projects.proposal_id -> proposals.id
- projects.project_manager_id -> users.id
- project_members.project_id -> projects.id
- project_members.user_id -> users.id
- survey_plans.project_id -> projects.id
- fieldwork_progress.survey_plan_id -> survey_plans.id
- quality_checks.project_id -> projects.id
- quality_checks.dataset_id -> datasets.id
- datasets.project_id -> projects.id
- datasets.file_id -> files.id
- ai_outputs.project_id -> projects.id
- reports.project_id -> projects.id
- report_sections.report_id -> reports.id
- report_sections.ai_output_id -> ai_outputs.id
- knowledge_items.project_id -> projects.id
- knowledge_items.client_id -> clients.id

---

# 17. Catatan Teknis

Catatan untuk implementasi:

- UUID dapat dibuat di backend atau database.
- Password harus disimpan sebagai hash, bukan plain text.
- Timestamp sebaiknya menggunakan timezone-aware timestamp pada implementasi.
- Status dapat diubah menjadi enum database jika sudah stabil.
- Untuk MVP, tags pada knowledge_items dapat disimpan sebagai TEXT sederhana.
- Pada tahap berikutnya, permissions dapat dibuat sebagai tabel terpisah jika role menjadi lebih kompleks.

---

# 18. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah API Requirement dan implementasi backend dimulai.
