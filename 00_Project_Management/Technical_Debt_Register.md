# Technical Debt Register

Tanggal:
26 Juli 2026

Scope:
ResearchAI setelah Sprint 7

## Summary

Technical debt ResearchAI masih wajar untuk MVP, tetapi beberapa item harus diselesaikan sebelum aplikasi bergerak ke production-like usage.

Prioritas tertinggi:

1. Database migration framework.
2. Authorization/RBAC.
3. Automated test baseline.
4. Shared workflow/activity infrastructure.

## Debt Register

| ID | Area | Technical Debt | Priority | Impact | Recommendation |
| --- | --- | --- | --- | --- | --- |
| TD-001 | Database | Belum ada Alembic migration framework | High | Schema drift, rollback sulit, environment tidak konsisten | Implement Alembic baseline |
| TD-002 | Database | Schema upgrade masih memakai script manual | High | Sulit audit dan tidak ideal untuk production | Migrasikan script upgrade ke migration formal |
| TD-003 | Security | Belum ada role-based access control | High | Semua user aktif berpotensi akses seluruh action | Buat permission matrix dan dependency authorization |
| TD-004 | Security | Belum ada object-level authorization | High | Risiko akses lintas client/project | Tambahkan access policy per resource |
| TD-005 | Testing | Belum ada automated backend integration test | High | Regression business flow sulit dideteksi | Tambahkan pytest untuk Proposal -> Project -> Questionnaire |
| TD-006 | Testing | Belum ada automated frontend regression test | Medium | UI flow bergantung testing manual | Tambahkan Playwright test setelah workflow stabil |
| TD-007 | Workflow | Status transition logic tersebar di services | Medium | Inconsistent workflow antar modul | Buat shared workflow helper |
| TD-008 | Activity | Activity logging berulang di setiap service | Medium | Event antar modul bisa tidak konsisten | Buat shared activity service |
| TD-009 | API | Belum ada pagination standar | Medium | List endpoint bisa lambat saat data besar | Tambahkan pagination contract |
| TD-010 | API | Deprecated endpoint belum ditandai formal | Medium | Developer bisa memakai endpoint lama | Tandai deprecated di OpenAPI dan docs |
| TD-011 | API | Error response belum standar | Medium | Frontend perlu banyak handling khusus | Buat error response convention |
| TD-012 | Frontend | Page components mulai panjang | Medium | Sulit dirawat saat modul bertambah | Pecah page menjadi sections/components |
| TD-013 | Frontend | Belum ada DataTable reusable | Medium | Table pattern akan duplikatif | Buat shared DataTable |
| TD-014 | Frontend | Form validation masih manual per page | Medium | UX dan validasi bisa tidak konsisten | Buat form field dan validation pattern |
| TD-015 | Design System | Design System belum menjadi component library lengkap | Medium | UI consistency bergantung disiplin manual | Tambahkan reusable components |
| TD-016 | Naming | Istilah campuran dan belum ada naming convention formal | Low | Onboarding dan komunikasi bisa membingungkan | Buat Naming Convention v1 |
| TD-017 | Security | Token disimpan di localStorage | Medium | Risiko XSS berdampak ke token | Evaluasi httpOnly cookie atau mitigasi XSS |
| TD-018 | Security | Secret key default masih tersedia | High | Risiko konfigurasi production lemah | Wajibkan secret dari env untuk non-dev |
| TD-019 | Data Validation | KoBo/XLSForm URL belum divalidasi ketat | Medium | Data reference bisa invalid | Tambahkan URL validation backend/frontend |
| TD-020 | Domain | ClientActivity belum menjadi general domain event | Medium | Project/module timeline sulit diperluas | Rancang Domain Activity/Event |
| TD-021 | Domain | Sample belum dimodelkan, padahal terkait langsung dengan Questionnaire | Medium | Fieldwork bisa salah fondasi | Discovery Sample sebelum Fieldwork |
| TD-022 | Operations | Belum ada background job untuk proses berat | Low | XLSForm parsing/AI/report akan block request | Tambahkan queue saat modul berat dimulai |
| TD-023 | Files | File/document storage belum solid | Medium | Attachment dan XLSForm upload belum siap | Buat storage service |
| TD-024 | Documentation | Baseline dokumen aktif belum diindeks | Low | Risiko memakai dokumen lama | Buat Architecture Baseline Index |
| TD-025 | Repository | Banyak dokumen lama masih untracked | Medium | Commit berikutnya berisiko tercampur | Rapikan staging/commit dokumen baseline |

## High Priority Detail

### TD-001 Database Migration Framework

Masalah:

ResearchAI belum memakai Alembic atau migration framework formal.

Dampak:

- Sulit tracking perubahan schema.
- Sulit rollback.
- Risiko perbedaan schema antar laptop/server.

Recommended Sprint:

Technical Foundation Sprint sebelum schema Sample dibuat.

### TD-003 Role-Based Access Control

Masalah:

Endpoint hanya memvalidasi user login, belum role/action permission.

Dampak:

- Semua user aktif dapat mengakses action penting.
- Tidak cocok untuk ERP multi-role.

Recommended Sprint:

Sebelum modul Fieldwork dan Finance.

### TD-005 Automated Backend Integration Test

Masalah:

Business flow diuji manual/API ad hoc.

Dampak:

- Regression sulit dideteksi saat refactoring.

Recommended Test Flow:

```text
Login
  -> Create Proposal
  -> Approve Proposal
  -> Setup Project
  -> Create Multiple Questionnaire
  -> Mark Questionnaire Ready
  -> Verify Activity Logging
```

## Debt by Phase

### Before Sprint 8

Recommended:

- Architecture baseline index.
- API convention document.
- Decide whether to implement Alembic now.

### Before Sample Implementation

Recommended:

- Clarify Questionnaire -> Sample relationship.
- Add backend integration tests.
- Add pagination convention if list grows.

### Before Fieldwork Implementation

Required:

- RBAC.
- Object-level authorization.
- Project readiness rules.
- Domain activity/event design.

### Before Production

Required:

- Alembic migration.
- Environment secret enforcement.
- RBAC.
- Automated tests.
- Error handling standard.
- File storage strategy.

## Priority Summary

High:

- TD-001
- TD-002
- TD-003
- TD-004
- TD-005
- TD-018

Medium:

- TD-006
- TD-007
- TD-008
- TD-009
- TD-010
- TD-011
- TD-012
- TD-013
- TD-014
- TD-015
- TD-017
- TD-019
- TD-020
- TD-021
- TD-023
- TD-025

Low:

- TD-016
- TD-022
- TD-024
