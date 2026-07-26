# Changelog

Semua perubahan penting ResearchAI dicatat di file ini.

## 2026-07-26 - Sprint 8.2 Sampling Plan API Layer

### Added

- REST API untuk Sample Group:
  - List Sample Group per Project.
  - Create Sample Group.
  - Detail Sample Group.
  - Update Sample Group Draft.
  - Delete Sample Group Draft.
  - Status action Draft ke Ready.
- REST API untuk Sampling Target:
  - List Sampling Target per Sample Group.
  - Create Sampling Target.
  - Detail Sampling Target.
  - Update Sampling Target.
  - Delete Sampling Target.
- Swagger/OpenAPI documentation untuk endpoint Sampling Plan.
- API tests untuk Sample Group dan Sampling Target.
- Product Owner Review document untuk Sprint 8.2.

### Business Rules

- Delete Sample Group hanya diperbolehkan pada status Draft.
- Delete Sampling Target terakhir ditolak.
- PATCH Sample Group dengan field `targets` berarti full replacement.
- Replacement Sampling Target tidak boleh menghasilkan orphan record.
- Activity Logging dicatat dari backend service.

### Technical Debt

- Error response masih menggunakan format FastAPI `detail`.
- Permission masih berbasis authenticated user.
- Alembic migration framework belum tersedia.
- Warning `datetime.utcnow()` dan constant HTTP 422 perlu dirapikan pada sprint teknis berikutnya.
