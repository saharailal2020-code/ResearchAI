# Business Requirement Document

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan kebutuhan bisnis utama yang harus dipenuhi oleh ResearchAI.

Business Requirement Document (BRD) menjadi dasar untuk menyusun functional requirement, non-functional requirement, database design, API design, UI/UX flow, dan rencana pengembangan teknis.

---

# 2. Latar Belakang

Perusahaan riset menjalankan banyak proses yang saling berkaitan, mulai dari kebutuhan klien, proposal, project setup, research design, fieldwork, quality control, data processing, analysis, report generation, client delivery, hingga knowledge management.

Saat ini proses tersebut sering tersebar di banyak file, aplikasi, folder, dan komunikasi terpisah. Kondisi ini dapat menimbulkan duplikasi pekerjaan, kesulitan monitoring, risiko kesalahan data, dan waktu penyusunan laporan yang panjang.

ResearchAI dibangun sebagai platform terintegrasi untuk membantu perusahaan riset mengelola proses tersebut secara lebih cepat, konsisten, kolaboratif, dan didukung Artificial Intelligence.

---

# 3. Tujuan Bisnis

ResearchAI memiliki tujuan bisnis utama sebagai berikut:

1. Mengintegrasikan seluruh siklus proyek riset dalam satu platform.
2. Mengurangi pekerjaan manual dan repetitif.
3. Meningkatkan visibilitas progress proyek.
4. Meningkatkan konsistensi kualitas data, analisis, dan laporan.
5. Mempercepat penyusunan proposal, insight, executive summary, dan laporan.
6. Menjadikan data dan knowledge proyek sebagai aset perusahaan.
7. Meningkatkan kolaborasi antar tim internal.
8. Menyiapkan fondasi sistem yang dapat dikembangkan bertahap.

---

# 4. Ruang Lingkup MVP

MVP ResearchAI fokus pada modul berikut:

- Client Management
- Proposal Management
- Project Management
- Survey Management
- Quality Control
- Data Processing
- AI Analysis
- Report Generator
- User and Access Management
- Dashboard

Modul berikut belum menjadi prioritas MVP:

- Finance Management lengkap
- Client Portal lengkap
- Mobile Enumerator App
- Advanced Statistical Analysis
- Advanced Data Visualization
- Vendor Management
- Public API
- Multi-company Support

---

# 5. Pengguna Utama

Pengguna utama pada MVP:

- System Administrator
- Research Director
- Research Manager
- Project Manager
- Marketing / Business Development
- Data Processing
- Data Analyst / Research Analyst
- Quality Control

Pengguna yang dapat dikembangkan setelah MVP:

- Supervisor
- Enumerator
- Finance
- Client
- Research Partner / Vendor

---

# 6. Kebutuhan Bisnis Umum

## BR-001: Sistem harus menyimpan data dalam satu sumber utama

ResearchAI harus memastikan data klien, proposal, proyek, survei, dataset, analisis, dan laporan saling terhubung.

Tujuan:

- Mengurangi duplikasi data
- Menghindari perbedaan versi informasi
- Memudahkan pelacakan data antar proses

Prioritas:

High

---

## BR-002: Sistem harus mendukung alur proyek riset end-to-end

ResearchAI harus mendukung alur dari client request hingga knowledge base.

Tahapan utama:

1. Client Request
2. Proposal
3. Project Setup
4. Research Design
5. Fieldwork
6. Quality Control
7. Data Processing
8. Analysis
9. Report Generation
10. Client Delivery
11. Knowledge Base

Prioritas:

High

---

## BR-003: Sistem harus memiliki hak akses berbasis role

Setiap pengguna hanya boleh mengakses modul dan data sesuai role-nya.

Tujuan:

- Melindungi data klien dan responden
- Mengurangi risiko perubahan data yang tidak berwenang
- Mendukung workflow kerja antar role

Prioritas:

High

---

## BR-004: Sistem harus menggunakan AI sebagai asisten kerja

AI harus membantu pekerjaan riset, tetapi keputusan akhir tetap berada pada manusia.

Contoh bantuan AI:

- Draft proposal
- Ringkasan proyek
- Draft insight
- Draft executive summary
- Narasi laporan
- Rekomendasi awal

Prioritas:

High

---

## BR-005: Sistem harus menyimpan knowledge proyek

Setiap proyek harus dapat menghasilkan aset pengetahuan yang bisa digunakan kembali.

Contoh knowledge:

- Insight
- Rekomendasi
- Template proposal
- Template laporan
- Metodologi
- Catatan pembelajaran proyek

Prioritas:

Medium

---

# 7. Kebutuhan Bisnis Per Modul

## 7.1 Client Management

Tujuan:

Mengelola informasi klien sebagai dasar proposal dan proyek riset.

Kebutuhan bisnis:

- Sistem harus dapat menyimpan data klien.
- Sistem harus dapat menyimpan kontak utama klien.
- Sistem harus dapat menampilkan riwayat proposal dan proyek per klien.
- Sistem harus dapat menghubungkan klien dengan proposal dan proyek.
- Sistem harus membatasi akses data klien berdasarkan role.

Prioritas:

High

---

## 7.2 Proposal Management

Tujuan:

Mengelola proses penyusunan dan pelacakan proposal riset.

Kebutuhan bisnis:

- Sistem harus dapat membuat data proposal.
- Sistem harus dapat menghubungkan proposal dengan klien.
- Sistem harus dapat mencatat tujuan riset, metodologi awal, timeline, dan estimasi budget.
- Sistem harus dapat menyimpan status proposal.
- Sistem harus dapat menyimpan file proposal.
- Sistem harus dapat membantu membuat draft proposal menggunakan AI.
- Sistem harus dapat mengubah proposal menjadi proyek setelah disetujui.

Prioritas:

High

---

## 7.3 Project Management

Tujuan:

Mengelola proyek riset setelah proposal disetujui.

Kebutuhan bisnis:

- Sistem harus dapat membuat proyek dari proposal.
- Sistem harus dapat menentukan project manager dan tim proyek.
- Sistem harus dapat menyimpan timeline, milestone, dan status proyek.
- Sistem harus dapat mencatat progress proyek.
- Sistem harus dapat menampilkan daftar proyek aktif.
- Sistem harus dapat menampilkan detail proyek.
- Sistem harus dapat menutup proyek setelah selesai.

Prioritas:

High

---

## 7.4 Survey Management

Tujuan:

Mengelola kebutuhan survei dan fieldwork.

Kebutuhan bisnis:

- Sistem harus dapat menyimpan metode survei.
- Sistem harus dapat menyimpan target responden.
- Sistem harus dapat menyimpan jumlah sampel.
- Sistem harus dapat menyimpan area survei.
- Sistem harus dapat mencatat progress fieldwork.
- Sistem harus dapat mencatat kendala lapangan.
- Sistem harus dapat menampilkan status pencapaian sampel.

Prioritas:

Medium

---

## 7.5 Quality Control

Tujuan:

Memastikan kualitas data dan proses fieldwork.

Kebutuhan bisnis:

- Sistem harus dapat mencatat hasil pemeriksaan data.
- Sistem harus dapat menandai data valid dan data bermasalah.
- Sistem harus dapat menyimpan catatan QC.
- Sistem harus dapat menampilkan status kualitas data.
- Sistem harus dapat menghubungkan hasil QC dengan data processing.

Prioritas:

High

---

## 7.6 Data Processing

Tujuan:

Mengelola data hasil riset agar siap dianalisis.

Kebutuhan bisnis:

- Sistem harus dapat menyimpan dataset per proyek.
- Sistem harus dapat menerima upload file data.
- Sistem harus dapat mencatat status data processing.
- Sistem harus dapat menyimpan catatan data cleaning.
- Sistem harus dapat menandai dataset siap dianalisis.
- Sistem harus dapat menghubungkan dataset dengan modul AI Analysis dan Report Generator.

Prioritas:

High

---

## 7.7 AI Analysis

Tujuan:

Membantu tim riset menyusun ringkasan, insight, dan rekomendasi awal.

Kebutuhan bisnis:

- Sistem harus dapat membuat ringkasan proyek dengan bantuan AI.
- Sistem harus dapat membantu membuat draft insight.
- Sistem harus dapat membantu membuat draft rekomendasi.
- Sistem harus dapat membantu membuat executive summary.
- Sistem harus dapat menyimpan hasil AI sebagai draft.
- Sistem harus memungkinkan manusia mereview dan mengedit hasil AI.
- Sistem harus membedakan hasil AI draft dan hasil final yang sudah disetujui manusia.

Prioritas:

High

---

## 7.8 Report Generator

Tujuan:

Membantu penyusunan laporan riset secara lebih cepat dan konsisten.

Kebutuhan bisnis:

- Sistem harus dapat membuat draft struktur laporan.
- Sistem harus dapat membuat narasi laporan berdasarkan data dan insight.
- Sistem harus dapat membuat executive summary.
- Sistem harus dapat membuat rekomendasi awal.
- Sistem harus dapat menyimpan draft laporan.
- Sistem harus dapat mendukung revisi manual.
- Sistem harus dapat menyimpan status laporan.

Prioritas:

High

---

## 7.9 User and Access Management

Tujuan:

Mengatur pengguna, role, dan hak akses di ResearchAI.

Kebutuhan bisnis:

- Sistem harus dapat menyimpan data pengguna.
- Sistem harus dapat menetapkan role pengguna.
- Sistem harus dapat membatasi akses berdasarkan role.
- Sistem harus mendukung login dan logout.
- Sistem harus melindungi modul penting dari akses tidak sah.

Prioritas:

High

---

## 7.10 Dashboard

Tujuan:

Memberikan ringkasan kondisi proyek dan aktivitas utama.

Kebutuhan bisnis:

- Sistem harus menampilkan jumlah proyek aktif.
- Sistem harus menampilkan proposal berjalan.
- Sistem harus menampilkan status proyek.
- Sistem harus menampilkan progress fieldwork.
- Sistem harus menampilkan proyek yang membutuhkan perhatian.
- Dashboard harus menyesuaikan informasi berdasarkan role pengguna.

Prioritas:

Medium

---

# 8. Kebutuhan Non-Fungsional Awal

## 8.1 Security

Sistem harus melindungi data klien, data responden, dataset, dan laporan.

Kebutuhan:

- Role-based access control
- Login pengguna
- Pembatasan akses data
- Audit log untuk aktivitas penting pada tahap lanjutan

Prioritas:

High

---

## 8.2 Usability

Sistem harus mudah digunakan oleh tim riset yang memiliki latar belakang teknis berbeda.

Kebutuhan:

- Navigasi jelas
- Form input sederhana
- Dashboard mudah dipahami
- Istilah yang digunakan sesuai dunia riset

Prioritas:

High

---

## 8.3 Scalability

Sistem harus dapat dikembangkan bertahap tanpa mengubah fondasi utama secara besar-besaran.

Kebutuhan:

- Modul terpisah
- Data antar modul terhubung
- Struktur database dapat diperluas
- API dapat dikembangkan per modul

Prioritas:

Medium

---

## 8.4 Reliability

Sistem harus menjaga data penting agar tidak mudah hilang.

Kebutuhan:

- Penyimpanan data konsisten
- Backup data pada tahap deployment
- Validasi input penting

Prioritas:

High

---

## 8.5 AI Governance

Penggunaan AI harus dapat dikontrol dan direview manusia.

Kebutuhan:

- Output AI disimpan sebagai draft
- Output AI dapat diedit
- Keputusan final tetap oleh manusia
- Data sensitif harus dipertimbangkan sebelum dikirim ke layanan AI

Prioritas:

High

---

# 9. Business Rules Awal

1. Setiap proyek harus memiliki klien.
2. Setiap proyek sebaiknya berasal dari proposal yang disetujui.
3. Setiap proyek harus memiliki project manager.
4. Dataset hanya dapat masuk tahap analysis setelah dinyatakan siap dianalisis.
5. Hasil AI tidak boleh langsung dianggap final tanpa review manusia.
6. Laporan final hanya boleh diterbitkan setelah melewati proses review.
7. Pengguna hanya boleh mengakses data sesuai role dan penugasan proyek.
8. Knowledge proyek hanya dibuat dari proyek yang sudah selesai atau memiliki output yang valid.

---

# 10. Success Criteria MVP

MVP ResearchAI dianggap berhasil jika:

1. Klien dapat dicatat dalam sistem.
2. Proposal dapat dibuat dan dilacak statusnya.
3. Proposal yang disetujui dapat menjadi proyek.
4. Proyek dapat dikelola dengan timeline dan status.
5. Progress fieldwork dapat dicatat.
6. Dataset dapat disimpan dan ditandai siap dianalisis.
7. AI dapat membantu membuat ringkasan, insight, dan executive summary draft.
8. Draft laporan dapat dibuat dan direview.
9. Hak akses dasar berdasarkan role berjalan.
10. Dashboard dapat menampilkan ringkasan proyek utama.

---

# 11. Risiko Awal

## 11.1 Scope Terlalu Besar

ResearchAI memiliki potensi fitur yang sangat luas. Risiko utama adalah pengembangan terlalu melebar sebelum MVP selesai.

Mitigasi:

Fokus pada modul inti MVP dan tunda fitur lanjutan.

---

## 11.2 Ketergantungan Pada AI

AI dapat membantu mempercepat pekerjaan, tetapi hasilnya perlu divalidasi.

Mitigasi:

Semua output AI disimpan sebagai draft dan harus direview manusia.

---

## 11.3 Keamanan Data

ResearchAI akan menyimpan data sensitif.

Mitigasi:

Hak akses dan pembatasan data harus dirancang sejak awal.

---

## 11.4 Kompleksitas Workflow Riset

Setiap jenis riset dapat memiliki alur berbeda.

Mitigasi:

MVP menggunakan alur umum terlebih dahulu, lalu dikembangkan untuk jenis riset spesifik.

---

# 12. Dokumen Terkait

- Product Vision
- Product Principles
- Business Process
- User Roles
- MVP Feature List

---

# 13. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah functional requirement, database design, dan UI/UX flow dibuat.
