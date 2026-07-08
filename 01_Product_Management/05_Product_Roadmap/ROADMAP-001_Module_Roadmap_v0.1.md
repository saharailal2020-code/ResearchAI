# Module Roadmap

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan urutan pengembangan modul ResearchAI.

Module Roadmap digunakan untuk menentukan prioritas pembangunan, mengurangi risiko scope terlalu besar, dan memastikan setiap modul dibangun berdasarkan fondasi yang benar.

---

# 2. Prinsip Roadmap

Prinsip penyusunan roadmap:

1. Bangun fondasi sistem terlebih dahulu.
2. Mulai dari modul yang menjadi sumber data utama.
3. Hubungkan alur client -> proposal -> project sebelum masuk ke fitur lanjutan.
4. AI dan report generator dibangun setelah data proyek mulai tersedia.
5. Fitur lanjutan ditunda sampai MVP internal stabil.

---

# 3. Roadmap Ringkas

Urutan besar pengembangan ResearchAI:

1. Foundation
2. Core Business Flow
3. Project Execution
4. Data and Quality
5. AI and Report
6. Dashboard and Review
7. Post-MVP Expansion

---

# 4. Stage 0: Product and Technical Foundation

Tujuan:

Menyiapkan fondasi produk dan teknis sebelum coding modul utama.

Modul / pekerjaan:

- Product documentation
- Repository setup
- Technology stack decision
- Project structure
- Development environment
- Database planning
- UI/UX planning

Output:

- Product Vision
- Product Principles
- Business Process
- User Roles
- BRD
- FRD
- Database Entity List
- UI/UX User Flow
- Module Roadmap

Status:

In Progress

Prioritas:

High

---

# 5. Stage 1: System Foundation

Tujuan:

Membangun dasar aplikasi agar modul lain dapat berjalan.

Modul:

- User and Access Management
- Authentication
- Role Management
- Basic Layout
- Main Navigation
- Database Setup

Fitur utama:

- Login
- Logout
- Create user
- Assign role
- Sidebar navigation
- Protected pages
- Basic settings

Database utama:

- users
- roles
- user_roles

UI utama:

- Login Page
- Dashboard Shell
- User List
- User Detail
- Settings

Ketergantungan:

- Database Entity List
- User Roles
- UI/UX User Flow

Output:

- Pengguna dapat login
- Role dasar tersedia
- Akses menu dapat dibatasi
- Aplikasi memiliki layout utama

Prioritas:

High

Estimasi urutan:

Build first

---

# 6. Stage 2: Client and Proposal Flow

Tujuan:

Membangun alur awal dari klien sampai proposal.

Modul:

- Client Management
- Proposal Management

Fitur utama:

- Create client
- View client list
- View client detail
- Create proposal
- View proposal list
- View proposal detail
- Update proposal status
- Upload proposal file
- Draft proposal with AI pada tahap lanjutan

Database utama:

- clients
- client_contacts
- proposals
- proposal_files
- files

UI utama:

- Client List
- Client Detail
- Client Form
- Proposal List
- Proposal Detail
- Proposal Form

Ketergantungan:

- Stage 1 selesai

Output:

- Data klien dapat disimpan
- Proposal dapat dibuat dan dilacak
- Proposal dapat disetujui untuk menjadi proyek

Prioritas:

High

Estimasi urutan:

Build after foundation

---

# 7. Stage 3: Project Management Flow

Tujuan:

Membangun alur proyek setelah proposal disetujui.

Modul:

- Project Management
- Project Team
- Project Timeline

Fitur utama:

- Create project from approved proposal
- View project list
- View project detail
- Assign project manager
- Add project members
- Set project timeline
- Update project status
- Add project notes

Database utama:

- projects
- project_members
- project_milestones
- project_notes

UI utama:

- Project List
- Project Detail
- Project Team
- Project Timeline
- Project Status Panel

Ketergantungan:

- Stage 1 selesai
- Stage 2 selesai

Output:

- Proposal yang disetujui dapat menjadi proyek
- Project manager dapat mengelola tim dan status proyek
- Proyek menjadi pusat data untuk modul berikutnya

Prioritas:

High

Estimasi urutan:

Build after client and proposal

---

# 8. Stage 4: Survey, QC, and Data Processing

Tujuan:

Membangun alur pelaksanaan proyek, quality control, dan pengelolaan dataset.

Modul:

- Survey Management
- Quality Control
- Data Processing

Fitur utama:

- Setup survey plan
- Update fieldwork progress
- Record QC result
- Update QC status
- Upload dataset
- Update dataset status
- Add data processing notes

Database utama:

- survey_plans
- fieldwork_progress
- quality_checks
- quality_check_items
- datasets
- data_processing_notes
- files

UI utama:

- Survey Detail
- Fieldwork Progress Panel
- Quality Control Page
- Dataset List
- Dataset Detail

Ketergantungan:

- Stage 3 selesai

Output:

- Project dapat memiliki survey plan
- QC dapat mencatat kualitas data
- Dataset dapat diupload dan ditandai siap dianalisis

Prioritas:

High

Estimasi urutan:

Build after project management

---

# 9. Stage 5: AI Analysis and Report Generator

Tujuan:

Membangun fitur AI dan report generator setelah data proyek tersedia.

Modul:

- AI Analysis
- Report Generator

Fitur utama:

- Generate project summary
- Generate insight draft
- Generate executive summary
- Generate recommendation draft
- Create report structure
- Generate report narrative
- Review report
- Finalize report

Database utama:

- ai_outputs
- reports
- report_sections
- report_files
- files

UI utama:

- AI Analysis Page
- AI Draft Review Panel
- Report List
- Report Detail
- Report Editor
- Report Review Panel

Ketergantungan:

- Stage 3 selesai
- Stage 4 sebagian selesai
- AI governance rule tersedia

Output:

- AI dapat membantu analisis dan narasi
- Output AI tersimpan sebagai draft
- Report dapat dibuat, direview, dan difinalisasi

Prioritas:

High

Estimasi urutan:

Build after core data flow exists

---

# 10. Stage 6: Dashboard and Monitoring

Tujuan:

Menyediakan ringkasan status proyek dan pekerjaan berdasarkan role.

Modul:

- Dashboard
- Activity Monitoring

Fitur utama:

- Portfolio dashboard
- Project manager dashboard
- Data processing dashboard
- QC dashboard
- Project at risk
- Recent activity

Database utama:

- projects
- proposals
- datasets
- quality_checks
- reports
- activity_logs

UI utama:

- Research Director Dashboard
- Project Manager Dashboard
- Data Processing Dashboard
- QC Dashboard

Ketergantungan:

- Stage 2 selesai
- Stage 3 selesai
- Stage 4 sebagian selesai
- Stage 5 sebagian selesai

Output:

- Pengguna dapat melihat pekerjaan dan status utama
- Manajemen dapat memantau progress proyek

Prioritas:

Medium

Estimasi urutan:

Build incrementally

---

# 11. Stage 7: Knowledge Base

Tujuan:

Menyimpan hasil proyek sebagai aset pengetahuan perusahaan.

Modul:

- Knowledge Base

Fitur utama:

- Save project insight as knowledge
- Save recommendation
- Save methodology
- Save reusable template
- Search knowledge
- Filter by client, industry, research type, and category

Database utama:

- knowledge_items
- projects
- clients
- ai_outputs
- reports

UI utama:

- Knowledge List
- Knowledge Detail
- Knowledge Form

Ketergantungan:

- Stage 5 selesai sebagian
- Project dan report sudah tersedia

Output:

- Insight dan pembelajaran proyek tersimpan
- Knowledge dapat digunakan untuk proyek berikutnya

Prioritas:

Medium

Estimasi urutan:

Build after MVP core flow

---

# 12. Post-MVP Expansion

Fitur setelah MVP:

- Client Portal
- Finance Management
- Mobile Enumerator App
- Advanced Statistical Analysis
- Advanced Data Visualization
- Vendor Management
- Notification System
- Public API
- Multi-company Support
- Advanced Audit Log

Prioritas:

Later

Catatan:

Fitur ini tidak boleh mengganggu penyelesaian MVP internal.

---

# 13. MVP Development Order

Urutan pembangunan MVP yang disarankan:

1. User and Access Management
2. Basic Application Layout
3. Client Management
4. Proposal Management
5. Project Management
6. Survey Management
7. Quality Control
8. Data Processing
9. AI Analysis
10. Report Generator
11. Dashboard
12. Knowledge Base

---

# 14. MVP Release Target

MVP v0.1 harus mampu menjalankan alur:

Login -> Client -> Proposal -> Project -> Survey -> QC -> Data Processing -> AI Analysis -> Report -> Dashboard

Kriteria MVP:

- Pengguna dapat login.
- Klien dapat dibuat.
- Proposal dapat dibuat.
- Proposal approved dapat menjadi project.
- Project dapat memiliki tim dan status.
- Survey plan dapat dibuat.
- QC dapat dicatat.
- Dataset dapat diupload.
- AI dapat membuat draft summary, insight, dan executive summary.
- Report dapat dibuat sebagai draft.
- Dashboard dapat menampilkan ringkasan proyek.

---

# 15. Risiko Roadmap

## 15.1 Scope Creep

Risiko:

Pengembangan melebar ke terlalu banyak fitur sebelum alur utama selesai.

Mitigasi:

Fokus pada MVP Development Order.

---

## 15.2 AI Dibangun Terlalu Awal

Risiko:

AI sulit berguna jika data proyek belum tersedia.

Mitigasi:

Bangun AI setelah client, proposal, project, dan dataset tersedia.

---

## 15.3 Dashboard Dibangun Tanpa Data

Risiko:

Dashboard tidak bermakna jika modul data belum berjalan.

Mitigasi:

Bangun dashboard secara bertahap setelah modul utama memiliki data.

---

# 16. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah teknologi, database schema, dan UI wireframe diputuskan.
