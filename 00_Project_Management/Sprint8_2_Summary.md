# Sprint 8.2 Summary

Nama Sprint:
Sampling Plan API Layer

Status:
Completed

Tanggal:
26 Juli 2026

## 1. Objective

Membangun API Layer untuk modul Sampling Plan berdasarkan Sprint 8.1 Backend Foundation dan Sprint 8.2 Design Freeze.

API ini menjadi fondasi untuk frontend Sampling Plan pada sprint berikutnya.

## 2. Scope

Scope Sprint 8.2:

- REST API Sample Group.
- REST API Sampling Target.
- Validation sesuai Design Freeze.
- Error response.
- Status code.
- Activity Logging.
- Authorization.
- Swagger/OpenAPI.
- API tests.

Out of scope:

- Frontend.
- Import Excel.
- Export Excel.
- Sample Database.
- Enumerator.
- Fieldwork.
- QC.
- Dashboard.

## 3. Implementasi

Implementasi yang diselesaikan:

1. Router API Sampling Plan.
2. Registration router ke API v1.
3. Schema request/response Sampling Target update.
4. Repository helper untuk Sampling Target.
5. Service delete Sample Group Draft.
6. Service CRUD Sampling Target.
7. Activity Logging untuk create/update/delete/ready.
8. API tests untuk endpoint dan business rule.

## 4. Endpoint yang Ditambahkan

```text
GET    /api/v1/projects/{project_id}/sample-groups
POST   /api/v1/projects/{project_id}/sample-groups
GET    /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}
DELETE /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}/status
GET    /api/v1/sample-groups/{sample_group_id}/targets
POST   /api/v1/sample-groups/{sample_group_id}/targets
GET    /api/v1/sampling-targets/{target_id}
PATCH  /api/v1/sampling-targets/{target_id}
DELETE /api/v1/sampling-targets/{target_id}
```

## 5. Test Result

Compile:

```text
PASS
```

Backend unit/API test:

```text
Ran 11 tests
OK
```

Swagger/OpenAPI verification:

```text
PASS
```

## 6. Product Owner Approval

Product Owner Review menghasilkan keputusan:

```text
APPROVED
```

Sprint 8.2 dinyatakan siap commit.

## 7. Technical Debt

Technical debt yang belum diselesaikan:

1. Error response belum standardized.
2. Permission masih authenticated user, belum project-level permission.
3. Response list dapat menjadi berat jika target wilayah sangat banyak.
4. Filter list Sample Group belum menjadi API MVP.
5. Alembic migration framework belum tersedia.
6. `datetime.utcnow()` deprecated warning.
7. `HTTP_422_UNPROCESSABLE_ENTITY` deprecated warning.

## 8. Lessons Learned

1. Design Freeze membantu menjaga API tetap fokus dan tidak melebar ke database responden.
2. Endpoint Sampling Target eksplisit membuat frontend lebih mudah mengelola target wilayah.
3. Full replacement untuk `targets` perlu selalu didokumentasikan jelas karena berisiko disalahpahami.
4. API test harus mencakup business rule kritis, bukan hanya happy path.

## 9. Definition of Done

- API endpoint tersedia.
- Business rule utama tervalidasi.
- Test lulus.
- Product Owner Review approved.
- Sprint summary dan retrospective tersedia.
- Perubahan siap di-commit dan push.
