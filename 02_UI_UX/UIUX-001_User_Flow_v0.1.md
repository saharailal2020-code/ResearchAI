# UI/UX User Flow

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan alur pengguna utama ResearchAI pada tahap MVP.

UI/UX User Flow menjadi dasar untuk membuat wireframe, desain halaman, navigasi aplikasi, dan prioritas pengembangan frontend.

---

# 2. Prinsip UI/UX

Prinsip desain awal ResearchAI:

1. Workflow first: tampilan harus mengikuti alur kerja riset.
2. Simple and professional: tampilan harus jelas, tenang, dan mudah digunakan.
3. Role-based experience: menu dan dashboard menyesuaikan role pengguna.
4. Data connected: pengguna harus mudah berpindah dari client ke proposal, project, data, AI, dan report.
5. AI as assistant: fitur AI ditampilkan sebagai alat bantu, bukan pengambil keputusan final.
6. Review before final: output AI dan report harus mudah direview sebelum menjadi final.

---

# 3. Struktur Navigasi Utama

Navigasi utama MVP:

- Dashboard
- Clients
- Proposals
- Projects
- Surveys
- Quality Control
- Data Processing
- AI Analysis
- Reports
- Users
- Settings

Catatan:

Menu yang tampil dapat berbeda berdasarkan role pengguna.

---

# 4. Global User Flow

Alur umum pengguna:

Login -> Dashboard -> Select Module -> Work on Task -> Save/Review -> Update Status -> Return to Dashboard

Contoh alur end-to-end:

Login -> Dashboard -> Clients -> Create Client -> Create Proposal -> Approve Proposal -> Create Project -> Setup Survey -> QC -> Data Processing -> AI Analysis -> Report Generator -> Deliver Report -> Close Project

---

# 5. Authentication Flow

## 5.1 Login Flow

Alur:

1. Pengguna membuka ResearchAI.
2. Sistem menampilkan halaman login.
3. Pengguna memasukkan email dan password.
4. Sistem memvalidasi akun.
5. Jika berhasil, pengguna diarahkan ke dashboard.
6. Jika gagal, sistem menampilkan pesan error.

Halaman:

- Login Page
- Forgot Password Page pada tahap lanjutan
- Dashboard Page

Komponen utama:

- Email input
- Password input
- Login button
- Error message

Prioritas:

High

---

## 5.2 Logout Flow

Alur:

1. Pengguna membuka menu profil.
2. Pengguna memilih logout.
3. Sistem mengakhiri sesi pengguna.
4. Sistem mengarahkan pengguna kembali ke halaman login.

Prioritas:

High

---

# 6. Dashboard Flow

## 6.1 Research Director Dashboard

Tujuan:

Memberikan ringkasan portfolio proyek dan kondisi bisnis riset.

Informasi utama:

- Total proyek aktif
- Proposal berjalan
- Project status overview
- Project at risk
- Report waiting for review
- Recent activity

Alur:

1. Research Director login.
2. Sistem menampilkan dashboard portfolio.
3. Pengguna memilih proyek atau proposal yang ingin dilihat.
4. Sistem membuka detail sesuai pilihan.

Prioritas:

Medium

---

## 6.2 Project Manager Dashboard

Tujuan:

Memberikan ringkasan proyek yang sedang dikelola.

Informasi utama:

- My active projects
- Project timeline
- Fieldwork progress
- Dataset status
- Report status
- Open tasks

Alur:

1. Project Manager login.
2. Sistem menampilkan proyek yang ditugaskan.
3. Pengguna membuka project detail.
4. Pengguna memperbarui status, catatan, atau timeline.

Prioritas:

High

---

## 6.3 Data Processing Dashboard

Tujuan:

Menampilkan dataset yang perlu diproses.

Informasi utama:

- Dataset uploaded
- Dataset cleaning
- Dataset ready for analysis
- Data notes

Alur:

1. Data Processing login.
2. Sistem menampilkan daftar dataset.
3. Pengguna membuka dataset detail.
4. Pengguna memperbarui status data processing.

Prioritas:

Medium

---

## 6.4 Quality Control Dashboard

Tujuan:

Menampilkan pekerjaan QC yang perlu dilakukan.

Informasi utama:

- Data waiting for QC
- Valid data count
- Invalid data count
- QC notes

Alur:

1. Quality Control login.
2. Sistem menampilkan daftar data/proyek yang perlu diperiksa.
3. Pengguna membuka detail QC.
4. Pengguna mencatat hasil pemeriksaan.

Prioritas:

Medium

---

# 7. Client Management Flow

## 7.1 Create Client

Alur:

1. Pengguna membuka menu Clients.
2. Sistem menampilkan daftar klien.
3. Pengguna memilih Add Client.
4. Sistem menampilkan form client.
5. Pengguna mengisi data klien dan kontak utama.
6. Pengguna menyimpan data.
7. Sistem menampilkan client detail.

Halaman:

- Client List
- Client Form
- Client Detail

Data utama:

- Client name
- Industry
- Client type
- Contact name
- Contact email
- Contact phone
- Notes

Prioritas:

High

---

## 7.2 View Client Detail

Alur:

1. Pengguna membuka daftar klien.
2. Pengguna memilih satu klien.
3. Sistem menampilkan detail klien.
4. Sistem menampilkan riwayat proposal dan proyek klien.

Bagian halaman:

- Client profile
- Primary contact
- Proposal history
- Project history
- Notes

Prioritas:

High

---

# 8. Proposal Management Flow

## 8.1 Create Proposal

Alur:

1. Pengguna membuka menu Proposals.
2. Pengguna memilih Add Proposal.
3. Sistem menampilkan form proposal.
4. Pengguna memilih klien.
5. Pengguna mengisi tujuan riset, metodologi awal, timeline, dan estimasi budget.
6. Pengguna menyimpan proposal.
7. Sistem menampilkan proposal detail dengan status Proposal Draft.

Halaman:

- Proposal List
- Proposal Form
- Proposal Detail

Prioritas:

High

---

## 8.2 AI Draft Proposal

Alur:

1. Pengguna membuka proposal detail.
2. Pengguna memilih Generate Draft with AI.
3. Sistem meminta input tambahan jika diperlukan.
4. AI membuat draft proposal.
5. Sistem menampilkan hasil sebagai draft.
6. Pengguna mengedit dan menyimpan hasil.

Catatan:

Output AI tidak menjadi proposal final secara otomatis.

Prioritas:

Medium

---

## 8.3 Approve Proposal and Create Project

Alur:

1. Pengguna membuka proposal detail.
2. Pengguna mengubah status proposal menjadi Approved.
3. Sistem menampilkan opsi Create Project.
4. Pengguna membuat proyek dari proposal.
5. Sistem membawa data proposal ke project form.
6. Sistem membuat project baru.

Prioritas:

High

---

# 9. Project Management Flow

## 9.1 Project Detail Flow

Alur:

1. Pengguna membuka menu Projects.
2. Sistem menampilkan daftar proyek.
3. Pengguna memilih proyek.
4. Sistem menampilkan project detail.
5. Pengguna dapat melihat timeline, tim, status, survey, dataset, AI output, dan report.

Bagian halaman:

- Project summary
- Client information
- Timeline
- Team members
- Survey status
- QC status
- Dataset status
- AI output
- Report status
- Project notes

Prioritas:

High

---

## 9.2 Manage Project Team

Alur:

1. Pengguna membuka project detail.
2. Pengguna memilih Team.
3. Pengguna menambahkan anggota tim.
4. Pengguna menentukan role dalam proyek.
5. Sistem menyimpan anggota tim.

Prioritas:

High

---

## 9.3 Update Project Status

Alur:

1. Pengguna membuka project detail.
2. Pengguna memilih status proyek.
3. Pengguna mengubah status sesuai tahapan.
4. Sistem menyimpan status baru.
5. Dashboard menampilkan update terbaru.

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

# 10. Survey and Fieldwork Flow

## 10.1 Setup Survey

Alur:

1. Pengguna membuka project detail.
2. Pengguna memilih Survey.
3. Sistem menampilkan survey form.
4. Pengguna mengisi metode survei, target responden, jumlah sampel, area, dan timeline.
5. Sistem menyimpan survey plan.

Prioritas:

Medium

---

## 10.2 Update Fieldwork Progress

Alur:

1. Pengguna membuka survey detail.
2. Pengguna menambahkan progress fieldwork.
3. Pengguna mengisi jumlah data terkumpul dan catatan kendala.
4. Sistem menghitung progress terhadap target sampel.
5. Dashboard menampilkan progress terbaru.

Prioritas:

Medium

---

# 11. Quality Control Flow

## 11.1 Record QC Result

Alur:

1. Pengguna membuka menu Quality Control.
2. Sistem menampilkan daftar proyek atau dataset yang perlu QC.
3. Pengguna membuka detail QC.
4. Pengguna mencatat jumlah data valid dan tidak valid.
5. Pengguna menambahkan catatan QC.
6. Sistem menyimpan hasil QC.

Prioritas:

High

---

## 11.2 QC to Data Processing

Alur:

1. QC menyelesaikan pemeriksaan.
2. Sistem menyimpan status QC.
3. Data valid dapat diproses oleh Data Processing.
4. Data bermasalah diberi catatan perbaikan.

Prioritas:

High

---

# 12. Data Processing Flow

## 12.1 Upload Dataset

Alur:

1. Pengguna membuka project detail atau menu Data Processing.
2. Pengguna memilih Upload Dataset.
3. Pengguna mengunggah file dataset.
4. Sistem menyimpan metadata file.
5. Dataset memiliki status Uploaded.

Prioritas:

High

---

## 12.2 Update Dataset Status

Alur:

1. Pengguna membuka dataset detail.
2. Pengguna memperbarui status data.
3. Pengguna menambahkan catatan data cleaning.
4. Jika selesai, pengguna mengubah status menjadi Ready for Analysis.
5. Dataset dapat digunakan pada AI Analysis.

Status:

- Uploaded
- Cleaning
- Validated
- Ready for Analysis

Prioritas:

High

---

# 13. AI Analysis Flow

## 13.1 Generate Project Summary

Alur:

1. Pengguna membuka project detail.
2. Pengguna memilih AI Analysis.
3. Pengguna memilih Generate Project Summary.
4. AI membuat ringkasan proyek.
5. Sistem menyimpan hasil sebagai draft.
6. Pengguna mereview dan mengedit hasil.

Prioritas:

High

---

## 13.2 Generate Insight Draft

Alur:

1. Pengguna membuka AI Analysis.
2. Pengguna memilih dataset atau informasi proyek yang akan digunakan.
3. Pengguna memilih Generate Insight.
4. AI membuat draft insight.
5. Pengguna mereview, mengedit, dan menyimpan hasil final.

Prioritas:

High

---

## 13.3 Generate Executive Summary

Alur:

1. Pengguna membuka AI Analysis.
2. Pengguna memilih Generate Executive Summary.
3. AI membuat executive summary draft.
4. Pengguna mereview dan mengedit.
5. Hasil final dapat digunakan pada report.

Prioritas:

High

---

# 14. Report Generator Flow

## 14.1 Create Report Structure

Alur:

1. Pengguna membuka project detail.
2. Pengguna memilih Reports.
3. Pengguna memilih Create Report.
4. Sistem membuat draft struktur laporan.
5. Pengguna mengubah bagian laporan jika diperlukan.

Prioritas:

High

---

## 14.2 Generate Report Narrative

Alur:

1. Pengguna membuka report detail.
2. Pengguna memilih section laporan.
3. Pengguna memilih Generate Narrative.
4. AI membuat draft narasi.
5. Pengguna mengedit narasi.
6. Sistem menyimpan section laporan.

Prioritas:

High

---

## 14.3 Review and Finalize Report

Alur:

1. Pengguna menyelesaikan draft laporan.
2. Pengguna mengubah status menjadi Review.
3. Research Manager atau Research Director melakukan review.
4. Jika perlu revisi, status menjadi Revised.
5. Jika disetujui, status menjadi Final.
6. Setelah dikirim ke klien, status menjadi Delivered.

Prioritas:

High

---

# 15. User Management Flow

## 15.1 Create User

Alur:

1. System Administrator membuka menu Users.
2. Administrator memilih Add User.
3. Administrator mengisi nama, email, dan role.
4. Sistem membuat akun pengguna.
5. Pengguna baru dapat login sesuai role.

Prioritas:

High

---

## 15.2 Manage Role

Alur:

1. Administrator membuka detail user.
2. Administrator mengubah role pengguna.
3. Sistem menyimpan role baru.
4. Akses pengguna berubah sesuai role.

Prioritas:

High

---

# 16. MVP Screen List

Daftar layar utama MVP:

- Login Page
- Dashboard Page
- Client List Page
- Client Detail Page
- Client Form Page
- Proposal List Page
- Proposal Detail Page
- Proposal Form Page
- Project List Page
- Project Detail Page
- Survey Detail Page
- Quality Control Page
- Dataset List Page
- Dataset Detail Page
- AI Analysis Page
- Report List Page
- Report Detail Page
- User List Page
- User Detail Page
- Settings Page

---

# 17. Prioritas UI MVP

Prioritas pertama:

- Login
- Dashboard
- Client List and Detail
- Proposal List and Detail
- Project List and Detail
- User Management

Prioritas kedua:

- Survey
- Quality Control
- Data Processing
- AI Analysis
- Report Generator

Prioritas setelah MVP:

- Client Portal
- Mobile Fieldwork
- Finance Dashboard
- Advanced Analytics

---

# 18. Catatan Desain Visual Awal

ResearchAI sebaiknya menggunakan tampilan yang:

- Profesional
- Bersih
- Mudah dibaca
- Cocok untuk pekerjaan operasional
- Tidak terlalu dekoratif
- Fokus pada status, data, dan aksi pengguna

Komponen penting:

- Sidebar navigation
- Role-based dashboard cards
- Data tables
- Detail panels
- Status badges
- Forms
- Review panels
- AI draft editor
- Report editor

---

# 19. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah wireframe dan desain halaman dibuat.
