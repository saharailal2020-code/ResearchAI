# Sampling Plan API Design

Status:
READY FOR DESIGN REVIEW

Tanggal:
26 Juli 2026

Domain:
Sampling Plan

Resource:
Sample Group dan Sampling Target

## 1. API Design Principles

Prinsip desain:

1. Project adalah root operasional.
2. Sample Group dibuat di bawah Project.
3. Sampling Target dibuat di bawah Sample Group.
4. Sampling Plan bukan database responden.
5. API tidak menyimpan individual respondent.
6. Backend menghitung `total_target_sample`.
7. Status tidak diedit bebas melalui form.
8. Perubahan status dilakukan melalui endpoint status action.
9. Activity logging dicatat dari backend service.
10. Endpoint harus mendukung Pattern A dan Pattern B.

## 2. Common Response Shape

### Sample Group Response

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

### Error Response

```json
{
  "detail": "Pesan error"
}
```

Rekomendasi future:

```json
{
  "error": {
    "code": "SAMPLING_TARGET_REQUIRED",
    "message": "Minimal satu target wilayah wajib diisi.",
    "fields": {
      "targets": "Minimal satu target wilayah wajib diisi."
    }
  }
}
```

Untuk MVP, struktur FastAPI `detail` masih diterima agar konsisten dengan API yang sudah berjalan.

## 3. Endpoint List Sample Group

### Endpoint

```text
GET /api/v1/projects/{project_id}/sample-groups
```

### Tujuan

Mengambil seluruh Sample Group milik Project.

### Authorization

Authenticated user.

### Query Parameters

MVP optional:

```text
status=Draft|Ready
questionnaire_id=uuid
search=text
```

Jika ingin menjaga scope ketat, filter dapat ditunda dan frontend melakukan filter sederhana dari response list.

### Response 200

```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "questionnaire_id": "uuid",
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
    "questionnaire": {
      "id": "uuid",
      "questionnaire_name": "Questionnaire Rumah Tangga",
      "target_respondent": "Rumah Tangga",
      "status": "Ready"
    },
    "targets": []
  }
]
```

### Business Rules

- Project harus ada.
- Jika Project tidak ditemukan, return 404.
- Response boleh empty array jika belum ada Sample Group.

### Status Codes

- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Activity Logging

Tidak ada activity untuk read operation.

## 4. Endpoint Create Sample Group

### Endpoint

```text
POST /api/v1/projects/{project_id}/sample-groups
```

### Tujuan

Membuat Sample Group Draft beserta Sampling Target awal.

### Authorization

Authenticated user.

Future:
Project Manager, Admin, atau user dengan permission `sampling_plan:create`.

### Request Body

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
    },
    {
      "region_type": "Provinsi",
      "region_name": "Jawa Tengah",
      "target_sample": 650
    }
  ]
}
```

### Response 201

Mengembalikan Sample Group detail.

### Business Rules

1. Project wajib ada.
2. Project tidak boleh `Completed` atau `Cancelled`.
3. Sample Group Name wajib.
4. Questionnaire optional saat Draft.
5. Jika `questionnaire_id` diisi, Questionnaire wajib milik Project yang sama.
6. Minimal satu Sampling Target wajib diisi.
7. `target_sample` harus lebih dari 0.
8. `total_target_sample` dihitung backend.
9. Status otomatis `Draft`.
10. `created_by` diisi dari user login.

### Validation

- `sample_group_name`: required, 2-200 karakter.
- `target_respondent`: optional, maksimal 150 karakter.
- `notes`: optional, maksimal 1000 karakter.
- `region_type`: required, 2-80 karakter.
- `region_name`: required, 2-150 karakter.
- `target_sample`: integer, lebih dari 0.

### Status Codes

- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `422 Unprocessable Entity`

### Error Examples

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
  "detail": "Target sample must be greater than 0"
}
```

### Activity Logging

Event:

```text
Sampling Plan dibuat
```

Description:

```text
Sample Group {sample_group_name} telah dibuat.
```

## 5. Endpoint Get Sample Group Detail

### Endpoint

```text
GET /api/v1/sample-groups/{sample_group_id}
```

### Tujuan

Mengambil detail Sample Group beserta Project, Questionnaire, dan Sampling Target.

### Authorization

Authenticated user.

### Response 200

Mengembalikan Sample Group detail.

### Business Rules

- Sample Group harus ada.
- Tidak mengubah data.

### Status Codes

- `200 OK`
- `401 Unauthorized`
- `404 Not Found`

### Activity Logging

Tidak ada activity untuk read operation.

## 6. Endpoint Update Sample Group Draft

### Endpoint

```text
PATCH /api/v1/sample-groups/{sample_group_id}
```

### Tujuan

Memperbarui Sample Group yang masih Draft.

### Authorization

Authenticated user.

Future:
Project Manager, Admin, atau user dengan permission `sampling_plan:update`.

### Request Body

Semua field optional, tetapi jika `targets` dikirim maka daftar target lama diganti penuh.

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

### Response 200

Mengembalikan Sample Group detail terbaru.

### Business Rules

1. Sample Group harus ada.
2. Project tidak boleh `Completed` atau `Cancelled`.
3. Hanya status `Draft` yang dapat diedit.
4. Jika `questionnaire_id` diisi, Questionnaire wajib milik Project yang sama.
5. Jika `targets` dikirim, maka replacement penuh dilakukan.
6. Target lama yang tidak dikirim lagi harus terhapus.
7. Tidak boleh ada orphan Sampling Target.
8. `total_target_sample` dihitung ulang backend.

### Status Codes

- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `422 Unprocessable Entity`

### Error Examples

```json
{
  "detail": "Ready sample group cannot be edited"
}
```

```json
{
  "detail": "At least one sampling target is required"
}
```

### Activity Logging

Event:

```text
Sampling Plan diperbarui
```

Description:

```text
Sample Group {sample_group_name} telah diperbarui.
```

## 7. Endpoint Delete Sample Group Draft

### Endpoint

```text
DELETE /api/v1/sample-groups/{sample_group_id}
```

### Tujuan

Menghapus Sample Group yang masih Draft.

### Authorization

Authenticated user.

Future:
Project Manager, Admin, atau user dengan permission `sampling_plan:delete`.

### Response 204

Tidak mengembalikan body.

### Business Rules

1. Sample Group harus ada.
2. Hanya Sample Group status `Draft` yang boleh dihapus.
3. Ready tidak boleh dihapus pada MVP.
4. Semua Sampling Target di bawah Sample Group ikut terhapus.
5. Tidak boleh ada orphan Sampling Target.

### Status Codes

- `204 No Content`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`

### Error Example

```json
{
  "detail": "Ready sample group cannot be deleted"
}
```

### Activity Logging

Event:

```text
Sampling Plan dihapus
```

Description:

```text
Sample Group {sample_group_name} telah dihapus.
```

Catatan:

Activity perlu dicatat sebelum row Sample Group dihapus, dengan `source_id` tetap memakai id Sample Group.

## 8. Endpoint Update Sample Group Status

### Endpoint

```text
PATCH /api/v1/sample-groups/{sample_group_id}/status
```

### Tujuan

Menjalankan status action dari `Draft` ke `Ready`.

### Authorization

Authenticated user.

Future:
Project Manager, Admin, atau user dengan permission `sampling_plan:mark_ready`.

### Request Body

```json
{
  "status": "Ready"
}
```

### Response 200

Mengembalikan Sample Group detail terbaru.

### Business Rules

1. Sample Group harus ada.
2. Project tidak boleh `Completed` atau `Cancelled`.
3. Status valid hanya `Draft` dan `Ready`.
4. Transisi MVP hanya `Draft -> Ready`.
5. `Ready -> Draft` tidak didukung.
6. Ready membutuhkan minimal satu Sampling Target.
7. Ready membutuhkan total target sample lebih dari 0.
8. Questionnaire masih optional pada Sprint 8.2 karena wajib Questionnaire baru diberlakukan sebelum Fieldwork.

### Status Codes

- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `422 Unprocessable Entity`

### Error Examples

```json
{
  "detail": "Only Draft to Ready transition is available in this sprint"
}
```

```json
{
  "detail": "Sample group must have at least one sampling target before Ready"
}
```

### Activity Logging

Event:

```text
Sampling Plan ditandai Ready
```

Description:

```text
Sample Group {sample_group_name} siap digunakan untuk Fieldwork.
```

## 9. Endpoint Create Sampling Target

### Endpoint

```text
POST /api/v1/sample-groups/{sample_group_id}/targets
```

### Tujuan

Menambahkan satu Sampling Target ke Sample Group Draft.

### Authorization

Authenticated user.

### Request Body

```json
{
  "region_type": "Provinsi",
  "region_name": "Jawa Barat",
  "target_sample": 800
}
```

### Response 201

Mengembalikan Sample Group detail terbaru.

### Business Rules

1. Sample Group harus ada.
2. Hanya Sample Group Draft yang bisa ditambah target.
3. Target sample harus lebih dari 0.
4. `total_target_sample` dihitung ulang.
5. `sort_order` target baru diisi otomatis.

### Status Codes

- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `422 Unprocessable Entity`

### Activity Logging

Event:

```text
Sampling Plan diperbarui
```

## 10. Endpoint Update Sampling Target

### Endpoint

```text
PATCH /api/v1/sampling-targets/{target_id}
```

### Tujuan

Memperbarui satu Sampling Target pada Sample Group Draft.

### Authorization

Authenticated user.

### Request Body

```json
{
  "region_type": "Kabupaten/Kota",
  "region_name": "Bandung",
  "target_sample": 120
}
```

### Response 200

Mengembalikan Sample Group detail terbaru.

### Business Rules

1. Sampling Target harus ada.
2. Parent Sample Group harus Draft.
3. Target sample harus lebih dari 0.
4. `total_target_sample` dihitung ulang.

### Status Codes

- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`
- `422 Unprocessable Entity`

### Activity Logging

Event:

```text
Sampling Plan diperbarui
```

## 11. Endpoint Delete Sampling Target

### Endpoint

```text
DELETE /api/v1/sampling-targets/{target_id}
```

### Tujuan

Menghapus satu Sampling Target dari Sample Group Draft.

### Authorization

Authenticated user.

### Response 200

Mengembalikan Sample Group detail terbaru.

Alasan bukan `204`:

Frontend perlu menerima ulang total target terbaru setelah target dihapus.

### Business Rules

1. Sampling Target harus ada.
2. Parent Sample Group harus Draft.
3. Target boleh dihapus.
4. Jika target terakhir dihapus, Sample Group tetap boleh Draft dengan total 0 hanya jika Product Owner menyetujui.
5. Rekomendasi MVP: jangan izinkan menghapus target terakhir melalui endpoint target eksplisit, agar rule "minimal satu target" tetap konsisten.
6. `total_target_sample` dihitung ulang.

### Status Codes

- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`

### Error Example

```json
{
  "detail": "Sample group must have at least one sampling target"
}
```

### Activity Logging

Event:

```text
Sampling Plan diperbarui
```

## 12. Validation Matrix

| Field | Rule | Error Status |
| --- | --- | --- |
| project_id | Project harus ada | 404 |
| questionnaire_id | Harus milik Project yang sama | 400 |
| sample_group_name | Required, 2-200 karakter | 422 |
| target_respondent | Optional, maksimal 150 karakter | 422 |
| notes | Optional, maksimal 1000 karakter | 422 |
| targets | Minimal satu saat create/update inline | 422 |
| region_type | Required, 2-80 karakter | 422 |
| region_name | Required, 2-150 karakter | 422 |
| target_sample | Integer > 0 | 422 |
| status | Hanya Draft/Ready | 400 |

## 13. Status Code Standard

| Status Code | Penggunaan |
| --- | --- |
| 200 | Read/update/status action berhasil |
| 201 | Create berhasil |
| 204 | Delete Sample Group berhasil |
| 400 | Business rule violation |
| 401 | Belum login |
| 403 | Tidak punya akses, future permission |
| 404 | Resource tidak ditemukan |
| 422 | Validation error |
| 500 | Unexpected server error |

## 14. Authorization Matrix

| Endpoint | MVP Authorization | Future Permission |
| --- | --- | --- |
| GET project sample groups | Authenticated user | `sampling_plan:read` |
| POST project sample groups | Authenticated user | `sampling_plan:create` |
| GET sample group detail | Authenticated user | `sampling_plan:read` |
| PATCH sample group | Authenticated user | `sampling_plan:update` |
| DELETE sample group | Authenticated user | `sampling_plan:delete` |
| PATCH sample group status | Authenticated user | `sampling_plan:mark_ready` |
| POST target | Authenticated user | `sampling_plan:update` |
| PATCH target | Authenticated user | `sampling_plan:update` |
| DELETE target | Authenticated user | `sampling_plan:update` |

## 15. Activity Logging Matrix

| Endpoint | Activity |
| --- | --- |
| GET list | Tidak ada |
| POST sample group | Sampling Plan dibuat |
| GET detail | Tidak ada |
| PATCH sample group | Sampling Plan diperbarui |
| DELETE sample group | Sampling Plan dihapus |
| PATCH status Ready | Sampling Plan ditandai Ready |
| POST target | Sampling Plan diperbarui |
| PATCH target | Sampling Plan diperbarui |
| DELETE target | Sampling Plan diperbarui |

## 16. API Support for Pattern A and Pattern B

### Pattern A

API mendukung banyak Questionnaire karena setiap Sample Group dapat membawa `questionnaire_id` berbeda.

No special endpoint needed.

### Pattern B

API mendukung satu Questionnaire digunakan banyak Sample Group karena tidak ada pembatasan unik pada `questionnaire_id`.

No special endpoint needed.

## 17. Open Decisions for Product Owner

1. Apakah endpoint target eksplisit wajib diimplementasikan di Sprint 8.2, atau cukup inline targets dulu?
2. Apakah delete Sample Group Draft wajib tersedia sejak API MVP?
3. Jika Sampling Target terakhir dihapus, apakah Sample Group Draft boleh menjadi kosong?
4. Apakah filter query pada list Sample Group perlu masuk API MVP, atau cukup frontend-side filtering?
5. Apakah error message langsung memakai Bahasa Indonesia, atau tetap Bahasa Inggris mengikuti backend saat ini?

## 18. Recommendation

Rekomendasi Product Architecture:

1. Implementasikan endpoint Sample Group utama pada Sprint 8.2.
2. Implementasikan delete Sample Group Draft agar CRUD Sample Group lengkap.
3. Untuk Sampling Target, pilih salah satu:
   - MVP sederhana: target dikelola inline lewat create/update Sample Group.
   - MVP lengkap sesuai request: tambah endpoint target eksplisit.
4. Jaga activity logging tetap pada event ringkas.
5. Tetap jangan membuat database responden.

## 19. Final Decision

```text
READY FOR DESIGN REVIEW
```
