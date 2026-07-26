# SPR-007 Implementation Plan

Nama Sprint:
Questionnaire MVP

Status:
Draft for Product Owner Review

Milestone:
M3 - Research Preparation

Basis:

- Questionnaire Discovery v1
- WF-006 Questionnaire
- Domain Model v1
- WF-005 Project Detail
- Design System v1

## 1. Tujuan Sprint

Membangun Questionnaire MVP sebagai modul pertama di bawah Project.

Sprint ini bertujuan membuat ResearchAI mampu mencatat dan menyiapkan instrumen riset sebelum Sample dan Fieldwork.

## 2. Scope Sprint 7

Masuk scope:

- Backend entity Questionnaire.
- Relasi Questionnaire ke Project.
- Questionnaire status `Draft` dan `Ready`.
- Version number sederhana.
- Create Questionnaire.
- Edit Questionnaire Draft.
- Questionnaire Detail.
- Action `Tandai Ready`.
- Integrasi placeholder Questionnaire pada Project Detail.
- Activity Logging:
  - Questionnaire dibuat.
  - Questionnaire diperbarui.
  - Questionnaire ditandai Ready.
- Loading state.
- Empty state.
- Error state.
- Browser testing.
- Regression testing.

## 3. Out of Scope

- Form builder.
- Question item editor.
- Skip logic editor.
- XLSForm parser.
- KoBoToolbox API integration.
- File upload penuh.
- Client review portal.
- Multi-version history lengkap.
- Multi-questionnaire kompleks.
- Sample module.
- Fieldwork module.
- QC module.
- Dataset module.
- Dashboard module.
- Report module.

## 4. Candidate Backend Components

Files:

- `backend/app/models/questionnaire.py`
- `backend/app/schemas/questionnaire.py`
- `backend/app/services/questionnaires.py`
- `backend/app/api/v1/questionnaires.py`
- Update `backend/app/models/project.py`
- Update `backend/app/models/__init__.py`
- Update router.

Candidate endpoints:

```text
GET /api/v1/projects/{project_id}/questionnaires
POST /api/v1/projects/{project_id}/questionnaires
GET /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}
PATCH /api/v1/questionnaires/{questionnaire_id}/status
```

Payload create:

```json
{
  "questionnaire_title": "Main Survey Questionnaire",
  "questionnaire_type": "Quantitative Survey",
  "description": "Instrumen utama untuk survey CSAT.",
  "source_format": "XLSForm",
  "xlsform_reference": "https://...",
  "kobo_form_url": null
}
```

## 5. Candidate Frontend Components

Files:

- `frontend/src/pages/QuestionnaireCreatePage.jsx`
- `frontend/src/pages/QuestionnaireDetailPage.jsx`
- `frontend/src/services/questionnaires.js`
- Update `frontend/src/pages/ProjectDetailPage.jsx`
- Update `frontend/src/App.jsx`

Routes:

```text
/projects/:projectId/questionnaires/new
/questionnaires/:questionnaireId
```

Optional route:

```text
/projects/:projectId/questionnaires
```

## 6. UI Scope

### Project Detail Integration

Questionnaire placeholder berubah menjadi:

- Jika belum ada Questionnaire:
  - Empty state.
  - Button `Buat Questionnaire`.
- Jika sudah ada:
  - Title.
  - Status badge.
  - Version.
  - Button `Buka Questionnaire`.

### Questionnaire Create

Field:

- Questionnaire Title.
- Questionnaire Type.
- Description.
- Source Format.
- XLSForm Reference optional.
- KoBo Form URL optional.

### Questionnaire Detail

Tampil:

- Questionnaire Title.
- Status badge.
- Version.
- Project Reference.
- Questionnaire Type.
- Source Format.
- XLSForm Reference.
- KoBo Form URL.
- Created Date.
- Updated Date.
- Ready Date.

Actions:

- Edit Draft.
- Tandai Ready.

## 7. Acceptance Criteria

1. User dapat membuat Questionnaire dari Project Detail.
2. Questionnaire wajib terkait dengan Project.
3. Questionnaire status awal `Draft`.
4. Questionnaire memiliki version number default `1`.
5. User dapat melihat Questionnaire Detail.
6. User dapat edit Questionnaire selama status `Draft`.
7. User dapat menandai Questionnaire sebagai `Ready`.
8. Questionnaire `Ready` tidak dapat diedit langsung pada MVP.
9. Project Detail menampilkan status Questionnaire.
10. Activity `Questionnaire dibuat` tercatat.
11. Activity `Questionnaire diperbarui` tercatat.
12. Activity `Questionnaire ditandai Ready` tercatat.
13. Frontend lint berhasil.
14. Frontend build berhasil.
15. Backend/API test berhasil.
16. Browser testing berhasil.
17. Regression Project dan Proposal tetap berhasil.

## 8. Risiko

### Risiko 1: Scope melebar menjadi form builder

Mitigasi:

- Batasi MVP pada metadata dan reference.
- Jangan membuat question editor.

### Risiko 2: KoBoToolbox integration terlalu awal

Mitigasi:

- Simpan URL/reference dulu.
- API integration menjadi backlog.

### Risiko 3: Versioning terlalu kompleks

Mitigasi:

- Simpan version number.
- Full version history ditunda.

### Risiko 4: Project Fieldwork gate belum tersedia

Mitigasi:

- Dokumentasikan rule bahwa Fieldwork butuh Questionnaire Ready.
- Implement gate saat Project Status Actions lanjutan dibuat.

### Risiko 5: Database migration belum tersedia

Mitigasi:

- TECH-001 tetap prioritas teknis.
- Jika Sprint 7 menambah table baru, perlu keputusan apakah Alembic dikerjakan dulu.

## 9. Testing Plan

Backend testing:

- Create Questionnaire.
- Get Questionnaire.
- List Questionnaire by Project.
- Edit Draft Questionnaire.
- Reject edit Ready Questionnaire.
- Mark Ready.
- Activity logging.

Frontend testing:

- Lint.
- Build.
- Browser create Questionnaire.
- Browser detail Questionnaire.
- Browser edit Draft.
- Browser mark Ready.
- Browser empty state.
- Browser loading state.
- Browser error state.

Regression testing:

- Login.
- Dashboard.
- Client.
- Proposal.
- Setup Project.
- Project Detail.
- Activity Logging.

## 10. Technical Notes

TECH-001 Database Migration Framework masih backlog high priority.

Sebelum Sprint 7 implementation, Product Owner perlu memutuskan:

- Apakah TECH-001 dikerjakan sebelum Questionnaire table dibuat.
- Atau Sprint 7 tetap mengikuti pola local schema saat ini dan migration menyusul.

## 11. Rekomendasi Implementasi

Rekomendasi:

1. Lakukan Design Review Questionnaire terlebih dahulu.
2. Freeze field MVP.
3. Putuskan Alembic dulu atau setelah Sprint 7.
4. Implement backend Questionnaire.
5. Implement frontend Project Detail integration.
6. Implement Questionnaire Create/Detail.
7. Testing dan PO Review.

Sprint 7 sebaiknya tetap kecil dan fokus agar M3 dimulai dengan fondasi Research Preparation yang stabil.
