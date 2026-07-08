# Business Process

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan proses bisnis utama yang akan didukung oleh ResearchAI.

Business Process menjadi dasar untuk menyusun User Roles, Business Requirement, Feature List, Database Design, UI/UX, Backend, AI, dan Report Generator.

---

# 2. Gambaran Umum Proses

ResearchAI dirancang untuk mengelola seluruh siklus proyek riset dari awal hingga akhir.

Alur utama:

Client Request -> Proposal -> Project Setup -> Research Design -> Fieldwork -> Quality Control -> Data Processing -> Analysis -> Report Generation -> Client Delivery -> Knowledge Base

---

# 3. Tahapan Proses Bisnis

## 3.1 Client Request

Tahap awal ketika calon klien atau klien existing menyampaikan kebutuhan riset.

Input:

- Nama klien
- Kontak klien
- Latar belakang kebutuhan
- Tujuan riset awal
- Jenis riset yang dibutuhkan
- Estimasi waktu
- Catatan diskusi awal

Output:

- Data klien
- Data peluang proyek
- Ringkasan kebutuhan awal

Modul terkait:

- Client Management
- Proposal Management

---

## 3.2 Proposal

Tahap penyusunan proposal berdasarkan kebutuhan klien.

Input:

- Data klien
- Kebutuhan riset
- Tujuan riset
- Metodologi awal
- Target responden
- Area riset
- Estimasi timeline
- Estimasi biaya

Aktivitas:

- Menyusun latar belakang proposal
- Menyusun tujuan riset
- Menentukan metodologi
- Menentukan ruang lingkup pekerjaan
- Menentukan timeline
- Menentukan budget
- Mengirim proposal ke klien
- Melacak status proposal

Output:

- Draft proposal
- Proposal final
- Status proposal

Modul terkait:

- Proposal Management
- AI Assistant
- Document Management

---

## 3.3 Project Setup

Tahap pembentukan proyek setelah proposal disetujui.

Input:

- Proposal yang disetujui
- Data klien
- Scope pekerjaan
- Timeline proyek
- Budget proyek

Aktivitas:

- Membuat data proyek
- Menentukan project manager
- Menentukan tim internal
- Menentukan milestone
- Menentukan timeline detail
- Menentukan dokumen kerja
- Menentukan status awal proyek

Output:

- Data proyek aktif
- Tim proyek
- Timeline proyek
- Milestone proyek

Modul terkait:

- Project Management
- User and Access Management
- Dashboard

---

## 3.4 Research Design

Tahap perancangan metodologi dan instrumen riset.

Input:

- Tujuan riset
- Scope proyek
- Jenis riset
- Target responden
- Metodologi yang disepakati

Aktivitas:

- Menyusun desain riset
- Menentukan metode pengumpulan data
- Menentukan jumlah sampel
- Menentukan kriteria responden
- Menyusun kuesioner atau panduan wawancara
- Melakukan review instrumen
- Menyetujui instrumen final

Output:

- Research design
- Sampling plan
- Kuesioner atau interview guide
- Instrumen final

Modul terkait:

- Survey Management
- AI Assistant
- Document Management

---

## 3.5 Fieldwork

Tahap pelaksanaan pengumpulan data.

Input:

- Instrumen final
- Target responden
- Area survei
- Tim lapangan
- Timeline fieldwork

Aktivitas:

- Menugaskan supervisor dan enumerator
- Memantau progress pengumpulan data
- Mencatat kendala lapangan
- Menerima data hasil survei
- Memantau pencapaian target sampel

Output:

- Data survei
- Progress fieldwork
- Catatan kendala lapangan
- Status pencapaian sampel

Modul terkait:

- Survey Management
- Dashboard
- Quality Control

---

## 3.6 Quality Control

Tahap pemeriksaan kualitas data dan proses fieldwork.

Input:

- Data survei
- Catatan lapangan
- Target sampel
- Kriteria validasi

Aktivitas:

- Memeriksa kelengkapan data
- Memeriksa konsistensi jawaban
- Menandai data bermasalah
- Melakukan validasi responden
- Melakukan revisi atau follow up jika diperlukan
- Menyetujui data yang valid

Output:

- Data valid
- Data bermasalah
- Catatan QC
- Status kualitas data

Modul terkait:

- Quality Control
- Data Processing
- Dashboard

---

## 3.7 Data Processing

Tahap pengolahan data agar siap dianalisis.

Input:

- Data valid
- Struktur kuesioner
- Kode variabel
- Catatan QC

Aktivitas:

- Membersihkan data
- Mengatur struktur data
- Membuat kode variabel
- Menyiapkan tabulasi
- Menyiapkan dataset analisis
- Menyimpan dataset final

Output:

- Dataset bersih
- Tabulasi awal
- Dataset siap analisis

Modul terkait:

- Data Processing
- Database
- AI Analysis

---

## 3.8 Analysis

Tahap membaca data dan menghasilkan insight.

Input:

- Dataset siap analisis
- Tujuan riset
- Pertanyaan riset
- Tabulasi
- Catatan proyek

Aktivitas:

- Membaca hasil data
- Membandingkan antar segmen
- Mencari pola dan temuan utama
- Menyusun insight
- Menyusun rekomendasi awal
- Menggunakan AI untuk membantu ringkasan dan narasi
- Melakukan review manusia terhadap hasil AI

Output:

- Temuan utama
- Insight
- Rekomendasi
- Executive summary draft

Modul terkait:

- AI Analysis
- Report Generator
- Knowledge Base

---

## 3.9 Report Generation

Tahap penyusunan laporan riset.

Input:

- Insight
- Rekomendasi
- Executive summary
- Dataset final
- Grafik dan tabel
- Template laporan

Aktivitas:

- Menyusun struktur laporan
- Membuat narasi laporan
- Membuat executive summary
- Membuat rekomendasi final
- Menyusun grafik dan tabel
- Melakukan review laporan
- Melakukan revisi laporan

Output:

- Draft laporan
- Laporan final
- Materi presentasi

Modul terkait:

- Report Generator
- AI Assistant
- Document Management

---

## 3.10 Client Delivery

Tahap penyampaian hasil riset kepada klien.

Input:

- Laporan final
- Materi presentasi
- Catatan rekomendasi

Aktivitas:

- Mengirim laporan kepada klien
- Melakukan presentasi hasil
- Mencatat feedback klien
- Menyimpan revisi jika ada
- Menutup proyek

Output:

- Laporan terkirim
- Feedback klien
- Status proyek selesai

Modul terkait:

- Project Management
- Client Management
- Report Generator

---

## 3.11 Knowledge Base

Tahap penyimpanan pembelajaran dari proyek sebagai aset perusahaan.

Input:

- Laporan final
- Insight
- Rekomendasi
- Metodologi
- Catatan proyek
- Feedback klien

Aktivitas:

- Menyimpan hasil proyek
- Menyimpan insight penting
- Menyimpan template yang dapat digunakan kembali
- Menyimpan pembelajaran proyek
- Menghubungkan knowledge dengan jenis riset dan industri klien

Output:

- Knowledge proyek
- Template reusable
- Benchmark internal
- Referensi proyek berikutnya

Modul terkait:

- Knowledge Base
- AI Assistant
- Client Management

---

# 4. Alur Status Proyek

Status proyek utama:

1. Lead
2. Proposal Draft
3. Proposal Sent
4. Proposal Approved
5. Project Active
6. Research Design
7. Fieldwork
8. Quality Control
9. Data Processing
10. Analysis
11. Report Draft
12. Report Final
13. Delivered
14. Closed

---

# 5. Modul Yang Terlibat

Modul utama dalam proses bisnis ResearchAI:

- Client Management
- Proposal Management
- Project Management
- Survey Management
- Quality Control
- Data Processing
- AI Analysis
- Report Generator
- Knowledge Base
- Dashboard
- User and Access Management

---

# 6. Catatan Untuk Pengembangan Berikutnya

Dokumen ini akan menjadi dasar untuk membuat:

- User Roles
- Business Requirement Document
- Functional Requirement
- Database Entity List
- UI/UX User Flow
- API Requirement
- AI Use Case

---

# 7. Status

Dokumen ini masih berstatus draft dan dapat diperbarui setelah alur kerja aktual perusahaan dirinci lebih detail.
