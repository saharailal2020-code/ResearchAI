# User Roles

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan jenis pengguna ResearchAI, tanggung jawab utama, dan akses awal setiap role.

User Roles menjadi dasar untuk merancang hak akses, dashboard, menu, workflow approval, database permission, dan fitur keamanan ResearchAI.

---

# 2. Prinsip Hak Akses

ResearchAI menggunakan prinsip role-based access control.

Setiap pengguna hanya boleh mengakses fitur dan data yang sesuai dengan tugasnya.

Prinsip utama:

1. Pengguna hanya melihat data yang relevan dengan pekerjaannya.
2. Data klien, data proyek, data responden, dan laporan harus dilindungi.
3. Akses admin tidak boleh diberikan kepada semua pengguna.
4. Setiap aktivitas penting sebaiknya dapat dilacak melalui audit log.
5. Klien hanya boleh melihat data dan laporan yang memang ditujukan untuk mereka.

---

# 3. Kategori Pengguna

Pengguna ResearchAI dibagi menjadi dua kategori utama:

## 3.1 Internal User

Pengguna dari dalam perusahaan riset.

Contoh:

- Management
- Project Manager
- Research Team
- Data Processing
- Quality Control
- Field Team
- Finance
- Administrator

## 3.2 External User

Pengguna dari luar perusahaan riset.

Contoh:

- Client
- Research Partner
- Vendor

Pada MVP, external user dapat dibatasi terlebih dahulu. Client Portal dapat dikembangkan setelah alur internal stabil.

---

# 4. Internal Roles

## 4.1 System Administrator

Deskripsi:

Pengguna yang bertanggung jawab mengelola konfigurasi sistem dan akses pengguna.

Tanggung jawab:

- Membuat dan mengelola akun pengguna
- Menentukan role pengguna
- Mengelola konfigurasi sistem
- Memantau keamanan sistem
- Mengelola master data dasar

Akses utama:

- User and Access Management
- Settings
- Audit Log
- Semua modul dengan akses administratif

Batasan:

- Tidak selalu menjadi pemilik keputusan bisnis proyek
- Perubahan penting tetap perlu mengikuti kebijakan perusahaan

---

## 4.2 Research Director

Deskripsi:

Pengguna level manajemen yang bertanggung jawab melihat performa riset secara keseluruhan dan mengambil keputusan strategis.

Tanggung jawab:

- Melihat seluruh portfolio proyek
- Memantau progress proyek strategis
- Meninjau laporan penting
- Memberikan arahan metodologi atau rekomendasi strategis
- Menyetujui output penting jika diperlukan

Akses utama:

- Dashboard
- Client Management
- Proposal Management
- Project Management
- AI Analysis
- Report Generator
- Knowledge Base

Batasan:

- Tidak perlu mengelola detail teknis harian setiap proyek

---

## 4.3 Research Manager

Deskripsi:

Pengguna yang mengelola beberapa proyek riset dan memastikan kualitas metodologi serta output riset.

Tanggung jawab:

- Meninjau proposal
- Meninjau research design
- Mengawasi beberapa project manager
- Melakukan review insight dan rekomendasi
- Memastikan standar kualitas riset terpenuhi

Akses utama:

- Proposal Management
- Project Management
- Survey Management
- Data Processing
- AI Analysis
- Report Generator
- Knowledge Base

Batasan:

- Tidak harus mengelola semua konfigurasi sistem

---

## 4.4 Project Manager

Deskripsi:

Pengguna yang bertanggung jawab menjalankan proyek riset dari awal hingga selesai.

Tanggung jawab:

- Membuat dan mengelola proyek
- Menentukan timeline proyek
- Mengatur tim proyek
- Memantau fieldwork
- Berkoordinasi dengan data processing dan analyst
- Mengelola komunikasi terkait progress proyek
- Menutup proyek setelah selesai

Akses utama:

- Project Management
- Survey Management
- Quality Control
- Data Processing
- AI Analysis
- Report Generator
- Dashboard

Batasan:

- Hanya mengelola proyek yang menjadi tanggung jawabnya, kecuali diberi akses lebih luas

---

## 4.5 Marketing / Business Development

Deskripsi:

Pengguna yang bertanggung jawab mengelola prospek klien, kebutuhan awal klien, dan proposal.

Tanggung jawab:

- Menambah data calon klien
- Mencatat kebutuhan klien
- Membuat peluang proyek
- Membantu penyusunan proposal
- Melacak status proposal
- Mencatat feedback klien pada tahap awal

Akses utama:

- Client Management
- Proposal Management
- Dashboard terbatas
- AI Assistant untuk draft proposal

Batasan:

- Tidak mengakses data mentah responden kecuali diperlukan
- Tidak mengubah hasil analisis final tanpa otorisasi

---

## 4.6 Data Processing

Deskripsi:

Pengguna yang bertanggung jawab mengelola data hasil riset agar siap dianalisis.

Tanggung jawab:

- Mengunggah dataset
- Membersihkan data
- Memvalidasi struktur data
- Menyiapkan tabulasi
- Menyiapkan dataset final
- Mencatat proses data cleaning

Akses utama:

- Data Processing
- Quality Control
- Project data terkait
- AI Analysis terbatas

Batasan:

- Tidak mengubah proposal atau informasi komersial proyek
- Tidak mengirim laporan final ke klien

---

## 4.7 Data Analyst / Research Analyst

Deskripsi:

Pengguna yang bertanggung jawab membaca data, menemukan insight, dan menyusun rekomendasi.

Tanggung jawab:

- Membaca dataset final
- Menyusun temuan utama
- Membuat insight
- Membuat rekomendasi awal
- Menggunakan AI untuk membantu analisis dan narasi
- Menyusun draft report content

Akses utama:

- Data Processing
- AI Analysis
- Report Generator
- Knowledge Base
- Project data terkait

Batasan:

- Hasil AI harus direview sebelum dijadikan output final
- Tidak mengelola konfigurasi sistem

---

## 4.8 Quality Control

Deskripsi:

Pengguna yang bertanggung jawab memeriksa kualitas data dan proses fieldwork.

Tanggung jawab:

- Memeriksa kelengkapan data
- Memeriksa konsistensi data
- Menandai data bermasalah
- Mencatat hasil QC
- Menyetujui data valid
- Memberikan catatan perbaikan kepada tim lapangan

Akses utama:

- Quality Control
- Survey Management
- Data Processing terbatas
- Dashboard fieldwork

Batasan:

- Tidak mengubah laporan final
- Tidak mengubah data klien atau proposal

---

## 4.9 Supervisor

Deskripsi:

Pengguna yang mengawasi pelaksanaan fieldwork di lapangan.

Tanggung jawab:

- Mengatur enumerator
- Memantau pencapaian sampel
- Mencatat kendala lapangan
- Melakukan pengecekan awal kualitas data
- Melaporkan progress fieldwork

Akses utama:

- Survey Management
- Fieldwork Dashboard
- Quality Control terbatas

Batasan:

- Hanya melihat proyek atau area yang ditugaskan
- Tidak mengakses laporan strategis klien

---

## 4.10 Enumerator

Deskripsi:

Pengguna yang melakukan pengumpulan data dari responden.

Tanggung jawab:

- Melakukan survei atau wawancara
- Mengisi data responden
- Mengirim hasil pengumpulan data
- Mencatat kendala lapangan jika ada

Akses utama:

- Form survei
- Tugas fieldwork
- Status tugas pribadi

Batasan:

- Tidak melihat seluruh data proyek
- Tidak mengakses data klien, laporan, atau analisis
- Hanya mengakses tugas yang diberikan

---

## 4.11 Finance

Deskripsi:

Pengguna yang bertanggung jawab pada aspek keuangan proyek.

Tanggung jawab:

- Melihat informasi budget proyek
- Mencatat pembayaran atau biaya terkait proyek
- Membantu monitoring profitabilitas proyek
- Menyimpan dokumen administrasi keuangan

Akses utama:

- Finance Management
- Project Management terbatas
- Client data terbatas

Batasan:

- Pada MVP, modul finance dapat ditunda atau dibuat sederhana
- Tidak mengakses data responden mentah kecuali diperlukan

---

# 5. External Roles

## 5.1 Client

Deskripsi:

Pengguna dari pihak klien yang menerima informasi proyek, laporan, atau hasil riset.

Tanggung jawab:

- Memberikan kebutuhan riset
- Memberikan feedback proposal
- Menyetujui dokumen tertentu jika diperlukan
- Menerima laporan dan presentasi hasil

Akses utama:

- Client Portal
- Report Delivery
- Project status terbatas

Batasan:

- Pada MVP, akses klien dapat dilakukan secara manual tanpa portal
- Klien hanya boleh melihat proyek miliknya
- Klien tidak boleh melihat data internal perusahaan riset

---

## 5.2 Research Partner / Vendor

Deskripsi:

Pihak eksternal yang membantu pelaksanaan sebagian pekerjaan riset.

Tanggung jawab:

- Melaksanakan pekerjaan sesuai scope
- Memberikan update progress
- Mengirim data atau dokumen yang dibutuhkan
- Menindaklanjuti catatan dari tim internal

Akses utama:

- Partner Portal
- Project task terbatas
- Fieldwork update terbatas

Batasan:

- Pada MVP, akses partner dapat ditunda
- Partner hanya boleh mengakses pekerjaan yang ditugaskan

---

# 6. Matriks Akses Awal

| Role | Client | Proposal | Project | Survey | QC | Data | AI | Report | User Admin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Administrator | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| Research Director | View | View | View | View | View | View | View | View | None |
| Research Manager | View | Edit | View/Edit | View | View | View | View/Edit | Review | None |
| Project Manager | View | View | Edit | Edit | View | View | View | Edit | None |
| Marketing | Edit | Edit | View | None | None | None | Draft | None | None |
| Data Processing | None | None | View | View | View | Edit | Limited | None | None |
| Data Analyst | None | None | View | View | View | View | Edit | Edit | None |
| Quality Control | None | None | View | View | Edit | Limited | None | None | None |
| Supervisor | None | None | Limited | Edit | Limited | None | None | None | None |
| Enumerator | None | None | None | Limited | None | None | None | None | None |
| Finance | Limited | Limited | Limited | None | None | None | None | None | None |
| Client | Limited | Limited | Limited | None | None | None | None | View | None |

Catatan:

Matriks ini masih draft dan akan disesuaikan setelah Business Requirement dibuat.

---

# 7. Prioritas Role Untuk MVP

Role yang perlu tersedia pada MVP:

- System Administrator
- Research Director
- Project Manager
- Marketing
- Data Processing
- Data Analyst
- Quality Control

Role yang dapat dibuat sederhana atau ditunda:

- Supervisor
- Enumerator
- Finance
- Client
- Research Partner / Vendor

---

# 8. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah Business Requirement dan UI/UX User Flow dibuat.
