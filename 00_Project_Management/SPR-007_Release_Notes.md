# Sprint 7 Release Notes

Nama Release:
Questionnaire Foundation MVP

Milestone:
M3 - Research Preparation

Tanggal:
26 Juli 2026

## Ringkasan

Sprint 7 menambahkan fondasi modul Questionnaire pada ResearchAI.

Questionnaire sekarang menjadi object operasional di bawah Project dan dapat digunakan untuk mencatat metadata instrumen survey kuantitatif.

Release ini juga merevisi business rule penting:

```text
Satu Project dapat memiliki satu atau lebih Questionnaire.
```

## Modul yang Ditambahkan

### Questionnaire

Kemampuan utama:

- Membuat Questionnaire dari Project Detail.
- Menampilkan daftar Questionnaire pada Project Detail.
- Membuka Questionnaire Detail.
- Mengedit Questionnaire selama status masih Draft.
- Menandai Questionnaire sebagai Ready.
- Mendukung banyak Questionnaire dalam satu Project.

## Workflow yang Tersedia

```text
Project Detail
  -> Tambah Questionnaire
  -> Simpan Draft
  -> Questionnaire Detail
  -> Tandai Ready
```

Untuk Project dengan beberapa target respondent:

```text
Project
  -> Questionnaire Rumah Tangga
  -> Questionnaire UMKM
  -> Questionnaire Bank Peserta
```

## Architecture Update

- Relasi Project ke Questionnaire menjadi one-to-many.
- Endpoint plural menjadi endpoint utama.
- Endpoint singular lama tetap dipertahankan sementara untuk backward compatibility.
- Activity Questionnaire dicatat ke Client Activity Timeline.

## Database Update

Tabel Questionnaire mendukung field:

- Project ID.
- Questionnaire Name.
- Target Respondent.
- Instrument Type.
- Version Number.
- Status.
- KoBo Link.
- XLSForm Link.
- Sort Order.
- Created By.
- Ready At.
- Created At.
- Updated At.

Script upgrade:

```text
backend/scripts/upgrade_questionnaire_multiple.py
```

## Known Limitation

- Belum ada Form Builder.
- Belum ada KoBoToolbox API integration.
- Belum ada XLSForm upload dan parsing.
- Belum ada version history penuh.
- Belum ada permission khusus per role.
- Belum ada readiness gate Fieldwork berbasis semua Questionnaire Ready.

## Technical Backlog

- Implementasi Alembic migration framework.
- Validasi URL KoBo dan XLSForm.
- Penandaan formal endpoint deprecated di Swagger.
- Authorization berbasis role dan project access.
- Automated frontend test untuk Questionnaire workflow.

## Product Backlog

- Questionnaire Version History.
- XLSForm Upload.
- KoBoToolbox Sync.
- Questionnaire Template Library.
- Sample group integration.
- Fieldwork readiness checklist.

## Rekomendasi Sprint Berikutnya

Sprint berikutnya sebaiknya tidak langsung masuk ke Fieldwork.

Rekomendasi:

1. Review Project readiness rule.
2. Rancang Sample Foundation.
3. Tentukan hubungan Sample dengan Questionnaire dan Target Respondent.
4. Tentukan apakah semua Questionnaire wajib Ready sebelum Sample/Fieldwork.
