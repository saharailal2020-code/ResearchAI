# M2 Release Notes

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Milestone:
M2 - Proposal to Project Foundation

## 1. Ringkasan Milestone M2

Milestone M2 menandai perubahan penting ResearchAI dari platform perencanaan dan Proposal Management menjadi fondasi ERP/Operating System riset yang mulai memiliki alur operasional.

Pada M2, ResearchAI sudah mampu menjalankan alur inti:

```text
Client
  -> Proposal
  -> Proposal Approved
  -> Setup Project
  -> Project Detail
```

Project mulai menjadi pusat operasional sesuai Domain Model yang telah dibekukan.

## 2. Modul yang Selesai

### Client Management

Fitur yang tersedia:

- Client List.
- Client Detail / Client 360.
- Contact Management.
- Activity Timeline.
- Proposal relation pada Client.
- Bahasa Indonesia sebagai baseline UI Client Management.

### Proposal Management

Fitur yang tersedia:

- Proposal List.
- Proposal Detail read-only.
- Proposal Status Actions.
- Proposal Create.
- Proposal Number otomatis.
- Proposal Owner otomatis.
- Activity Logging.
- Integrasi dengan Client 360.

### Project Foundation

Fitur yang tersedia:

- Action Setup Project pada Proposal Approved.
- Review Setup Project.
- Create Project dari Proposal Approved.
- Project Number otomatis.
- Project status awal `Setup`.
- Redirect ke Project Detail.
- Project Detail MVP.
- Next Business Action `Tandai Ready`.
- Timeline Project.
- Summary Card.
- Information Card.
- Proposal Reference.
- Client Information.
- Placeholder modul operasional:
  - Questionnaire
  - Sample
  - Fieldwork
  - QC
  - Dataset
  - Dashboard
  - Report
- Activity Logging:
  - Project dibuat dari Proposal
  - Project ditandai Ready

## 3. Workflow yang Tersedia

### Client Workflow

```text
Client dibuat
  -> Contact dikelola
  -> Activity Timeline mencatat event bisnis
```

### Proposal Workflow

```text
Draft
  -> Dikirim ke Client
  -> Revisi
  -> Disetujui / Ditolak
```

### Proposal Create Workflow

```text
Proposal List
  -> Proposal Baru
  -> Simpan Draft
  -> Proposal Detail
```

### Setup Project Workflow

```text
Proposal Approved
  -> Setup Project
  -> Review Setup Project
  -> Buat Project
  -> Project Detail
```

### Project Workflow MVP

```text
Setup
  -> Ready
```

Lifecycle penuh yang sudah dibekukan:

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

## 4. Architecture Update

### Proposal vs Project

Keputusan arsitektur yang sudah diterapkan:

- Proposal adalah dokumen penawaran bisnis.
- Project adalah pekerjaan operasional.
- Proposal tetap menjadi historical record.
- Project dibuat dari Proposal `Approved`.
- Project dibuat melalui action eksplisit `Setup Project`.
- Project tidak dibuat otomatis.
- Untuk MVP, satu Proposal maksimal memiliki satu Project.

### Activity sebagai Cross-Cutting Behavior

Activity tidak menjadi sprint terpisah.

Setiap modul bisnis yang dibuat wajib mencatat event bisnis penting ke Client Activity Timeline.

Event yang sudah dicatat:

- Proposal dibuat.
- Proposal diperbarui.
- Proposal dikirim ke client.
- Proposal perlu revisi.
- Proposal disetujui.
- Proposal ditolak.
- Project dibuat dari Proposal.
- Project ditandai Ready.

### Project sebagai Operational Center

Project Detail menjadi fondasi untuk modul operasional berikutnya:

- Questionnaire.
- Sample.
- Fieldwork.
- QC.
- Dataset.
- Dashboard.
- Report.
- Invoice pada phase berikutnya.

## 5. Design System Update

Design System v1 sudah disetujui dan mulai diterapkan pada Project Foundation.

Komponen/pola yang sudah digunakan:

- Page Header.
- Summary Card.
- Information Card.
- Status Badge.
- Next Business Action.
- Timeline Component.
- Placeholder Card.
- Loading State.
- Error State.
- Currency Format.
- Date Format.
- Button Style.
- Validation Style.

Reusable component awal yang sudah tersedia:

- `StatusBadge`.
- `InfoCard`.
- `DetailItem`.
- `SummaryCard`.
- `PlaceholderCard`.
- `ErrorState`.

Utility awal:

- Format Rupiah.
- Format tanggal Indonesia.
- Mapping status Proposal dan Project.

## 6. Known Limitation

Keterbatasan saat ini:

- Project List lengkap belum tersedia.
- Project Detail masih MVP dan read-mostly.
- Project Status Actions baru mendukung `Setup -> Ready`.
- Lifecycle Project setelah `Ready` belum diimplementasikan.
- Questionnaire belum tersedia.
- Sample belum tersedia.
- Fieldwork belum tersedia.
- QC belum tersedia.
- Dataset belum tersedia.
- Dashboard belum tersedia.
- Report belum tersedia.
- Invoice belum tersedia.
- Permission granular belum tersedia.
- Notification belum tersedia.
- Document Management belum tersedia.
- Project Manager masih optional dan belum dipilih dari user list.
- Contract tidak menjadi syarat MVP.
- Database migration framework belum tersedia.

## 7. Technical Backlog

Backlog teknis prioritas:

- TECH-001 Database Migration Framework.
- Membuat Alembic migration.
- Schema versioning.
- Rollback strategy.
- Seed data strategy.
- Environment consistency.
- Membuat shared UI components lebih formal.
- Menambahkan backend automated tests.
- Menambahkan frontend component/browser test yang lebih stabil.
- Menstandarkan error response backend.
- Menstandarkan status enum backend dan frontend.

## 8. Product Backlog

Backlog produk prioritas:

- Project List.
- Project Status Actions lengkap.
- Project Activity Timeline.
- Project Team / Project Manager assignment.
- Questionnaire MVP.
- Sample MVP.
- Fieldwork MVP.
- QC MVP.
- Dataset MVP.
- Dashboard MVP.
- Report MVP.
- Document Management.
- Client Contact Integration pada Proposal.
- Proposal Edit.
- Setup Project dengan Project Manager optional dari user list.
- Contract Gate pada phase berikutnya.

## 9. Rekomendasi Sprint Berikutnya

Rekomendasi urutan sprint:

### Sprint 7

Project List dan Project Navigation.

Tujuan:

- Membuat entry point Project Management.
- Menampilkan daftar Project.
- Search/filter/sort Project.
- Link ke Project Detail.

### Sprint 8

Project Status Actions lanjutan.

Tujuan:

- Menambahkan workflow:

```text
Ready -> Fieldwork -> QC -> Analysis -> Reporting -> Completed
```

### Sprint 9

Questionnaire MVP.

Tujuan:

- Membuat instrumen riset pertama di bawah Project.

### Sprint 10

Sample MVP.

Tujuan:

- Menyusun target sample, quota, dan segment awal.

### Sprint Teknis Paralel

TECH-001 Database Migration Framework.

Tujuan:

- Menyiapkan fondasi database yang aman sebelum modul operasional semakin banyak.

## 10. Commit

Commit M2 utama:

```text
3d2aaf2 feat(project): implement project foundation mvp
```

Push ke branch `main` berhasil.

## 11. Release Summary

M2 berhasil membuktikan fondasi Product Build Phase:

```text
Client -> Proposal -> Project
```

ResearchAI kini mulai bergerak dari Proposal Management menuju ERP operasional perusahaan riset.
