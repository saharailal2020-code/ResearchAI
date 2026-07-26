# Sprint 8 Proposal

Nama Sprint:
Sample Management Discovery

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. Tujuan Sprint

Sprint 8 bertujuan melakukan discovery dan design review untuk modul Sample Management.

Sample Management adalah modul pertama setelah Questionnaire dan menjadi fondasi sebelum Fieldwork.

Tujuan bisnis:

```text
Membuat Project memiliki target responden dan target sample yang jelas sebelum Fieldwork dibuat.
```

## 2. Problem Statement

Saat ini ResearchAI sudah memiliki:

- Project.
- Multiple Questionnaire.

Namun Project belum memiliki:

- Target sample.
- Kuota.
- Segmentasi.
- Wilayah.
- Dasar perhitungan progress Fieldwork.

Jika Fieldwork dibuat sekarang, progress tidak memiliki dasar yang jelas.

## 3. Product Hypothesis

Jika ResearchAI memiliki Sample Group di bawah Project, maka:

- Fieldwork dapat direncanakan dengan lebih jelas.
- Monitoring dapat menghitung completion rate.
- Project multi-questionnaire dapat dikelola per target respondent.
- QC dan Dataset nantinya dapat dilacak berdasarkan target sample.

## 4. Scope Discovery Sprint 8

Masuk scope:

- Business analysis Sample Management.
- ADR Sample Management.
- Sample Domain Model.
- Sample Workflow.
- UI concept.
- API concept.
- Database concept.
- Activity Logging concept.
- Security consideration.
- Out of Scope MVP.
- Acceptance Criteria untuk implementasi Sprint 9/10.

Tidak masuk scope:

- Coding backend.
- Coding frontend.
- Database migration.
- API implementation.
- Commit implementasi.

## 5. Proposed MVP Scope

Sample MVP mencakup:

- Sample Group.
- Project relationship.
- Questionnaire optional relationship.
- Sample Name.
- Target Respondent.
- Target Sample Size.
- Region optional.
- Segment optional.
- Quota Notes optional.
- Status Draft/Ready.
- Activity Logging.

## 6. Recommended Entities

### Sample Group

Entity utama untuk Sprint 9/10.

Purpose:

Mewakili satu kelompok target sample dalam Project.

Example:

```text
Sample Rumah Tangga - Target 1.200
Sample UMKM - Target 600
Sample Bank Peserta - Target 80
```

### Sample Quota

Ditunda.

Purpose:

Mewakili quota detail seperti gender, age group, region, atau segment.

## 7. Recommended Workflow

```text
Project Detail
  -> Sample Section
  -> Tambah Sample
  -> Simpan Draft
  -> Sample Detail
  -> Tandai Ready
```

Status:

```text
Draft -> Ready
```

## 8. Proposed UI

### Project Detail

Tambahkan Sample section di bawah Questionnaire.

Tampilkan:

- Total Sample Group.
- Total Target Sample.
- Ready Sample.
- Draft Sample.
- Sample list.
- Tombol `+ Tambah Sample`.

### Sample Create

Field:

- Questionnaire optional.
- Sample Name.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.

Button:

- Batal.
- Simpan Draft.

### Sample Detail

Tampilkan:

- Sample summary.
- Project reference.
- Questionnaire reference.
- Target respondent.
- Target sample size.
- Region.
- Segment.
- Quota notes.
- Next Business Action.

## 9. Proposed API

```text
GET /api/v1/projects/{project_id}/samples
POST /api/v1/projects/{project_id}/samples
GET /api/v1/samples/{sample_id}
PATCH /api/v1/samples/{sample_id}
PATCH /api/v1/samples/{sample_id}/status
```

## 10. Proposed Database

Table:

```text
samples
```

Columns:

- id.
- project_id.
- questionnaire_id.
- sample_name.
- target_respondent.
- target_sample_size.
- region.
- segment.
- quota_notes.
- status.
- sort_order.
- created_by.
- ready_at.
- created_at.
- updated_at.

## 11. Activity Logging

Events:

- Sample dibuat.
- Sample diperbarui.
- Sample ditandai Ready.

Location:

- Client Activity Timeline.
- Future Project Timeline.

## 12. Security

MVP:

- User harus login.
- created_by dari current user.
- Tidak menerima created_by dari frontend.

Future:

- RBAC.
- Project-level authorization.
- Audit log.

## 13. Risks

### Risk 1 - Sample terlalu kompleks

Mitigation:

- Fokus pada Sample Group.
- Tunda quota matrix.

### Risk 2 - Relasi Questionnaire tidak jelas

Mitigation:

- Questionnaire optional tetapi direkomendasikan.
- Target Respondent wajib.

### Risk 3 - Fieldwork readiness terlalu cepat

Mitigation:

- Fieldwork readiness rule dicatat, tetapi gate otomatis ditunda.

### Risk 4 - Migration debt

Mitigation:

- Product Owner perlu memutuskan apakah Alembic baseline dikerjakan sebelum implementasi Sample.

## 14. Open Questions

1. Apakah Sample wajib memilih Questionnaire?
2. Apakah Target Respondent boleh berbeda dari Questionnaire?
3. Apakah satu Questionnaire boleh memiliki beberapa Sample Group?
4. Apakah Region wajib pada MVP?
5. Apakah Segment wajib pada MVP?
6. Apakah status Sample cukup Draft dan Ready?
7. Apakah Sample Ready menjadi syarat membuat Fieldwork Plan?
8. Apakah Technical Foundation perlu dikerjakan sebelum Sprint 9?

## 15. Recommended Sprint Plan

### Sprint 8

Discovery dan Design Review Sample.

Output:

- ADR-006.
- Sample Domain Model.
- Sample Workflow.
- Sprint 8 Proposal.

### Sprint 9

Sample Backend.

Scope:

- Database model.
- Schema.
- Service.
- API.
- Activity logging.
- Backend tests.

### Sprint 10

Sample Frontend.

Scope:

- Project Detail Sample section.
- Sample Create.
- Sample Detail.
- Status Action.
- Browser testing.

## 16. Recommendation

Rekomendasi Product Manager:

Setujui Sample Management sebagai modul berikutnya.

Rekomendasi Solution Architect:

Sebelum implementasi Sprint 9, putuskan terlebih dahulu:

```text
Apakah Alembic Migration Baseline wajib dikerjakan sebelum Sample table dibuat?
```

Jika data ResearchAI mulai dianggap penting, Alembic sebaiknya dikerjakan dulu.

Jika masih local MVP exploration, Sample Backend dapat mengikuti pola script upgrade sementara, tetapi risikonya technical debt bertambah.
