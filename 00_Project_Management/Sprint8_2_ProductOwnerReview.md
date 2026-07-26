# Sprint 8.2 Product Owner Review

Nama Sprint:
Sampling Plan API Layer

Status Review:
APPROVED

Tanggal:
26 Juli 2026

Dokumen acuan:

- `Sprint8_Design_Freeze.md`
- `Sprint8_2_Design_Freeze.md`

## 1. Executive Summary

Implementasi Sprint 8.2 API Layer telah direview terhadap Design Freeze.

Hasil review:

```text
APPROVED
```

Sprint 8.2 siap di-commit.

Implementasi sudah menyediakan API backend untuk:

- CRUD Sample Group.
- CRUD Sampling Target.
- Status action `Draft -> Ready`.
- Activity Logging.
- Authorization.
- Swagger/OpenAPI.
- API tests.

Tidak ditemukan perubahan business rule, perubahan domain model, atau fitur di luar scope.

## 2. Compliance

### 2.1 Endpoint REST API

Compliant.

Endpoint yang tersedia:

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

Catatan:

Design Freeze mewajibkan endpoint target eksplisit untuk create/update/delete. Implementasi juga menambahkan list/detail Sampling Target karena instruksi implementasi meminta REST API Sampling Target lengkap. Tambahan ini tidak melanggar Design Freeze.

### 2.2 URI

Compliant.

URI mengikuti pola REST API:

- Collection Sample Group berada di bawah Project.
- Detail Sample Group memakai `sample_group_id`.
- Target create berada di bawah Sample Group.
- Detail/update/delete Sampling Target memakai `target_id`.

### 2.3 HTTP Method

Compliant.

| Use Case | Method | Status |
| --- | --- | --- |
| List | GET | Sesuai |
| Detail | GET | Sesuai |
| Create | POST | Sesuai |
| Update | PATCH | Sesuai |
| Delete | DELETE | Sesuai |
| Status Action | PATCH | Sesuai Design Freeze |

### 2.4 Request Schema

Compliant.

Create Sample Group menerima:

- `questionnaire_id`
- `sample_group_name`
- `target_respondent`
- `notes`
- `targets`

Update Sample Group menerima partial payload.

Jika `targets` dikirim pada PATCH Sample Group, implementasi melakukan full replacement sesuai Design Freeze.

Sampling Target menerima:

- `region_type`
- `region_name`
- `target_sample`

### 2.5 Response Schema

Compliant.

Mutation Sample Group dan Sampling Target mengembalikan Sample Group detail terbaru, kecuali delete Sample Group yang mengembalikan:

```text
204 No Content
```

Delete Sampling Target mengembalikan Sample Group detail terbaru agar frontend langsung mendapat total target terbaru.

### 2.6 Validation

Compliant.

Validation sudah mencakup:

- Project harus ada.
- Sample Group harus ada.
- Sampling Target harus ada.
- Questionnaire harus berada pada Project yang sama.
- Sample Group Name wajib.
- Target sample harus lebih dari 0.
- Minimal satu Sampling Target saat create/update inline.
- Delete Sampling Target terakhir ditolak.

### 2.7 Business Rule

Compliant.

Business rule final tetap terjaga:

- Sampling Plan bukan database responden.
- Sample Group berada di bawah Project.
- Sampling Target berada di bawah Sample Group.
- Questionnaire optional saat Draft.
- Questionnaire harus dari Project yang sama jika dipilih.
- Satu Questionnaire dapat digunakan banyak Sample Group.
- Status flow hanya `Draft -> Ready`.
- Ready tidak dapat diedit.
- Ready tidak dapat dihapus.

### 2.8 Authorization

Compliant.

Semua endpoint Sampling Plan menggunakan authenticated user melalui dependency login.

Project-level permission belum diterapkan dan sudah tercatat sebagai technical debt, bukan blocker MVP.

### 2.9 Activity Logging

Compliant.

Activity logging berjalan untuk mutation event:

- Sampling Plan dibuat.
- Sampling Plan diperbarui.
- Sampling Plan ditandai Ready.
- Sampling Plan dihapus.

Perubahan target wilayah dicatat sebagai `Sampling Plan diperbarui`, sesuai keputusan agar timeline tidak terlalu ramai.

### 2.10 Swagger/OpenAPI

Compliant.

OpenAPI sudah memuat endpoint Sampling Plan:

```text
/api/v1/projects/{project_id}/sample-groups
/api/v1/sample-groups/{sample_group_id}
/api/v1/sample-groups/{sample_group_id}/status
/api/v1/sample-groups/{sample_group_id}/targets
/api/v1/sampling-targets/{target_id}
```

### 2.11 Unit Test

Compliant.

Unit test service Sampling Plan tetap PASS.

### 2.12 Integration/API Test

Compliant.

API test sudah mencakup:

- Sample Group create/list/detail/update/delete.
- Sampling Target list/detail/create/update/delete.
- Status Draft -> Ready.
- Delete Ready Sample Group ditolak.
- Delete target terakhir ditolak.
- PATCH Sample Group targets full replacement.
- Activity logging.
- Pattern A.
- Pattern B.
- Validation error.
- Not found error.

## 3. Validasi Khusus

| Checklist | Status | Catatan |
| --- | --- | --- |
| Delete Sample Group hanya saat Draft | PASS | Ready delete menghasilkan 400 |
| Delete Sampling Target terakhir ditolak | PASS | Target terakhir menghasilkan 400 |
| PATCH Sample Group targets full replacement | PASS | Target lama diganti dan total dihitung ulang |
| Tidak ada orphan Sampling Target | PASS | Sudah divalidasi di service test |
| Activity Logging berjalan | PASS | Create/update/ready/delete dicatat |
| Authorization sesuai | PASS | Semua endpoint memakai authenticated user |
| Endpoint sesuai Design Freeze | PASS | Endpoint final tersedia |

## 4. Hasil Testing

### Compile

```text
PASS
```

### Backend Unit/API Test

```text
Ran 11 tests
OK
```

### Swagger/OpenAPI Verification

```text
PASS
```

Endpoint Sampling Plan muncul pada OpenAPI schema.

## 5. Temuan

Tidak ditemukan blocker.

Temuan non-blocker:

1. Endpoint list/detail Sampling Target ditambahkan untuk memenuhi instruksi CRUD lengkap.
2. Error response masih memakai format FastAPI `detail`.
3. Authorization masih authenticated user, belum project-level permission.

Semua temuan di atas tidak melanggar Design Freeze dan tidak menjadi blocker.

## 6. Bug

Tidak ditemukan bug blocker pada review ini.

## 7. Technical Debt

| ID | Technical Debt | Priority | Status |
| --- | --- | --- | --- |
| TD-SAMPLING-API-001 | Error response belum standardized | Low | Non-blocker |
| TD-SAMPLING-API-002 | Permission masih authenticated user | Medium | Non-blocker |
| TD-SAMPLING-API-003 | Response list bisa berat jika target banyak | Low | Non-blocker |
| TD-SAMPLING-API-004 | Filter list belum masuk API MVP | Low | Non-blocker |
| TD-SAMPLING-API-005 | Alembic migration framework belum tersedia | Medium | Non-blocker |
| TD-SAMPLING-API-006 | `datetime.utcnow()` deprecated warning | Low | Non-blocker |
| TD-SAMPLING-API-007 | `HTTP_422_UNPROCESSABLE_ENTITY` deprecated warning | Low | Non-blocker |

## 8. Improvement

Improvement untuk sprint berikutnya:

1. Tambahkan project-level permission saat modul Role/Permission sudah matang.
2. Standardisasi error response.
3. Pertimbangkan lightweight list response jika target wilayah banyak.
4. Tambahkan filter API jika kebutuhan frontend meningkat.
5. Migrasikan datetime ke timezone-aware datetime.
6. Update status code constant FastAPI yang deprecated.

Tidak ada improvement yang wajib dilakukan sebelum commit Sprint 8.2.

## 9. Rekomendasi

Rekomendasi Product Owner:

1. Sprint 8.2 dinyatakan memenuhi acceptance criteria.
2. Implementasi siap di-commit.
3. Setelah commit, lanjutkan ke Sprint 8.3 untuk frontend Sampling Plan.
4. Technical debt dicatat dan tidak menghambat MVP.

## 10. Final Decision

```text
APPROVED
```

Sprint 8.2 siap di-commit.
