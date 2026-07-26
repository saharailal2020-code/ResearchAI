# Questionnaire Impact Analysis

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Topik:
Perubahan Business Rule dari one Questionnaire per Project menjadi multiple Questionnaire per Project.

## 1. Ringkasan Perubahan

Business rule baru:

```text
Satu Project dapat memiliki lebih dari satu Questionnaire.
```

Contoh:

```text
Project STKU 2026
  |
  +-- Questionnaire Rumah Tangga
  +-- Questionnaire UMKM
  +-- Questionnaire Bank Pengelola Kas Titipan
  +-- Questionnaire Bank Peserta
```

Perubahan ini berdampak pada:

- Database model.
- API.
- Frontend.
- Workflow.
- Design System usage.
- Migration strategy.
- Testing.

## 2. Database Model Impact

### Kondisi Sprint 7 Saat Ini

Implementasi Sprint 7 saat ini masih mengarah ke one-to-one:

```text
Project 1 -> 0/1 Questionnaire
```

Indikasi teknis:

- `questionnaires.project_id` memiliki unique constraint.
- `Project.questionnaire` memakai relasi `uselist=False`.
- Project Detail response mengembalikan satu `questionnaire`.

### Perubahan yang Diperlukan

Relasi harus berubah menjadi:

```text
Project 1 -> many Questionnaire
```

Perubahan model:

- Hapus unique constraint pada `questionnaires.project_id`.
- Ubah relationship `Project.questionnaire` menjadi `Project.questionnaires`.
- Schema Project Detail mengembalikan list `questionnaires`.

### Field Baru yang Diperlukan

Field yang direkomendasikan:

| Field | Type | Wajib | Alasan |
| --- | --- | --- | --- |
| `respondent_group` | string | Ya | Membedakan target responden |
| `instrument_type` | string | Ya | Menjelaskan jenis instrumen |
| `sort_order` | integer | Tidak | Mengatur urutan tampil |
| `is_required` | boolean | Tidak | Gate readiness Fieldwork |

Rekomendasi MVP:

- `respondent_group` wajib.
- `instrument_type` default `Quantitative Survey`.
- `sort_order` default berdasarkan urutan create.
- `is_required` ditunda sampai gate Fieldwork dibuat.

### Candidate Model

```text
Questionnaire
  id
  project_id
  questionnaire_name
  respondent_group
  instrument_type
  version_number
  status
  kobo_link
  xlsform_link
  sort_order
  created_by
  ready_at
  created_at
  updated_at
```

## 3. API Impact

### Endpoint yang Perlu Berubah

Endpoint singular saat ini:

```text
GET /api/v1/projects/{project_id}/questionnaire
POST /api/v1/projects/{project_id}/questionnaire
```

Endpoint baru yang direkomendasikan:

```text
GET /api/v1/projects/{project_id}/questionnaires
POST /api/v1/projects/{project_id}/questionnaires
```

Endpoint detail tetap:

```text
GET /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}/status
```

### Backward Compatibility

Untuk menjaga kompatibilitas:

1. Pertahankan endpoint singular sementara.
2. Tandai sebagai deprecated.
3. Endpoint singular `GET` mengembalikan Questionnaire pertama.
4. Endpoint singular `POST` boleh tetap membuat Questionnaire pertama jika belum ada.
5. Frontend baru harus pindah ke endpoint plural.

### Response Project Detail

Sebelumnya:

```json
{
  "questionnaire": {}
}
```

Menjadi:

```json
{
  "questionnaires": []
}
```

Backward compatibility optional:

```json
{
  "questionnaire": {},
  "questionnaires": []
}
```

Rekomendasi:

- Untuk sementara bisa menyediakan keduanya.
- Frontend baru memakai `questionnaires`.

## 4. Frontend Impact

### Project Detail

Project Detail tidak lagi menampilkan satu card tunggal.

Rekomendasi UI:

Gunakan table/list compact di dalam section Questionnaire.

Alasan:

- Multiple Questionnaire perlu mudah dibandingkan.
- User perlu melihat status per instrument.
- Lebih efisien untuk project seperti STKU dengan banyak respondent group.

Kolom MVP:

- Questionnaire Name.
- Respondent Group.
- Instrument Type.
- Version.
- Status.
- Last Updated.
- Action.

Wireframe:

```text
Questionnaire

[+ Buat Questionnaire]

| Name                     | Respondent Group              | Version | Status | Last Updated | Action |
|--------------------------|-------------------------------|---------|--------|--------------|--------|
| Questionnaire Rumah Tangga| Rumah Tangga                 | 1       | Ready  | 26 Jul 2026  | Buka   |
| Questionnaire UMKM       | UMKM                          | 1       | Draft  | 26 Jul 2026  | Buka   |
```

### Create Questionnaire Kedua

Project Detail harus selalu menampilkan tombol:

```text
+ Buat Questionnaire
```

Selama Project status valid.

Create form perlu field tambahan:

- Questionnaire Name.
- Respondent Group.
- Instrument Type.
- KoBo Link.
- XLSForm Link.

### Questionnaire Detail

Questionnaire Detail perlu menampilkan:

- Respondent Group.
- Instrument Type.
- Project Reference.
- Status.
- Version.
- KoBo Link.
- XLSForm Link.
- Last Updated.

Tidak berubah:

- Edit Draft.
- Tandai Ready.
- Ready tidak diedit langsung.

## 5. Workflow Impact

WF-006 perlu direvisi.

Perubahan utama:

### Sebelumnya

```text
Project Detail
  -> Create Questionnaire
  -> Questionnaire Detail
```

### Menjadi

```text
Project Detail
  -> Questionnaire Section
  -> Create Questionnaire
  -> Questionnaire Detail
  -> kembali ke Questionnaire Section
```

Readiness:

```text
Project dapat lanjut ke Fieldwork jika semua Questionnaire wajib sudah Ready.
```

Namun gate Fieldwork belum diimplementasikan pada Sprint 7.

## 6. Design System Impact

Reusable component tetap dapat digunakan.

Komponen yang tetap relevan:

- Page Header.
- InfoCard.
- StatusBadge.
- DetailItem.
- EmptyState pattern.
- ErrorState.
- Button style.
- Form layout.
- Date format.

Tambahan kebutuhan:

- Compact table/list pattern untuk child objects di dalam Project Detail.

Rekomendasi:

- Jangan membuat style baru.
- Gunakan table style yang konsisten dengan Proposal List.
- Gunakan badge status yang sama.

## 7. Migration Strategy

### Karena Sprint 7 Belum Commit

Secara Git, perubahan masih bisa direvisi sebelum commit.

Namun database lokal mungkin sudah memiliki tabel `questionnaires` dengan unique constraint.

### Target Migration

Perlu mengubah:

- Drop unique constraint `uq_questionnaires_project_id`.
- Add columns:
  - `respondent_group`
  - `instrument_type`
  - `sort_order`

### Data Existing

Data existing satu questionnaire per project dapat dipertahankan.

Default value:

- `respondent_group`: gunakan `Main Respondent` atau derive dari questionnaire name.
- `instrument_type`: `Quantitative Survey`.
- `sort_order`: `1`.

### Tanpa Alembic

Karena TECH-001 belum diimplementasikan, ada dua opsi:

1. Recreate local table jika data dev tidak perlu dipertahankan.
2. Jalankan SQL manual development-only untuk alter table.

Rekomendasi:

- Jika data lokal hanya test, recreate table lebih sederhana.
- Untuk production/staging nanti wajib memakai Alembic.

### Dengan Alembic

Jika TECH-001 dikerjakan dulu:

- Buat migration drop unique constraint.
- Add nullable columns.
- Backfill default.
- Jadikan required pada aplikasi.

## 8. Testing Impact

Testing tambahan:

- Create Questionnaire pertama.
- Create Questionnaire kedua dalam Project yang sama.
- List Questionnaires by Project.
- Edit Questionnaire Draft.
- Mark Ready per Questionnaire.
- Project Detail menampilkan banyak Questionnaire.
- Activity logging per Questionnaire.
- Backward compatibility endpoint singular.
- Regression Project Detail.

## 9. Risiko

### Risiko 1: Scope Sprint 7 melebar

Multiple questionnaire menambah API list dan UI table.

Mitigasi:

- Batasi tetap metadata-only.
- Jangan menambah form builder.

### Risiko 2: Database local constraint menghambat testing

Unique constraint lama harus dihapus.

Mitigasi:

- Recreate local table atau migration dev.
- TECH-001 tetap prioritas.

### Risiko 3: UI Project Detail menjadi padat

Banyak Questionnaire dapat membuat Project Detail terlalu ramai.

Mitigasi:

- Gunakan compact table/list.
- Tampilkan hanya metadata utama.

### Risiko 4: Readiness logic belum matang

Project Fieldwork gate belum ada.

Mitigasi:

- Catat business rule.
- Implement gate saat Project Status Actions lanjutan dibuat.

## 10. Rekomendasi

Perubahan dapat dilakukan dalam Sprint 7 karena Sprint 7 belum commit, tetapi secara proses lebih sehat diperlakukan sebagai:

```text
Sprint 7 Revision / Sprint 7.1
```

Rekomendasi final:

- Jangan commit implementasi Sprint 7 saat ini.
- Revisi desain dan implementasi menjadi multiple questionnaire.
- Setelah testing selesai, lakukan Product Owner Review ulang.
- Commit baru hanya setelah PO menyetujui Sprint 7 revised.
