# Functional Requirement Document

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan kebutuhan fungsi utama yang harus dimiliki ResearchAI pada tahap MVP.

Functional Requirement Document (FRD) menjadi jembatan antara Business Requirement Document (BRD) dan pengembangan teknis seperti database, API, UI/UX, backend, frontend, dan AI.

---

# 2. Ruang Lingkup

FRD v0.1 fokus pada modul MVP berikut:

- User and Access Management
- Client Management
- Proposal Management
- Project Management
- Survey Management
- Quality Control
- Data Processing
- AI Analysis
- Report Generator
- Dashboard

Fitur lanjutan seperti mobile app, client portal lengkap, finance lengkap, public API, dan advanced analytics tidak termasuk dalam ruang lingkup FRD v0.1.

---

# 3. Format Kebutuhan Fungsi

Setiap kebutuhan fungsi menggunakan format:

- ID
- Nama fungsi
- Deskripsi
- Pengguna utama
- Prioritas
- Acceptance Criteria

Prioritas:

- High: penting untuk MVP
- Medium: penting tetapi dapat dibuat sederhana pada MVP
- Low: dapat ditunda

---

# 4. User and Access Management

## FR-UAM-001: Login Pengguna

Deskripsi:

Sistem harus menyediakan fungsi login agar pengguna dapat masuk ke ResearchAI.

Pengguna utama:

- Semua pengguna internal

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat memasukkan email dan password.
- Sistem menolak login jika data tidak valid.
- Sistem mengarahkan pengguna yang berhasil login ke dashboard.

---

## FR-UAM-002: Logout Pengguna

Deskripsi:

Sistem harus menyediakan fungsi logout agar pengguna dapat keluar dari ResearchAI.

Pengguna utama:

- Semua pengguna internal

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat logout dari sistem.
- Setelah logout, pengguna tidak dapat mengakses halaman internal tanpa login ulang.

---

## FR-UAM-003: Manajemen Data Pengguna

Deskripsi:

Sistem harus memungkinkan administrator membuat, melihat, mengubah, dan menonaktifkan pengguna.

Pengguna utama:

- System Administrator

Prioritas:

High

Acceptance Criteria:

- Administrator dapat menambah pengguna baru.
- Administrator dapat mengubah informasi pengguna.
- Administrator dapat menonaktifkan pengguna.
- Pengguna nonaktif tidak dapat login.

---

## FR-UAM-004: Role Pengguna

Deskripsi:

Sistem harus memungkinkan administrator menetapkan role untuk setiap pengguna.

Pengguna utama:

- System Administrator

Prioritas:

High

Acceptance Criteria:

- Setiap pengguna memiliki minimal satu role.
- Role menentukan menu dan data yang dapat diakses.
- Perubahan role memengaruhi akses pengguna setelah login berikutnya.

---

# 5. Client Management

## FR-CL-001: Membuat Data Klien

Deskripsi:

Sistem harus memungkinkan pengguna yang berwenang menambahkan data klien.

Pengguna utama:

- Marketing / Business Development
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat mengisi nama klien.
- Pengguna dapat mengisi industri atau kategori klien.
- Pengguna dapat menyimpan data klien.
- Sistem menampilkan klien baru pada daftar klien.

---

## FR-CL-002: Melihat Daftar Klien

Deskripsi:

Sistem harus menyediakan daftar klien yang dapat dicari dan dilihat oleh pengguna yang berwenang.

Pengguna utama:

- Marketing / Business Development
- Project Manager
- Research Manager
- Research Director

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat melihat daftar klien.
- Pengguna dapat mencari klien berdasarkan nama.
- Sistem hanya menampilkan data klien sesuai hak akses.

---

## FR-CL-003: Melihat Detail Klien

Deskripsi:

Sistem harus menampilkan informasi detail klien dan riwayat proposal atau proyek terkait.

Pengguna utama:

- Marketing / Business Development
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat melihat informasi utama klien.
- Pengguna dapat melihat kontak utama klien.
- Pengguna dapat melihat proposal dan proyek yang terkait dengan klien.

---

## FR-CL-004: Mengubah Data Klien

Deskripsi:

Sistem harus memungkinkan pengguna yang berwenang memperbarui data klien.

Pengguna utama:

- Marketing / Business Development
- System Administrator

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat mengubah informasi klien.
- Sistem menyimpan perubahan.
- Sistem menampilkan data terbaru setelah perubahan disimpan.

---

# 6. Proposal Management

## FR-PR-001: Membuat Proposal

Deskripsi:

Sistem harus memungkinkan pengguna membuat data proposal baru.

Pengguna utama:

- Marketing / Business Development
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Proposal harus terhubung dengan klien.
- Pengguna dapat mengisi judul proposal.
- Pengguna dapat mengisi tujuan riset.
- Pengguna dapat mengisi metodologi awal.
- Proposal baru memiliki status awal Proposal Draft.

---

## FR-PR-002: Melihat Daftar Proposal

Deskripsi:

Sistem harus menyediakan daftar proposal dan statusnya.

Pengguna utama:

- Marketing / Business Development
- Project Manager
- Research Manager
- Research Director

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat melihat daftar proposal.
- Pengguna dapat melihat status proposal.
- Pengguna dapat memfilter proposal berdasarkan status.

---

## FR-PR-003: Mengubah Status Proposal

Deskripsi:

Sistem harus memungkinkan pengguna yang berwenang mengubah status proposal.

Pengguna utama:

- Marketing / Business Development
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Status proposal dapat diubah menjadi Draft, Sent, Approved, Rejected, atau Revised.
- Proposal yang disetujui dapat diproses menjadi proyek.
- Sistem menyimpan status terbaru.

---

## FR-PR-004: Upload File Proposal

Deskripsi:

Sistem harus memungkinkan pengguna menyimpan file proposal.

Pengguna utama:

- Marketing / Business Development
- Project Manager

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat mengunggah file proposal.
- File proposal terhubung dengan data proposal.
- Pengguna yang berwenang dapat melihat file proposal.

---

## FR-PR-005: Draft Proposal Dengan AI

Deskripsi:

Sistem harus menyediakan bantuan AI untuk membuat draft proposal awal.

Pengguna utama:

- Marketing / Business Development
- Research Manager

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat meminta AI membuat draft proposal.
- AI menggunakan input seperti tujuan riset, jenis riset, dan metodologi awal.
- Output AI tersimpan sebagai draft yang dapat diedit.

---

# 7. Project Management

## FR-PJ-001: Membuat Project Dari Proposal

Deskripsi:

Sistem harus memungkinkan proposal yang disetujui diubah menjadi proyek.

Pengguna utama:

- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Hanya proposal dengan status Approved yang dapat menjadi proyek.
- Data utama proposal dibawa ke proyek.
- Proyek baru memiliki status Project Active.

---

## FR-PJ-002: Menentukan Tim Proyek

Deskripsi:

Sistem harus memungkinkan project manager menentukan anggota tim proyek.

Pengguna utama:

- Project Manager

Prioritas:

High

Acceptance Criteria:

- Project manager dapat menambahkan anggota tim.
- Setiap anggota tim memiliki role dalam proyek.
- Anggota tim dapat melihat proyek yang ditugaskan.

---

## FR-PJ-003: Mengelola Timeline Proyek

Deskripsi:

Sistem harus memungkinkan pengguna menyimpan timeline dan milestone proyek.

Pengguna utama:

- Project Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat mengisi tanggal mulai dan selesai proyek.
- Pengguna dapat menambahkan milestone.
- Sistem menampilkan timeline proyek pada detail proyek.

---

## FR-PJ-004: Mengubah Status Proyek

Deskripsi:

Sistem harus memungkinkan pengguna mengubah status proyek sesuai tahapan kerja.

Pengguna utama:

- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Status proyek mengikuti alur yang ditentukan pada Business Process.
- Sistem menyimpan perubahan status.
- Dashboard menampilkan status terbaru.

---

## FR-PJ-005: Catatan Progress Proyek

Deskripsi:

Sistem harus menyediakan fitur catatan progress proyek.

Pengguna utama:

- Project Manager
- Research Manager

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat menambahkan catatan progress.
- Catatan tersimpan dengan tanggal dan pembuat catatan.
- Catatan dapat dilihat pada detail proyek.

---

# 8. Survey Management

## FR-SV-001: Menyimpan Informasi Survei

Deskripsi:

Sistem harus menyimpan informasi survei untuk setiap proyek.

Pengguna utama:

- Project Manager
- Research Manager

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat mengisi metode survei.
- Pengguna dapat mengisi target responden.
- Pengguna dapat mengisi jumlah sampel.
- Informasi survei terhubung dengan proyek.

---

## FR-SV-002: Monitoring Fieldwork

Deskripsi:

Sistem harus memungkinkan pengguna mencatat progress fieldwork.

Pengguna utama:

- Project Manager
- Supervisor
- Quality Control

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat mencatat jumlah data terkumpul.
- Pengguna dapat mencatat kendala lapangan.
- Sistem menampilkan progress terhadap target sampel.

---

# 9. Quality Control

## FR-QC-001: Mencatat Hasil QC

Deskripsi:

Sistem harus memungkinkan pengguna mencatat hasil quality control.

Pengguna utama:

- Quality Control
- Project Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat mencatat data valid.
- Pengguna dapat mencatat data bermasalah.
- Pengguna dapat menambahkan catatan QC.
- Hasil QC terhubung dengan proyek atau dataset.

---

## FR-QC-002: Status Kualitas Data

Deskripsi:

Sistem harus menampilkan status kualitas data.

Pengguna utama:

- Quality Control
- Data Processing
- Project Manager

Prioritas:

High

Acceptance Criteria:

- Sistem menampilkan status QC.
- Data yang belum lolos QC tidak langsung dianggap siap diproses.
- Status QC dapat digunakan oleh Data Processing.

---

# 10. Data Processing

## FR-DP-001: Upload Dataset

Deskripsi:

Sistem harus memungkinkan pengguna mengunggah dataset proyek.

Pengguna utama:

- Data Processing
- Project Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat mengunggah file dataset.
- Dataset terhubung dengan proyek.
- Sistem menyimpan metadata dataset seperti nama file, tanggal upload, dan pengunggah.

---

## FR-DP-002: Status Data Processing

Deskripsi:

Sistem harus memungkinkan pengguna mengatur status pengolahan data.

Pengguna utama:

- Data Processing

Prioritas:

High

Acceptance Criteria:

- Status dataset dapat berupa Uploaded, Cleaning, Validated, atau Ready for Analysis.
- Hanya dataset Ready for Analysis yang digunakan untuk analysis final.
- Sistem menampilkan status terbaru.

---

## FR-DP-003: Catatan Data Cleaning

Deskripsi:

Sistem harus menyediakan catatan proses data cleaning.

Pengguna utama:

- Data Processing

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat menambahkan catatan cleaning.
- Catatan tersimpan dengan tanggal dan pembuat catatan.
- Catatan dapat dilihat oleh pengguna yang berwenang.

---

# 11. AI Analysis

## FR-AI-001: Ringkasan Proyek Dengan AI

Deskripsi:

Sistem harus menyediakan bantuan AI untuk membuat ringkasan proyek.

Pengguna utama:

- Data Analyst
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat meminta AI membuat ringkasan proyek.
- Output AI tersimpan sebagai draft.
- Output AI dapat diedit oleh pengguna.

---

## FR-AI-002: Draft Insight Dengan AI

Deskripsi:

Sistem harus membantu pengguna membuat draft insight awal.

Pengguna utama:

- Data Analyst
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat meminta AI menyusun insight awal.
- Output AI harus diberi label draft.
- Pengguna dapat mengedit dan menyetujui hasil akhir.

---

## FR-AI-003: Draft Executive Summary Dengan AI

Deskripsi:

Sistem harus membantu membuat executive summary awal.

Pengguna utama:

- Data Analyst
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat meminta AI membuat executive summary.
- Output AI dapat diedit.
- Output final harus disimpan terpisah dari draft AI.

---

## FR-AI-004: Draft Rekomendasi Dengan AI

Deskripsi:

Sistem harus membantu membuat rekomendasi awal berdasarkan insight.

Pengguna utama:

- Data Analyst
- Research Manager

Prioritas:

Medium

Acceptance Criteria:

- Pengguna dapat meminta AI membuat rekomendasi.
- Output AI tersimpan sebagai draft.
- Pengguna dapat mengedit rekomendasi sebelum masuk laporan.

---

# 12. Report Generator

## FR-RG-001: Membuat Draft Struktur Laporan

Deskripsi:

Sistem harus membantu membuat struktur laporan riset.

Pengguna utama:

- Data Analyst
- Project Manager
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat membuat draft struktur laporan.
- Struktur laporan terhubung dengan proyek.
- Struktur laporan dapat diedit.

---

## FR-RG-002: Membuat Narasi Laporan

Deskripsi:

Sistem harus membantu membuat narasi laporan berdasarkan insight dan hasil analisis.

Pengguna utama:

- Data Analyst
- Research Manager

Prioritas:

High

Acceptance Criteria:

- Pengguna dapat membuat draft narasi.
- Draft narasi dapat diedit manual.
- Narasi tersimpan sebagai bagian dari laporan proyek.

---

## FR-RG-003: Status Laporan

Deskripsi:

Sistem harus menyimpan status laporan.

Pengguna utama:

- Project Manager
- Research Manager

Prioritas:

Medium

Acceptance Criteria:

- Status laporan dapat berupa Draft, Review, Revised, Final, atau Delivered.
- Status laporan tampil pada detail proyek.
- Laporan final tidak boleh berubah tanpa proses revisi.

---

# 13. Dashboard

## FR-DB-001: Dashboard Ringkasan Proyek

Deskripsi:

Sistem harus menampilkan ringkasan proyek utama.

Pengguna utama:

- Research Director
- Research Manager
- Project Manager

Prioritas:

Medium

Acceptance Criteria:

- Dashboard menampilkan jumlah proyek aktif.
- Dashboard menampilkan status proyek.
- Dashboard menampilkan proposal berjalan.
- Dashboard menampilkan proyek yang membutuhkan perhatian.

---

## FR-DB-002: Dashboard Berdasarkan Role

Deskripsi:

Sistem harus menampilkan informasi dashboard sesuai role pengguna.

Pengguna utama:

- Semua pengguna internal

Prioritas:

Medium

Acceptance Criteria:

- Research Director melihat ringkasan portfolio.
- Project Manager melihat proyek yang dikelola.
- Data Processing melihat dataset yang perlu diproses.
- Quality Control melihat data yang perlu diperiksa.

---

# 14. Prioritas MVP

Fungsi yang wajib ada untuk MVP awal:

- FR-UAM-001: Login Pengguna
- FR-UAM-002: Logout Pengguna
- FR-UAM-003: Manajemen Data Pengguna
- FR-UAM-004: Role Pengguna
- FR-CL-001: Membuat Data Klien
- FR-CL-002: Melihat Daftar Klien
- FR-CL-003: Melihat Detail Klien
- FR-PR-001: Membuat Proposal
- FR-PR-002: Melihat Daftar Proposal
- FR-PR-003: Mengubah Status Proposal
- FR-PJ-001: Membuat Project Dari Proposal
- FR-PJ-002: Menentukan Tim Proyek
- FR-PJ-003: Mengelola Timeline Proyek
- FR-PJ-004: Mengubah Status Proyek
- FR-QC-001: Mencatat Hasil QC
- FR-DP-001: Upload Dataset
- FR-DP-002: Status Data Processing
- FR-AI-001: Ringkasan Proyek Dengan AI
- FR-AI-002: Draft Insight Dengan AI
- FR-AI-003: Draft Executive Summary Dengan AI
- FR-RG-001: Membuat Draft Struktur Laporan
- FR-RG-002: Membuat Narasi Laporan

---

# 15. Dokumen Terkait

- Product Vision
- Product Principles
- Business Process
- Business Requirement Document
- User Roles
- MVP Feature List

---

# 16. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah database entity list, UI/UX user flow, dan API requirement dibuat.
