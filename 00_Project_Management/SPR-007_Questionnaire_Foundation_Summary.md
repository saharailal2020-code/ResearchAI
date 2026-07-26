# Sprint 7 Summary

Nama Sprint:
Questionnaire Foundation MVP

Milestone:
M3 - Research Preparation

Status:
Selesai dan disetujui Product Owner

Tanggal Closing:
26 Juli 2026

## Tujuan Sprint

Membangun fondasi modul Questionnaire sebagai object operasional di bawah Project.

Sprint ini memastikan ResearchAI dapat mencatat metadata instrumen riset kuantitatif sebelum modul Sample dan Fieldwork dikembangkan.

## Perubahan Business Rule

Pada Product Owner Review, business rule direvisi:

```text
Satu Project dapat memiliki satu atau lebih Questionnaire.
Questionnaire dibedakan berdasarkan Target Respondent.
```

Keputusan ini menggantikan desain awal yang membatasi satu Project hanya satu Questionnaire.

## Fitur yang Selesai

- Project mendukung banyak Questionnaire.
- Project Detail menampilkan daftar Questionnaire.
- User dapat membuat Questionnaire dari Project Detail.
- User dapat membuat lebih dari satu Questionnaire pada Project yang sama.
- Questionnaire memiliki status `Draft` dan `Ready`.
- Questionnaire memiliki version number default `1`.
- Questionnaire Draft dapat diedit.
- Questionnaire dapat ditandai Ready.
- Questionnaire Ready tidak dapat diedit pada MVP.
- Activity Logging berjalan untuk event Questionnaire.
- Endpoint plural menjadi endpoint utama.
- Endpoint singular lama dipertahankan sementara sebagai deprecated compatibility endpoint.
- Script upgrade database idempotent tersedia untuk revisi multiple Questionnaire.

## Field Final MVP

- Questionnaire Name.
- Target Respondent.
- Instrument Type.
- Version.
- Status.
- KoBo Link.
- XLSForm Link.
- Last Updated.

## Endpoint yang Digunakan

Endpoint utama:

```text
GET /api/v1/projects/{project_id}/questionnaires
POST /api/v1/projects/{project_id}/questionnaires
GET /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}/status
```

Endpoint deprecated:

```text
GET /api/v1/projects/{project_id}/questionnaire
POST /api/v1/projects/{project_id}/questionnaire
```

## Activity Logging

Event yang otomatis tercatat:

- Questionnaire dibuat.
- Questionnaire diperbarui.
- Questionnaire ditandai Ready.

Activity dicatat ke Client Activity Timeline melalui hubungan:

```text
Client -> Project -> Questionnaire
```

## Testing

Testing yang dilakukan:

- Backend compile.
- Database upgrade script.
- API multiple Questionnaire.
- Activity Logging.
- Frontend lint.
- Frontend build.
- Browser testing.
- Regression Project Detail.

Hasil:

```text
PASS
```

## Regression Testing

Regression area:

- Login.
- Backend health.
- Frontend app load.
- Project Detail.
- Questionnaire Create.
- Questionnaire Detail.
- Multiple Questionnaire list.
- Questionnaire status Ready.
- Activity Logging.

Hasil:

```text
PASS
```

## File Utama yang Berubah

Backend:

- `backend/app/api/v1/questionnaires.py`
- `backend/app/api/v1/router.py`
- `backend/app/models/questionnaire.py`
- `backend/app/models/project.py`
- `backend/app/models/__init__.py`
- `backend/app/schemas/questionnaire.py`
- `backend/app/schemas/project.py`
- `backend/app/services/questionnaires.py`
- `backend/app/services/projects.py`
- `backend/scripts/upgrade_questionnaire_multiple.py`

Frontend:

- `frontend/src/App.jsx`
- `frontend/src/pages/ProjectDetailPage.jsx`
- `frontend/src/pages/QuestionnaireCreatePage.jsx`
- `frontend/src/pages/QuestionnaireDetailPage.jsx`
- `frontend/src/services/questionnaires.js`
- `frontend/src/utils/statusStyles.js`

Documents:

- `00_Project_Management/ADR-005_Multiple_Questionnaire.md`
- `00_Project_Management/Questionnaire_Impact_Analysis.md`
- `00_Project_Management/SPR-007_Revision_Plan.md`
- `00_Project_Management/SPR-007_Questionnaire_Foundation_Summary.md`
- `00_Project_Management/SPR-007_Release_Notes.md`
- `00_Project_Management/SPR-007_Technical_Debt.md`
- `11_Documentation/WF-006_Questionnaire.md`

## Product Owner Notes

Sprint 7 Revision telah disetujui oleh Product Owner.

Keputusan final:

- Satu Project dapat memiliki banyak Questionnaire.
- Pembeda utama Questionnaire adalah Target Respondent.
- KoBo API belum masuk MVP.
- XLSForm parsing belum masuk MVP.
- Version history penuh belum masuk MVP.

## Definition of Done

- Business rule sesuai ADR-005.
- Backend mendukung multiple Questionnaire.
- Frontend menampilkan daftar Questionnaire.
- Browser testing berhasil.
- Testing teknis berhasil.
- Product Owner Review selesai.
- Siap commit.
