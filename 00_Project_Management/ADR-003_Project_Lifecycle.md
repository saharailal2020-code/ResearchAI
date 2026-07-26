# ADR-003 Project Lifecycle

Status:
Proposed for Domain Architecture Freeze

Tanggal:
26 Juli 2026

## Tujuan

Mendefinisikan lifecycle Project MVP agar modul Project Management ResearchAI memiliki alur operasional yang konsisten dengan proses bisnis perusahaan riset.

Lifecycle ini menjadi acuan untuk Project List, Project Detail, Project Status Actions, Activity Logging, dan dependency ke modul lanjutan seperti Questionnaire, Sample, Fieldwork, QC, Dataset, Dashboard, Report, dan Invoice.

## Latar Belakang

Project adalah pusat delivery ResearchAI. Setelah Proposal disetujui dan Project dibuat melalui `Setup Project`, pekerjaan riset tidak langsung selesai. Project harus melewati beberapa tahap operasional.

Product Owner mengusulkan lifecycle sederhana:

```text
Setup -> Ready -> Fieldwork -> QC -> Analysis -> Reporting -> Completed
```

Lifecycle ini cukup merepresentasikan proses utama perusahaan riset tanpa langsung membuat semua submodule secara lengkap.

## Keputusan Arsitektur

Lifecycle Project MVP yang direkomendasikan:

```text
Setup
-> Ready
-> Fieldwork
-> QC
-> Analysis
-> Reporting
-> Completed
```

Status tambahan:

```text
Cancelled
```

`Cancelled` dapat terjadi dari status sebelum `Completed` jika project dibatalkan.

## Status Lifecycle

### 1. Setup

Tujuan:
Menyiapkan project setelah Proposal disetujui.

Aktivitas utama:

- Membuat Project dari Proposal Approved.
- Menetapkan Project Manager jika sudah tersedia.
- Review scope dari Proposal.
- Review research type, objective, methodology summary, timeline, dan budget estimasi.
- Menyiapkan rencana awal questionnaire, sample, dan resource.

Output:

- Project record dibuat.
- Project terhubung ke Client dan Proposal.
- Informasi awal project tersedia.
- Activity `Project dibuat dari Proposal` tercatat.

Status berikutnya:

- Ready
- Cancelled

### 2. Ready

Tujuan:
Menandai project siap dijalankan secara operasional.

Aktivitas utama:

- Finalisasi brief internal.
- Finalisasi timeline kerja.
- Menetapkan PIC delivery.
- Menyiapkan questionnaire draft atau requirement.
- Menyiapkan sample plan awal.
- Menentukan kebutuhan fieldwork dan QC.

Output:

- Project siap masuk pelaksanaan.
- Requirement operasional minimum tersedia.
- Activity `Project siap dijalankan` tercatat.

Status berikutnya:

- Fieldwork
- Cancelled

### 3. Fieldwork

Tujuan:
Menjalankan pengumpulan data atau pelaksanaan riset.

Aktivitas utama:

- Menjalankan survey, interview, FGD, observation, recruitment, atau metode riset lain.
- Mengelola fieldwork progress.
- Mengelola enumerator, supervisor, caller, moderator, atau vendor jika tersedia.
- Memantau progress sample.

Output:

- Data mentah terkumpul.
- Progress fieldwork tercatat.
- Issue lapangan tercatat jika ada.

Status berikutnya:

- QC
- Cancelled

### 4. QC

Tujuan:
Memastikan data yang terkumpul memenuhi standar kualitas.

Aktivitas utama:

- Validasi data.
- Backcheck jika diperlukan.
- Flagging data bermasalah.
- Review kualitas responden atau hasil interview.
- Approval data untuk diproses.

Output:

- Data lolos QC atau memiliki catatan perbaikan.
- QC result tersedia.
- Dataset siap diproses.

Status berikutnya:

- Analysis
- Fieldwork jika perlu pengumpulan ulang atau perbaikan data
- Cancelled

### 5. Analysis

Tujuan:
Mengolah data menjadi insight awal.

Aktivitas utama:

- Data cleaning.
- Data processing.
- Tabulasi.
- Analisis statistik atau thematic analysis.
- Membuat dataset siap dashboard/report.

Output:

- Dataset siap dianalisis.
- Insight awal tersedia.
- Tabel/chart awal tersedia.

Status berikutnya:

- Reporting
- QC jika ditemukan masalah kualitas data
- Cancelled

### 6. Reporting

Tujuan:
Menyusun deliverable akhir untuk client.

Aktivitas utama:

- Membuat dashboard.
- Menyusun report.
- Menulis insight dan rekomendasi.
- Review internal report.
- Finalisasi output client.

Output:

- Report final.
- Dashboard jika termasuk scope.
- Deliverable siap dikirim ke client.

Status berikutnya:

- Completed
- Analysis jika perlu analisis tambahan
- Cancelled

### 7. Completed

Tujuan:
Menandai project selesai secara operasional.

Aktivitas utama:

- Menutup deliverable.
- Menyimpan report final.
- Menyimpan dataset final.
- Mencatat lesson learned.
- Menyiapkan invoice jika modul Finance sudah tersedia.

Output:

- Project selesai.
- Report final tersedia.
- Dataset final tersedia.
- Activity `Project selesai` tercatat.

Status berikutnya:

- Tidak ada status lanjutan pada MVP.

### 8. Cancelled

Tujuan:
Menandai project dibatalkan.

Aktivitas utama:

- Mencatat bahwa project tidak dilanjutkan.
- Menyimpan alasan pembatalan jika phase berikutnya membutuhkan.
- Menutup aktivitas operasional yang belum selesai.

Output:

- Project tidak aktif.
- Activity `Project dibatalkan` tercatat.

Status berikutnya:

- Tidak ada status lanjutan pada MVP.

## Candidate Workflow

```text
Setup
  |
  v
Ready
  |
  v
Fieldwork
  |
  v
QC
  |
  v
Analysis
  |
  v
Reporting
  |
  v
Completed
```

Alternative path:

```text
QC -> Fieldwork
Analysis -> QC
Reporting -> Analysis
Any active status -> Cancelled
```

## Business Rules

1. Project baru dibuat dengan status `Setup`.
2. Project tidak boleh langsung berstatus `Completed`.
3. Project status harus diubah melalui Status Actions, bukan dropdown bebas.
4. Activity harus tercatat untuk setiap perubahan status penting.
5. Project `Completed` tidak memiliki action lanjutan pada MVP.
6. Project `Cancelled` tidak memiliki action lanjutan pada MVP.
7. Project yang berasal dari Proposal harus tetap menampilkan Proposal asal.
8. Client 360 harus dapat menampilkan Project beserta statusnya.

## Konsekuensi

### Positif

- Lifecycle mencerminkan proses riset nyata.
- Project dapat menjadi delivery center yang jelas.
- Modul berikutnya punya posisi natural dalam lifecycle.
- Activity Timeline dapat membaca progress project secara bisnis.

### Negatif

- Lifecycle ini lebih panjang dibanding opsi sederhana `Setup -> In Progress -> Completed`.
- UI harus dirancang agar status tidak terasa terlalu banyak.
- Beberapa status seperti Fieldwork, QC, Analysis, dan Reporting belum memiliki modul penuh pada MVP awal.

### Mitigasi

- Mulai dengan status lifecycle terlebih dahulu, lalu submodule dibangun bertahap.
- Gunakan placeholder yang jelas pada Project Detail.
- Jangan membangun semua submodule dalam satu sprint.

## Future Consideration

1. Menambahkan status `On Hold` jika Beerka sering menunda project sementara.
2. Menambahkan status `Client Review` sebelum Completed.
3. Menambahkan status `Invoice Ready` jika Finance ingin terhubung langsung.
4. Membuat lifecycle berbeda untuk quantitative dan qualitative research.
5. Menghubungkan setiap status ke required checklist.
6. Menghubungkan status Fieldwork ke monitoring real-time.
7. Menghubungkan status QC ke Data Quality Checker.

## Decision Owner

Product Owner, Product Architecture, dan Engineering.

## Status Review

Dokumen ini perlu disetujui sebagai bagian dari Sprint A0 Domain Architecture Freeze sebelum Sprint 5 dimulai.
