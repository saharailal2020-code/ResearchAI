# Sprint 8.1 Product Owner Review

Nama Sprint:
Sampling Plan Backend Foundation

Status Review:
Product Owner Acceptance Review

Tanggal:
26 Juli 2026

Basis Review:

- `Sprint8_Design_Freeze.md`
- `ADR-006_Revision.md`
- `Domain_Model_v3.md`
- `Workflow_v3.md`

Scope Implementasi yang Direview:

- Entity `SampleGroup`
- Entity `SamplingTarget`
- Relasi backend
- Migration script
- Repository layer
- Service layer
- Validation
- Unit test backend

Out of Scope yang harus tetap tidak disentuh:

- Frontend
- API endpoint
- Import Excel
- Export Excel
- Sample Database / Respondent Database
- Enumerator
- Fieldwork
- QC
- Dashboard

## 1. Compliance terhadap Design Freeze

### 1.1 Entity

Design Freeze menetapkan entity final:

- `SampleGroup`
- `SamplingTarget`

Implementasi:

- `SampleGroup` tersedia di `backend/app/models/sampling.py`.
- `SamplingTarget` tersedia di `backend/app/models/sampling.py`.

Status:

```text
COMPLIANT
```

### 1.2 Field SampleGroup

Design Freeze menetapkan field:

- `id`
- `project_id`
- `questionnaire_id`
- `sample_group_name`
- `target_respondent`
- `total_target_sample`
- `status`
- `notes`
- `sort_order`
- `created_by`
- `ready_at`
- `created_at`
- `updated_at`

Implementasi:

Seluruh field tersedia.

Status:

```text
COMPLIANT
```

### 1.3 Field SamplingTarget

Design Freeze menetapkan field:

- `id`
- `sample_group_id`
- `region_type`
- `region_name`
- `target_sample`
- `sort_order`
- `created_at`
- `updated_at`

Implementasi:

Seluruh field tersedia.

Status:

```text
COMPLIANT
```

### 1.4 Field Tambahan

Review menunjukkan tidak ada field tambahan yang keluar dari scope MVP.

Status:

```text
COMPLIANT
```

## 2. Compliance terhadap Business Rule

### 2.1 Sampling Plan bukan database responden

Implementasi tidak membuat entity:

- Respondent
- Respondent Database
- Sample Frame
- Enumerator

Status:

```text
COMPLIANT
```

### 2.2 Satu Project dapat memiliki banyak Sample Group

Relasi `Project.sample_groups` menggunakan list relationship.

Tidak ada unique constraint pada `project_id`.

Status:

```text
COMPLIANT
```

### 2.3 Satu Sample Group memiliki banyak Sampling Target

Relasi `SampleGroup.targets` menggunakan list relationship dengan cascade `all, delete-orphan`.

Status:

```text
COMPLIANT
```

### 2.4 Satu Questionnaire dapat digunakan banyak Sample Group

Tidak ada unique constraint pada `questionnaire_id`.

Unit test Pattern B membuktikan satu Questionnaire dapat dipakai oleh dua Sample Group.

Status:

```text
COMPLIANT
```

### 2.5 Questionnaire harus berasal dari Project yang sama

Service `validate_questionnaire_for_project` menolak Questionnaire dari Project lain.

Unit test tersedia untuk kasus ini.

Status:

```text
COMPLIANT
```

### 2.6 Status Flow Draft -> Ready

Service hanya mengizinkan:

```text
Draft -> Ready
```

Ready tidak dapat diedit.

Unit test tersedia.

Status:

```text
COMPLIANT
```

## 3. Compliance terhadap Domain Model

Final relationship pada Design Freeze:

```text
Project 1 -> many Questionnaire
Project 1 -> many SampleGroup
Questionnaire 1 -> many SampleGroup
SampleGroup 1 -> many SamplingTarget
```

Implementasi:

- `Project.sample_groups` tersedia.
- `Questionnaire.sample_groups` tersedia.
- `SampleGroup.targets` tersedia.
- `SamplingTarget.sample_group` tersedia.

Status:

```text
COMPLIANT
```

## 4. Review Service Layer

Service tersedia di:

```text
backend/app/services/sampling.py
```

Fungsi utama:

- `create_sample_group`
- `list_sample_groups_by_project`
- `update_sample_group`
- `update_sample_group_status`

Validasi yang tersedia:

- Project harus ada.
- Project Completed/Cancelled tidak boleh diubah Sampling Plan-nya.
- Questionnaire harus berada di Project yang sama.
- Sample Group Name wajib.
- Minimal satu Sampling Target wajib.
- Region Type wajib.
- Region Name wajib.
- Target Sample harus lebih besar dari 0.
- Total Target dihitung dari Sampling Target.
- Ready Sample Group tidak dapat diedit.
- Activity Logging dibuat untuk create/update/ready.

Status:

```text
COMPLIANT
```

Catatan:

Service belum memiliki fungsi delete explicit. Untuk Sprint 8.1, delete tidak tercantum sebagai fitur bisnis utama dalam Design Freeze, tetapi review Product Owner meminta unit test minimal mencakup delete. Hal ini menjadi temuan blocker pada sisi test coverage.

## 5. Review Repository Layer

Repository tersedia di:

```text
backend/app/repositories/sampling.py
```

Fungsi repository:

- Load Project.
- Load Questionnaire.
- Load Sample Group detail.
- List Sample Group by Project.
- Generate sort order.
- Build Sampling Target rows.

Status:

```text
COMPLIANT
```

Catatan:

Repository masih sederhana dan sesuai kebutuhan Sprint 8.1. Belum ada delete repository karena delete behavior belum difinalkan sebagai service action.

## 6. Review Migration Script

Migration script:

```text
backend/scripts/upgrade_sampling_plan.py
```

Behavior:

- Membuat table `sample_groups`.
- Membuat table `sampling_targets`.
- Menggunakan `Base.metadata.create_all` sesuai pola migration script sementara yang sudah digunakan di project.
- Idempotent untuk local development.

Status:

```text
COMPLIANT FOR CURRENT PROJECT PATTERN
```

Technical note:

Ini belum migration framework formal seperti Alembic. Risiko ini sudah menjadi technical debt existing.

## 7. Review Unit Test

Test file:

```text
backend/tests/test_sampling_service.py
```

Coverage saat ini:

| Area | Status |
| --- | --- |
| Create Sample Group | Covered |
| Update Sample Group | Covered melalui activity update |
| Status Draft -> Ready | Covered |
| Reject edit Ready | Covered |
| Validation Questionnaire same Project | Covered |
| Relationship Pattern A | Covered |
| Relationship Pattern B | Covered |
| Activity Logging | Covered |
| Delete / replacement behavior | Not explicitly covered |

Test result:

```text
Ran 5 tests
OK
```

Compile result:

```text
PASS
```

Finding:

Product Owner review meminta unit test minimal mencakup delete. Implementasi memiliki cascade `delete-orphan` dan update targets mengganti list target, tetapi belum ada test eksplisit untuk memastikan target lama terhapus saat targets diganti.

Status:

```text
PARTIALLY COMPLIANT
```

## 8. Pattern Support

### Pattern A

Banyak Questionnaire dan banyak Sample Group.

Test:

```text
test_pattern_a_allows_many_questionnaires_for_many_sample_groups
```

Status:

```text
SUPPORTED
```

### Pattern B

Satu Questionnaire digunakan oleh banyak Sample Group.

Test:

```text
test_pattern_b_allows_one_questionnaire_for_many_sample_groups
```

Status:

```text
SUPPORTED
```

## 9. Out of Scope Compliance

Implementasi tidak menambahkan:

- Frontend
- API endpoint
- Import Excel
- Export Excel
- Sample Database / Respondent Database
- Enumerator
- Fieldwork
- QC
- Dashboard

Status:

```text
COMPLIANT
```

## 10. Temuan

### Finding 1 - Delete behavior belum diuji eksplisit

Severity:
Medium

Description:

Product Owner Review meminta unit test minimal mencakup delete. Saat ini belum ada test eksplisit untuk delete/replacement Sampling Target.

Business impact:

- Target wilayah dapat diganti melalui update inline, tetapi belum ada safety net yang membuktikan target lama benar-benar terhapus.
- Ini penting karena UI MVP memiliki konsep `Hapus Wilayah`.

Recommendation:

Tambahkan unit test non-feature untuk memastikan saat `SampleGroupUpdate.targets` dikirim dengan target baru, target lama diganti dan tidak tersisa.

### Finding 2 - Tidak ada explicit delete service

Severity:
Low to Medium

Description:

Tidak ada service `delete_sample_group` atau `delete_sampling_target`.

Business impact:

- Tidak menghambat Sprint 8.1 Backend Foundation karena delete endpoint juga belum masuk API scope.
- Namun dapat menjadi kebutuhan Sprint 8.2/8.3 jika UI mendukung `Hapus Wilayah`.

Recommendation:

Untuk Sprint 8.1, cukup test replacement behavior.
Untuk sprint API/UI, Product Owner perlu memutuskan apakah delete target dilakukan via inline update atau endpoint terpisah.

## 11. Technical Debt

### TD-8.1-001 Migration masih script manual

Priority:
Medium

Description:

Migration menggunakan `create_all`, bukan Alembic.

Recommendation:

Masuk backlog Technical Foundation.

### TD-8.1-002 datetime.utcnow warning

Priority:
Low

Description:

Test memunculkan warning Python terkait `datetime.utcnow()`.

Recommendation:

Refactor global ke timezone-aware datetime pada technical cleanup terpisah, bukan Sprint 8.1.

### TD-8.1-003 Delete policy Sampling Target belum final

Priority:
Medium

Description:

Belum diputuskan apakah delete target wilayah dilakukan melalui inline replace atau endpoint khusus.

Recommendation:

Tetapkan sebelum Sprint API/Frontend.

## 12. Risiko

### Risiko 1 - Target wilayah lama tidak terhapus saat update

Severity:
Medium

Mitigation:

Tambahkan unit test replacement/delete target.

### Risiko 2 - Migration debt bertambah

Severity:
Medium

Mitigation:

Alembic baseline sebelum production-like usage.

### Risiko 3 - Delete UX belum punya backend contract final

Severity:
Medium

Mitigation:

Freeze delete behavior sebelum Sprint 8.2 API atau Sprint 8.3 Frontend.

## 13. Improvement Non-Blocker

1. Tambahkan test untuk `list_sample_groups_by_project`.
2. Tambahkan test Project Completed/Cancelled tidak bisa mengubah Sampling Plan.
3. Tambahkan test target_sample `0` atau negatif ditolak.
4. Tambahkan test Sample Group tanpa Questionnaire tetap boleh Draft.
5. Tambahkan test Ready validation jika targets kosong.
6. Tambahkan future service untuk delete jika Product Owner menginginkan delete eksplisit.
7. Tambahkan Alembic migration pada technical foundation.

## 14. Readiness untuk Sprint 8.2 API

Secara arsitektur backend foundation sudah siap menjadi dasar Sprint 8.2 API karena:

- Entity tersedia.
- Relationship tersedia.
- Service layer tersedia.
- Repository layer tersedia.
- Validation utama tersedia.
- Pattern A dan Pattern B teruji.

Namun sebelum Sprint 8.2, satu gap kecil perlu ditutup:

```text
Tambahkan test delete/replacement Sampling Target.
```

## 15. Rekomendasi

Rekomendasi Product Owner Review:

```text
CHANGES REQUIRED
```

Alasan:

Implementasi secara fungsi dan domain sudah sesuai, tetapi acceptance review meminta unit test minimal mencakup delete. Saat ini delete/replacement behavior belum diuji eksplisit.

Blocker yang harus diperbaiki:

1. Tambahkan unit test untuk memastikan update `targets` mengganti daftar Sampling Target lama.
2. Pastikan test membuktikan target lama tidak tersisa setelah update.
3. Jalankan ulang backend compile dan unit test.

Setelah blocker ini selesai, Sprint 8.1 dapat dinyatakan:

```text
APPROVED - READY TO COMMIT
```

## 16. Final Decision

```text
CHANGES REQUIRED
```
