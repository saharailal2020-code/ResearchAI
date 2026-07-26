# SPR-007 Revision Plan

Nama:
Sprint 7 Revision - Multiple Questionnaire Support

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. Tujuan Revisi

Merevisi Sprint 7 Questionnaire Foundation MVP agar mendukung business rule baru:

```text
Satu Project dapat memiliki lebih dari satu Questionnaire.
```

Revisi ini menggantikan desain dan implementasi awal yang membatasi satu Project hanya satu Questionnaire.

## 2. Scope Revisi

Masuk scope:

- Ubah relasi Project -> Questionnaire menjadi one-to-many.
- Hapus unique constraint pada `project_id`.
- Tambahkan field:
  - `respondent_group`
  - `instrument_type`
  - `sort_order`
- Ubah endpoint Project Questionnaire menjadi plural.
- Tampilkan daftar Questionnaire pada Project Detail.
- Izinkan Create Questionnaire kedua, ketiga, dan seterusnya.
- Update Questionnaire Create form.
- Update Questionnaire Detail.
- Activity Logging tetap berjalan.
- Browser testing multiple Questionnaire.

Tetap out of scope:

- Form Builder.
- KoBo API.
- XLSForm Parsing.
- Version History.
- FGD.
- IDI.
- AI Review.
- Validation Logic.
- Sample.
- Fieldwork.
- QC.

## 3. Database Revision

### Current

```text
Project 1 -> 0/1 Questionnaire
```

### Target

```text
Project 1 -> many Questionnaire
```

Model changes:

- Remove:

```text
UniqueConstraint("project_id")
```

- Add:

```text
respondent_group
instrument_type
sort_order
```

- Change relationship:

```text
Project.questionnaire
```

to:

```text
Project.questionnaires
```

## 4. API Revision

### New Primary Endpoints

```text
GET /api/v1/projects/{project_id}/questionnaires
POST /api/v1/projects/{project_id}/questionnaires
GET /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}/status
```

### Deprecated Compatibility Endpoints

Optional:

```text
GET /api/v1/projects/{project_id}/questionnaire
POST /api/v1/projects/{project_id}/questionnaire
```

Recommendation:

- Keep compatibility during Sprint 7 revision.
- Frontend should use plural endpoints only.

## 5. Frontend Revision

### Project Detail

Replace single Questionnaire card with compact list/table.

Columns:

- Name.
- Respondent Group.
- Instrument Type.
- Version.
- Status.
- Last Updated.
- Action.

Action:

- `+ Buat Questionnaire`.
- `Buka`.

### Questionnaire Create

Fields:

- Questionnaire Name.
- Respondent Group.
- Instrument Type.
- KoBo Link.
- XLSForm Link.

### Questionnaire Detail

Show:

- Questionnaire Name.
- Respondent Group.
- Instrument Type.
- Version.
- Status.
- KoBo Link.
- XLSForm Link.
- Last Updated.
- Project Reference.

Actions:

- Edit Draft.
- Tandai Ready.

## 6. Workflow Revision

Updated workflow:

```text
Project Detail
  |
  v
Questionnaire Section
  |
  +-- Buat Questionnaire Rumah Tangga
  |
  +-- Buat Questionnaire UMKM
  |
  +-- Buat Questionnaire Bank Pengelola Kas Titipan
  |
  +-- Buat Questionnaire Bank Peserta
```

Each Questionnaire:

```text
Draft -> Ready
```

## 7. Acceptance Criteria Revised

1. User dapat membuat lebih dari satu Questionnaire dalam satu Project.
2. Project Detail menampilkan daftar Questionnaire.
3. Setiap Questionnaire memiliki:
   - Questionnaire Name.
   - Respondent Group.
   - Instrument Type.
   - Version Number.
   - Status.
   - KoBo Link.
   - XLSForm Link.
   - Last Updated.
4. Setiap Questionnaire dapat dibuka ke detail.
5. Questionnaire Draft dapat diedit.
6. Questionnaire dapat ditandai Ready.
7. Questionnaire Ready tidak dapat diedit langsung pada MVP.
8. Activity Logging mencatat setiap event Questionnaire.
9. Endpoint plural berjalan.
10. Backward compatibility endpoint singular tidak merusak data lama jika dipertahankan.
11. Frontend lint berhasil.
12. Frontend build berhasil.
13. Backend/API test berhasil.
14. Browser testing multiple Questionnaire berhasil.
15. Regression Project dan Proposal tetap berhasil.

## 8. Testing Plan Revised

Backend:

- Create first Questionnaire.
- Create second Questionnaire in same Project.
- List Questionnaires by Project.
- Get Questionnaire Detail.
- Edit Draft Questionnaire.
- Mark Ready.
- Reject edit Ready.
- Activity logging per Questionnaire.

Frontend:

- Project Detail empty state.
- Project Detail list multiple Questionnaire.
- Create Questionnaire.
- Create second Questionnaire.
- Questionnaire Detail Draft.
- Questionnaire Detail Ready.
- Loading state.
- Error state.

Regression:

- Login.
- Dashboard.
- Client.
- Proposal.
- Project Detail.
- Setup Project.
- Activity Logging.

## 9. Migration Plan

Because Sprint 7 is not committed:

1. Revise current uncommitted implementation.
2. Adjust local schema.
3. Preserve or reset local test data as needed.
4. Re-run API and browser tests.

If preserving local data:

- Drop unique constraint.
- Add new nullable columns.
- Backfill existing rows.

If not preserving local data:

- Recreate `questionnaires` table in local dev.

Note:

- TECH-001 remains a high-priority backlog before production-grade schema changes.

## 10. Recommendation

Recommendation:

```text
Use Sprint 7.1 label for this revision.
```

Reason:

- The business rule change is fundamental.
- It affects database, API, frontend, workflow, and tests.
- It deserves explicit Product Owner Review before implementation changes.

However, because Sprint 7 is not committed, implementation can still be revised before final Sprint 7 commit.

Recommended next step:

```text
Product Owner approves ADR-005 and SPR-007 Revision Plan
  -> implement multiple questionnaire
  -> test
  -> PO review
  -> commit
```
