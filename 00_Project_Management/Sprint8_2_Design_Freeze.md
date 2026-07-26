# Sprint 8.2 Design Freeze

Nama Sprint:
Sampling Plan API Layer

Status:
READY FOR IMPLEMENTATION

Tanggal:
26 Juli 2026

Dokumen acuan:

- `Sprint8_Design_Freeze.md`
- `Sprint8_2_Planning.md`
- `SamplingPlan_API_Design.md`
- `Sprint8_2_DesignReview.md`

## 1. Design Freeze Summary

Sprint 8.2 membekukan desain API untuk modul Sampling Plan.

API ini menjadi dasar implementasi backend API sebelum frontend Sampling Plan dibangun.

Keputusan utama:

```text
Domain UI: Sampling Plan
Resource API utama: Sample Group
Resource API detail wilayah: Sampling Target
```

API harus mendukung:

- CRUD Sample Group.
- CRUD Sampling Target.
- Status action `Draft -> Ready`.
- Pattern A: banyak Questionnaire dan banyak Sample Group.
- Pattern B: satu Questionnaire digunakan oleh banyak Sample Group.

API tidak boleh menyimpan database responden individual.

## 2. Final API Scope

Scope final Sprint 8.2:

1. List Sample Group per Project.
2. Create Sample Group.
3. Get Sample Group detail.
4. Update Sample Group Draft.
5. Delete Sample Group Draft.
6. Mark Sample Group Ready.
7. Create Sampling Target.
8. Update Sampling Target.
9. Delete Sampling Target.
10. Activity logging untuk mutation event.
11. Authorization berbasis authenticated user.
12. API tests untuk business rule utama.

## 3. Final Endpoint List

Endpoint final:

```text
GET    /api/v1/projects/{project_id}/sample-groups
POST   /api/v1/projects/{project_id}/sample-groups
GET    /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}
DELETE /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}/status
POST   /api/v1/sample-groups/{sample_group_id}/targets
PATCH  /api/v1/sampling-targets/{target_id}
DELETE /api/v1/sampling-targets/{target_id}
```

Keputusan final:

- Endpoint Sampling Target bersifat eksplisit.
- Create/update Sample Group tetap dapat menerima `targets` secara inline.
- `targets` pada PATCH Sample Group berarti full replacement.
- Endpoint target eksplisit digunakan untuk perubahan per baris target wilayah.

## 4. Final URI and HTTP Method

| Use Case | URI | Method |
| --- | --- | --- |
| List Sample Group per Project | `/api/v1/projects/{project_id}/sample-groups` | GET |
| Create Sample Group | `/api/v1/projects/{project_id}/sample-groups` | POST |
| Get Sample Group Detail | `/api/v1/sample-groups/{sample_group_id}` | GET |
| Update Sample Group Draft | `/api/v1/sample-groups/{sample_group_id}` | PATCH |
| Delete Sample Group Draft | `/api/v1/sample-groups/{sample_group_id}` | DELETE |
| Mark Sample Group Ready | `/api/v1/sample-groups/{sample_group_id}/status` | PATCH |
| Create Sampling Target | `/api/v1/sample-groups/{sample_group_id}/targets` | POST |
| Update Sampling Target | `/api/v1/sampling-targets/{target_id}` | PATCH |
| Delete Sampling Target | `/api/v1/sampling-targets/{target_id}` | DELETE |

## 5. Final Request Schema

### 5.1 Create Sample Group

```json
{
  "questionnaire_id": "uuid atau null",
  "sample_group_name": "Rumah Tangga",
  "target_respondent": "Rumah Tangga",
  "notes": "Target berdasarkan proposal STKU.",
  "targets": [
    {
      "region_type": "Provinsi",
      "region_name": "Jawa Barat",
      "target_sample": 800
    }
  ]
}
```

Rules:

- `status` tidak dikirim dari frontend.
- `total_target_sample` tidak dikirim dari frontend.
- `created_by` tidak dikirim dari frontend.
- Status otomatis `Draft`.
- Total target dihitung backend.
- User pembuat diambil dari user login.

### 5.2 Update Sample Group Draft

```json
{
  "questionnaire_id": "uuid atau null",
  "sample_group_name": "Rumah Tangga Updated",
  "target_respondent": "Rumah Tangga",
  "notes": "Catatan baru.",
  "targets": [
    {
      "region_type": "Provinsi",
      "region_name": "Jawa Timur",
      "target_sample": 900
    }
  ]
}
```

Rules:

- Semua field optional.
- Jika `targets` tidak dikirim, targets lama tidak berubah.
- Jika `targets` dikirim, daftar target lama diganti penuh.
- Replacement harus menghapus target lama yang tidak dikirim lagi.
- Tidak boleh menghasilkan orphan Sampling Target.

### 5.3 Update Sample Group Status

```json
{
  "status": "Ready"
}
```

Rules:

- Status action MVP hanya menerima `Ready`.
- Transisi final hanya `Draft -> Ready`.

### 5.4 Create Sampling Target

```json
{
  "region_type": "Provinsi",
  "region_name": "Jawa Barat",
  "target_sample": 800
}
```

### 5.5 Update Sampling Target

```json
{
  "region_type": "Kabupaten/Kota",
  "region_name": "Bandung",
  "target_sample": 120
}
```

## 6. Final Response Schema

### 6.1 Sample Group Detail Response

Semua create/update/status/target mutation mengembalikan Sample Group detail terbaru, kecuali delete Sample Group.

```json
{
  "id": "uuid",
  "project_id": "uuid",
  "questionnaire_id": "uuid atau null",
  "sample_group_name": "Rumah Tangga",
  "target_respondent": "Rumah Tangga",
  "total_target_sample": 2350,
  "status": "Draft",
  "notes": "Target berdasarkan proposal STKU.",
  "sort_order": 1,
  "ready_at": null,
  "created_at": "2026-07-26T10:00:00",
  "updated_at": "2026-07-26T10:00:00",
  "project": {
    "id": "uuid",
    "project_number": "PRJ-0001",
    "project_name": "STKU 2026",
    "status": "Setup"
  },
  "questionnaire": {
    "id": "uuid",
    "questionnaire_name": "Questionnaire Rumah Tangga",
    "target_respondent": "Rumah Tangga",
    "status": "Ready"
  },
  "targets": [
    {
      "id": "uuid",
      "sample_group_id": "uuid",
      "region_type": "Provinsi",
      "region_name": "Jawa Barat",
      "target_sample": 800,
      "sort_order": 1,
      "created_at": "2026-07-26T10:00:00",
      "updated_at": "2026-07-26T10:00:00"
    }
  ]
}
```

### 6.2 List Sample Group Response

```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "questionnaire_id": "uuid atau null",
    "sample_group_name": "Rumah Tangga",
    "target_respondent": "Rumah Tangga",
    "total_target_sample": 2350,
    "status": "Draft",
    "notes": null,
    "sort_order": 1,
    "ready_at": null,
    "created_at": "2026-07-26T10:00:00",
    "updated_at": "2026-07-26T10:00:00",
    "project": {
      "id": "uuid",
      "project_number": "PRJ-0001",
      "project_name": "STKU 2026",
      "status": "Setup"
    },
    "questionnaire": null,
    "targets": []
  }
]
```

Freeze decision:

- List response boleh mengembalikan targets penuh untuk MVP.
- Lightweight list response menjadi future optimization, bukan blocker.

### 6.3 Delete Sample Group Response

```text
204 No Content
```

### 6.4 Delete Sampling Target Response

Delete Sampling Target mengembalikan Sample Group detail terbaru.

```text
200 OK
```

Alasan:

Frontend membutuhkan total target terbaru setelah satu target dihapus.

## 7. Final Business Rule

Business rules final:

1. Sampling Plan adalah target sampling, bukan database responden.
2. Sample Group wajib berada di bawah Project.
3. Sampling Target wajib berada di bawah Sample Group.
4. Project harus valid.
5. Project dengan status `Completed` atau `Cancelled` tidak dapat mengubah Sampling Plan.
6. Questionnaire optional saat Draft.
7. Jika `questionnaire_id` diisi, Questionnaire wajib berada pada Project yang sama.
8. Satu Questionnaire dapat digunakan oleh banyak Sample Group.
9. Satu Sample Group dapat menggunakan satu Questionnaire.
10. Sample Group status awal otomatis `Draft`.
11. Sample Group Draft dapat diedit.
12. Sample Group Ready tidak dapat diedit pada MVP.
13. Sample Group Draft dapat dihapus.
14. Sample Group Ready tidak dapat dihapus.
15. Delete Sampling Target terakhir tidak diperbolehkan.
16. PATCH Sample Group dengan field `targets` berarti full replacement.
17. Full replacement harus menghapus target lama yang tidak dikirim.
18. Tidak boleh ada orphan Sampling Target.
19. Backend wajib menghitung ulang `total_target_sample`.
20. Status flow MVP hanya `Draft -> Ready`.
21. Ready membutuhkan minimal satu Sampling Target.
22. Ready membutuhkan total target sample lebih dari 0.
23. Questionnaire belum wajib untuk Ready pada Sprint 8.2.
24. Questionnaire menjadi wajib sebelum Fieldwork pada sprint berikutnya jika Product Owner menetapkan.

## 8. Final Validation Rule

| Field | Rule | Status Jika Gagal |
| --- | --- | --- |
| `project_id` | Project harus ada | 404 |
| `sample_group_id` | Sample Group harus ada | 404 |
| `target_id` | Sampling Target harus ada | 404 |
| `questionnaire_id` | Jika diisi, harus milik Project yang sama | 400 |
| `sample_group_name` | Required, 2-200 karakter | 422 |
| `target_respondent` | Optional, maksimal 150 karakter | 422 |
| `notes` | Optional, maksimal 1000 karakter | 422 |
| `targets` pada create | Minimal satu target | 422 |
| `targets` pada PATCH jika dikirim | Minimal satu target | 422 |
| `region_type` | Required, 2-80 karakter | 422 |
| `region_name` | Required, 2-150 karakter | 422 |
| `target_sample` | Integer lebih dari 0 | 422 |
| `status` | Hanya `Ready` untuk action MVP | 400 |

## 9. Final Error Response

MVP menggunakan error response FastAPI yang sudah konsisten dengan backend saat ini:

```json
{
  "detail": "Pesan error"
}
```

Contoh:

```json
{
  "detail": "Project not found"
}
```

```json
{
  "detail": "Questionnaire must belong to the same project"
}
```

```json
{
  "detail": "Ready sample group cannot be edited"
}
```

```json
{
  "detail": "Sample group must have at least one sampling target"
}
```

Future technical debt:

Standard error object dengan:

- `code`
- `message`
- `fields`

Tidak menjadi blocker Sprint 8.2.

## 10. Final Status Code

| Status Code | Penggunaan |
| --- | --- |
| 200 OK | Read, update, status action, delete target berhasil |
| 201 Created | Create Sample Group atau Sampling Target berhasil |
| 204 No Content | Delete Sample Group berhasil |
| 400 Bad Request | Business rule violation |
| 401 Unauthorized | User belum login |
| 403 Forbidden | Future project-level permission |
| 404 Not Found | Resource tidak ditemukan |
| 422 Unprocessable Entity | Validation error |
| 500 Internal Server Error | Unexpected error |

## 11. Final Authorization Rule

Authorization MVP:

```text
Authenticated user
```

Final rule:

1. Semua endpoint Sampling Plan wajib membutuhkan user login.
2. Project-level permission belum diterapkan pada Sprint 8.2.
3. Future permission harus mengikuti akses Project.

Future permission matrix:

| Endpoint | Future Permission |
| --- | --- |
| GET list | `sampling_plan:read` |
| POST Sample Group | `sampling_plan:create` |
| GET detail | `sampling_plan:read` |
| PATCH Sample Group | `sampling_plan:update` |
| DELETE Sample Group | `sampling_plan:delete` |
| PATCH status | `sampling_plan:mark_ready` |
| POST Target | `sampling_plan:update` |
| PATCH Target | `sampling_plan:update` |
| DELETE Target | `sampling_plan:update` |

Technical debt:

Permission granular belum tersedia.

Tidak menjadi blocker Sprint 8.2.

## 12. Final Activity Logging

Activity logging final:

| Endpoint | Activity |
| --- | --- |
| GET list | Tidak ada |
| POST Sample Group | Sampling Plan dibuat |
| GET detail | Tidak ada |
| PATCH Sample Group | Sampling Plan diperbarui |
| DELETE Sample Group | Sampling Plan dihapus |
| PATCH status Ready | Sampling Plan ditandai Ready |
| POST Sampling Target | Sampling Plan diperbarui |
| PATCH Sampling Target | Sampling Plan diperbarui |
| DELETE Sampling Target | Sampling Plan diperbarui |

Activity metadata:

```text
activity_type = "SamplingPlan"
source_type = "SamplingPlan"
source_id = sample_group.id
```

Rules:

- Activity dicatat dari backend service.
- Activity target-level tetap diringkas sebagai `Sampling Plan diperbarui`.
- Tidak perlu activity per wilayah agar timeline tidak terlalu ramai.
- Activity delete Sample Group dicatat sebelum Sample Group dihapus.

## 13. Final Pattern Support

### 13.1 Pattern A

Banyak Questionnaire dan banyak Sample Group.

```text
Questionnaire Rumah Tangga -> Sample Group Rumah Tangga
Questionnaire UMKM -> Sample Group UMKM
```

Status:
Supported.

Reason:

- Setiap Sample Group memiliki `questionnaire_id` sendiri.
- Tidak ada unique constraint pada `questionnaire_id`.

### 13.2 Pattern B

Satu Questionnaire digunakan banyak Sample Group.

```text
Questionnaire Kepuasan
  -> Sample Group Mitra
  -> Sample Group Non Mitra
```

Status:
Supported.

Reason:

- Banyak Sample Group dapat mereferensikan Questionnaire yang sama.

## 14. Final Out of Scope

Tidak termasuk Sprint 8.2:

- Frontend.
- Import Excel.
- Export Excel.
- Sample Database.
- Respondent individual.
- Sample Frame.
- Enumerator.
- Fieldwork.
- QC.
- Dashboard.
- Monitoring.
- KoBo sync.
- Random sampling.
- Quota matrix kompleks.
- Weighting.
- Project-level permission implementation.
- Standard error object.

## 15. Final Acceptance Criteria

Sprint 8.2 implementation dinyatakan selesai jika:

1. Endpoint list Sample Group per Project tersedia.
2. Endpoint create Sample Group tersedia.
3. Endpoint get Sample Group detail tersedia.
4. Endpoint update Sample Group Draft tersedia.
5. Endpoint delete Sample Group Draft tersedia.
6. Endpoint status `Draft -> Ready` tersedia.
7. Endpoint create Sampling Target tersedia.
8. Endpoint update Sampling Target tersedia.
9. Endpoint delete Sampling Target tersedia.
10. Delete Sample Group hanya dapat dilakukan pada status Draft.
11. Delete Sampling Target terakhir ditolak.
12. PATCH Sample Group dengan `targets` melakukan full replacement.
13. Replacement targets tidak menghasilkan orphan record.
14. Backend menghitung ulang `total_target_sample`.
15. Activity logging berjalan untuk mutation event.
16. Pattern A lulus test.
17. Pattern B lulus test.
18. Validation error lulus test.
19. Not found error lulus test.
20. Authorization login diterapkan.
21. API test lulus.
22. Regression Project dan Questionnaire tetap lulus.
23. Tidak ada database responden yang dibuat.
24. Tidak ada frontend yang diimplementasikan.

## 16. Open Decision Review

Open decision dari dokumen sebelumnya sudah ditutup:

| Open Decision | Final Decision | Blocker |
| --- | --- | --- |
| Endpoint target eksplisit wajib atau tidak | Wajib masuk Sprint 8.2 | Tidak |
| Delete Sample Group Draft wajib atau tidak | Wajib masuk Sprint 8.2 | Tidak |
| Delete target terakhir boleh atau tidak | Tidak boleh | Tidak |
| Filter query list wajib atau tidak | Ditunda, frontend-side dulu | Tidak |
| Error message Bahasa Indonesia atau Inggris | Ikuti backend saat ini, UI tetap Bahasa Indonesia | Tidak |

Tidak ada open decision yang menjadi blocker.

## 17. Technical Debt

Technical debt yang dicatat:

| ID | Technical Debt | Priority |
| --- | --- | --- |
| TD-SAMPLING-API-001 | Error response belum standardized | Low |
| TD-SAMPLING-API-002 | Permission masih authenticated user | Medium |
| TD-SAMPLING-API-003 | Response list bisa berat jika target banyak | Low |
| TD-SAMPLING-API-004 | Filter list belum masuk API MVP | Low |
| TD-SAMPLING-API-005 | Alembic migration framework belum tersedia | Medium |

Tidak ada technical debt yang menjadi blocker Sprint 8.2.

## 18. Risiko Implementasi

### Risiko 1 - Frontend salah memahami full replacement targets

Severity:
Medium

Mitigation:

- Dokumentasikan dengan jelas.
- Gunakan endpoint target eksplisit untuk perubahan per wilayah.

### Risiko 2 - Delete menghapus data penting

Severity:
Medium

Mitigation:

- Delete Sample Group hanya untuk Draft.
- Ready tidak dapat dihapus.
- Activity delete dicatat.

### Risiko 3 - Total target tidak sinkron

Severity:
Medium

Mitigation:

- Backend selalu menghitung ulang total.
- Tambahkan API test untuk create, update, add target, update target, delete target.

### Risiko 4 - Authorization MVP terlalu longgar

Severity:
Medium

Mitigation:

- Diterima untuk MVP.
- Catat project-level permission sebagai technical debt.

## 19. Recommendation for Implementation

Rekomendasi implementasi:

1. Implementasikan route `sample_groups`.
2. Gunakan service layer Sprint 8.1.
3. Tambahkan service delete Sample Group Draft.
4. Tambahkan service create/update/delete Sampling Target.
5. Tambahkan tests untuk setiap endpoint.
6. Tambahkan tests Pattern A dan Pattern B.
7. Tambahkan tests delete target terakhir.
8. Jangan implement frontend pada Sprint 8.2.
9. Jangan menambahkan database responden.

## 20. Final Decision

```text
READY FOR IMPLEMENTATION
```

Sprint 8.2 API Layer siap masuk tahap implementasi setelah Product Owner memberikan persetujuan untuk mulai coding.
