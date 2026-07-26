# WF-005 Project Detail

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- WF-003 Setup Project
- WF-004 Project Setup Review
- ADR-001 Proposal to Project
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1
- Product Owner Decision Sprint 6A

## 1. Tujuan Halaman Project Detail

Project Detail adalah pusat operasional untuk satu pekerjaan riset setelah Proposal disetujui dan Project dibuat.

Halaman ini menjadi "home" untuk seluruh delivery work ResearchAI:

```text
Project
  -> Questionnaire
  -> Sample
  -> Fieldwork
  -> QC
  -> Dataset
  -> Dashboard
  -> Report
  -> Invoice
```

Tujuan utama:

- Menampilkan identitas Project secara jelas.
- Menampilkan hubungan Project dengan Client dan Proposal asal.
- Menampilkan status lifecycle Project.
- Menampilkan next business action berdasarkan status Project.
- Menjadi pintu masuk ke modul operasional berikutnya.
- Menjaga Project sebagai pusat delivery, bukan Proposal.

## 2. Workflow

```text
Proposal Approved
  |
  v
Setup Project
  |
  v
Review Setup Project
  |
  v
Confirm Buat Project
  |
  v
Project dibuat dengan status Setup
  |
  v
Project Detail
  |
  v
Next Business Action sesuai lifecycle Project
```

Lifecycle Project MVP:

```text
Setup -> Ready -> Fieldwork -> QC -> Analysis -> Reporting -> Completed
```

Status tambahan:

```text
Cancelled
```

## 3. Header Project

Header harus membuat user langsung paham Project apa yang sedang dibuka.

Informasi header:

- Project Number.
- Project Name.
- Status Project badge.
- Client Name.
- Research Type.
- Project Value.
- Project Manager jika tersedia.
- Quick link ke Proposal asal.

Contoh:

```text
PRJ-20260726-0001
Customer Satisfaction Survey 2026                         [Setup]

Client: PT Contoh Riset
Research Type: Customer Satisfaction
Project Value: Rp 25.000.000
Project Manager: Belum ditentukan
Proposal: PROP-20260726-0001
```

## 4. Informasi Project

Section Informasi Project menampilkan data utama pekerjaan operasional.

Field MVP:

- Project Number.
- Project Name.
- Research Type.
- Project Status.
- Project Value.
- Project Manager.
- Created Date.
- Updated Date.
- Start Date jika tersedia.
- End Date jika tersedia.

Catatan:

- Project Number dibuat otomatis backend.
- Project Name default dari Proposal Title, tetapi dapat diubah saat Setup Project.
- Project Manager optional pada MVP.
- Start Date dan End Date tidak wajib pada MVP.

## 5. Informasi Client

Project harus selalu menampilkan konteks Client.

Field:

- Nama Client.
- Industry.
- Kota.
- Status Client.
- PIC utama jika tersedia.
- Email PIC jika tersedia.
- Nomor HP PIC jika tersedia.

Behavior:

- Klik Client membuka Client Detail.
- Client tidak dapat diganti setelah Project dibuat.

## 6. Informasi Proposal Asal

Project yang dibuat dari Proposal harus menampilkan Proposal asal sebagai historical source.

Field:

- Proposal Number.
- Proposal Title.
- Proposal Owner.
- Proposal Status.
- Approved Date jika tersedia.
- Estimated Budget / Estimasi Nilai Proposal.

Behavior:

- Klik Proposal Number membuka Proposal Detail.
- Proposal tetap menjadi historical record.
- Proposal tidak berubah menjadi Project.

## 7. Status Project

Status Project mengikuti lifecycle ADR-003.

Status MVP:

| Status | Tujuan | Next Business Action |
| --- | --- | --- |
| Setup | Menyiapkan scope dan requirement operasional | Tandai Ready |
| Ready | Project siap dijalankan | Mulai Fieldwork |
| Fieldwork | Pelaksanaan pengumpulan data | Masuk QC |
| QC | Pemeriksaan kualitas data | Masuk Analysis |
| Analysis | Pengolahan dan analisis data | Masuk Reporting |
| Reporting | Penyusunan deliverable akhir | Tandai Completed |
| Completed | Project selesai | Tidak ada action lanjutan |
| Cancelled | Project dibatalkan | Tidak ada action lanjutan |

Business rule:

- Perubahan status Project dilakukan melalui Next Business Action.
- Tidak menggunakan dropdown status bebas.
- Activity Project dicatat otomatis dari backend.

## 8. Timeline Project

Timeline Project menampilkan alur status dari awal hingga selesai.

MVP timeline:

```text
[Setup] -> [Ready] -> [Fieldwork] -> [QC] -> [Analysis] -> [Reporting] -> [Completed]
```

Jika Project dibatalkan:

```text
[Setup/Ready/Fieldwork/QC/Analysis/Reporting] -> [Cancelled]
```

Informasi pada timeline:

- Status name.
- Tanggal masuk status jika tersedia.
- User yang menjalankan action jika tersedia.
- Status aktif saat ini.

Untuk MVP awal, timeline boleh berupa visual sederhana atau list status.

## 9. Next Business Action

Next Business Action adalah action utama yang muncul berdasarkan status Project saat ini.

Rules:

- Action tampil sebagai tombol jelas, bukan dropdown bebas.
- Hanya action yang valid untuk status saat ini yang tampil.
- Action mencatat Activity.
- Action tidak boleh melompati lifecycle kecuali rule bisnis menyetujui.

Action MVP:

| Current Status | Action |
| --- | --- |
| Setup | Tandai Ready |
| Ready | Mulai Fieldwork |
| Fieldwork | Masuk QC |
| QC | Masuk Analysis |
| Analysis | Masuk Reporting |
| Reporting | Tandai Completed |
| Completed | Tidak ada |
| Cancelled | Tidak ada |

Cancel Project:

- Dapat dipertimbangkan sebagai secondary action pada status sebelum `Completed`.
- Membutuhkan Product Owner Review sebelum implementasi.

## 10. Placeholder Modul Berikutnya

Project Detail harus menyiapkan pintu masuk ke modul operasional, tetapi tidak membuat modul lengkap sebelum waktunya.

Placeholder MVP:

- Questionnaire.
- Sample.
- Fieldwork.
- QC.
- Dataset.
- Dashboard.
- Report.

Setiap placeholder menampilkan:

- Nama modul.
- Status `Coming Soon` atau `Belum dimulai`.
- Ringkasan fungsi singkat.
- Relasi bahwa modul berada di bawah Project.

Contoh:

```text
Questionnaire
Belum dimulai
Instrumen riset untuk project ini akan dikelola di sini.
```

## 11. Layout

Layout desktop:

```text
Breadcrumb
Project / Project Detail

Header Project
+--------------------------------------------------------------------------+
| PRJ-20260726-0001                                      [Setup]           |
| Customer Satisfaction Survey 2026                                        |
| Client: PT Contoh Riset | Research Type: CSAT | Value: Rp 25.000.000     |
+--------------------------------------------------------------------------+

Main Content
+----------------------------------------------+---------------------------+
| Informasi Project                             | Next Business Action      |
| - Project Number                              | [Tandai Ready]            |
| - Project Name                                |                           |
| - Research Type                               | Informasi Sistem          |
| - Project Value                               | - Status: Setup           |
| - Project Manager                             | - Created Date            |
| - Start / End Date                            | - Updated Date            |
+----------------------------------------------+---------------------------+

+----------------------------------------------+---------------------------+
| Informasi Client                              | Proposal Asal             |
| - Nama Client                                 | - Proposal Number         |
| - Industry                                    | - Proposal Title          |
| - Kota                                        | - Proposal Owner          |
| - PIC / Email / HP                            | - Approved Date           |
+----------------------------------------------+---------------------------+

Timeline Project
[Setup] -> [Ready] -> [Fieldwork] -> [QC] -> [Analysis] -> [Reporting] -> [Completed]

Modul Operasional
+----------------+----------------+----------------+----------------+
| Questionnaire  | Sample         | Fieldwork      | QC             |
| Belum dimulai  | Belum dimulai  | Belum dimulai  | Belum dimulai  |
+----------------+----------------+----------------+----------------+
| Dataset        | Dashboard      | Report         | Invoice nanti  |
| Belum dimulai  | Coming Soon    | Coming Soon    | Phase berikut  |
+----------------+----------------+----------------+----------------+
```

## 12. Business Rules

1. Project wajib memiliki Client.
2. Project MVP wajib berasal dari Proposal Approved.
3. Project wajib menyimpan Proposal asal.
4. Project Number dibuat otomatis backend.
5. Project status awal adalah `Setup`.
6. Project Manager optional pada MVP.
7. Start Date dan End Date optional pada MVP.
8. Contract tidak menjadi syarat Project pada MVP.
9. Client tidak dapat diganti setelah Project dibuat.
10. Proposal asal tetap menjadi historical record.
11. Status Project berubah melalui Next Business Action.
12. Activity Project dicatat otomatis oleh backend service.
13. Modul operasional berada di bawah Project, bukan Proposal.

## 13. Loading State

Saat memuat Project:

```text
Memuat detail project...
```

UI:

- Header skeleton.
- Card skeleton untuk informasi utama.
- Action button tidak aktif.

## 14. Error State

### Project tidak ditemukan

```text
Project tidak ditemukan.
```

Action:

- Kembali ke Project List jika sudah ada.
- Kembali ke Proposal Detail jika datang dari Setup Project.

### Backend tidak dapat dihubungi

```text
Tidak dapat terhubung ke server.
```

Action:

- Coba lagi.

### User tidak memiliki akses

```text
Anda tidak memiliki akses ke project ini.
```

Action:

- Kembali ke Dashboard.

## 15. Empty State

Untuk placeholder modul:

```text
Belum ada data.
```

atau:

```text
Modul ini akan dikembangkan pada sprint berikutnya.
```

Empty state tidak boleh membuat user berpikir ada error.

## 16. Acceptance Criteria

1. Project Detail menampilkan Header Project.
2. Project Number menjadi identitas utama Project.
3. Project Name tampil jelas.
4. Status Project tampil sebagai badge.
5. Informasi Project tampil lengkap untuk MVP.
6. Informasi Client tampil dan dapat mengarah ke Client Detail.
7. Informasi Proposal Asal tampil dan dapat mengarah ke Proposal Detail.
8. Timeline Project tampil minimal sebagai visual sederhana.
9. Next Business Action tampil sesuai status Project.
10. Tidak ada dropdown status bebas.
11. Placeholder Questionnaire tampil.
12. Placeholder Sample tampil.
13. Placeholder Fieldwork tampil.
14. Placeholder QC tampil.
15. Placeholder Dataset tampil.
16. Placeholder Dashboard tampil.
17. Placeholder Report tampil.
18. Loading state tersedia.
19. Error state tersedia.
20. Empty state placeholder mudah dipahami.

## 17. Risiko

### Risiko 1: Project Detail menjadi terlalu besar terlalu cepat

Mitigasi:

- Hanya tampilkan informasi inti dan placeholder modul.
- Modul detail dibuat bertahap.

### Risiko 2: Next Business Action memaksa proses yang belum siap

Mitigasi:

- Sprint awal boleh menampilkan action sebagai desain, implementasi status action dilakukan setelah backend siap.

### Risiko 3: User bingung antara Proposal dan Project

Mitigasi:

- Proposal Asal ditampilkan jelas.
- Project Header menggunakan Project Number, bukan Proposal Number.
- Copy UI menjelaskan Project adalah pekerjaan operasional.

### Risiko 4: Placeholder terlihat seperti fitur rusak

Mitigasi:

- Gunakan label `Belum dimulai` atau `Coming Soon`.
- Berikan deskripsi singkat fungsi modul.

### Risiko 5: Data Client atau Proposal tidak lengkap

Mitigasi:

- Gunakan fallback `-`.
- Jangan menghalangi Project Detail terbuka jika data optional kosong.
