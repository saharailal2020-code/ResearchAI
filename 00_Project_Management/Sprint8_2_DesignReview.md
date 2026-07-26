# Sprint 8.2 Design Review

Nama Review:
Product Owner Design Review - Sampling Plan API Layer

Status:
READY FOR DESIGN FREEZE

Tanggal:
26 Juli 2026

Dokumen yang direview:

- `Sprint8_Design_Freeze.md`
- `Sprint8_2_Planning.md`
- `SamplingPlan_API_Design.md`
- `ADR-006_Revision.md`
- `Domain_Model_v3.md`

## 1. Executive Summary

Rancangan API Sprint 8.2 sudah sesuai dengan Design Freeze Sampling Plan.

API sudah mendukung:

- CRUD Sample Group.
- CRUD Sampling Target.
- Status action `Draft -> Ready`.
- Pattern A: banyak Questionnaire dan banyak Sample Group.
- Pattern B: satu Questionnaire digunakan oleh banyak Sample Group.

Tidak ditemukan endpoint yang melanggar domain model, business rule, atau out of scope MVP.

Catatan utama:

Endpoint Sampling Target eksplisit menambah fleksibilitas untuk frontend, tetapi perlu keputusan freeze yang tegas agar implementasi tidak bercabang terlalu banyak.

Keputusan review:

```text
READY FOR DESIGN FREEZE
```

## 2. Compliance terhadap Design Freeze

### 2.1 Nama Domain

Compliant.

Desain tetap menggunakan:

```text
Sampling Plan
```

Sebagai nama domain/section bisnis.

Resource API tetap menggunakan:

```text
sample-groups
sampling-targets
```

Ini sesuai keputusan Design Freeze:

```text
Sampling Plan adalah nama domain/section.
Sample Group adalah resource API utama.
```

### 2.2 Entity

Compliant.

Entity yang digunakan:

- Sample Group.
- Sampling Target.

Tidak ada entity baru seperti:

- Respondent.
- Sample Database.
- Sample Frame.
- Fieldwork.
- QC.
- Dashboard.

### 2.3 Relationship

Compliant.

Relationship tetap:

```text
Project 1 -> many SampleGroup
Questionnaire 1 -> many SampleGroup
SampleGroup 1 -> many SamplingTarget
```

Tidak ada indikasi relasi Questionnaire dibuat 1:1.

### 2.4 Status Flow

Compliant.

Status flow tetap:

```text
Draft -> Ready
```

Tidak ada status baru seperti Cancelled, Archived, atau In Progress.

### 2.5 Out of Scope

Compliant.

Rancangan API tidak memasukkan:

- Import Excel.
- Export Excel.
- Database responden.
- Enumerator.
- Fieldwork.
- QC.
- Dashboard.

## 3. Review Endpoint Completeness

Endpoint yang dirancang:

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

Review:

- Endpoint sudah lengkap untuk CRUD Sample Group.
- Endpoint sudah lengkap untuk CRUD Sampling Target.
- Endpoint status action sudah tersedia.
- Endpoint list berada di bawah Project, sesuai Project sebagai root operasional.
- Endpoint detail/update/delete memakai resource id langsung, masih sesuai REST best practice.

Kesimpulan:

Endpoint lengkap.

## 4. Review REST API Best Practice

### Yang sudah baik

1. Collection endpoint memakai plural noun:

```text
/sample-groups
/sampling-targets
```

2. Nested collection digunakan saat konteks parent penting:

```text
/projects/{project_id}/sample-groups
/sample-groups/{sample_group_id}/targets
```

3. Resource detail memakai id langsung:

```text
/sample-groups/{sample_group_id}
/sampling-targets/{target_id}
```

4. Status action dipisahkan:

```text
/sample-groups/{sample_group_id}/status
```

Ini baik karena status bukan diedit bebas melalui form.

### Catatan

`PATCH /sample-groups/{id}/status` tetap acceptable untuk MVP.

Future option:

```text
POST /sample-groups/{id}/mark-ready
```

Namun untuk konsistensi dengan pola status API sebelumnya, endpoint `/status` dapat dipertahankan.

## 5. Review URI Endpoint

URI sudah jelas dan tidak membingungkan frontend.

Keputusan review:

1. List dan create Sample Group tetap di bawah Project:

```text
GET /projects/{project_id}/sample-groups
POST /projects/{project_id}/sample-groups
```

2. Detail/update/delete Sample Group memakai id:

```text
GET /sample-groups/{sample_group_id}
PATCH /sample-groups/{sample_group_id}
DELETE /sample-groups/{sample_group_id}
```

3. Target create berada di bawah Sample Group:

```text
POST /sample-groups/{sample_group_id}/targets
```

4. Target update/delete memakai id target:

```text
PATCH /sampling-targets/{target_id}
DELETE /sampling-targets/{target_id}
```

Kesimpulan:

URI endpoint siap digunakan.

## 6. Review HTTP Method

HTTP method sudah tepat:

| Action | Method | Review |
| --- | --- | --- |
| List | GET | Tepat |
| Detail | GET | Tepat |
| Create | POST | Tepat |
| Partial Update | PATCH | Tepat |
| Delete | DELETE | Tepat |
| Status Action | PATCH | Acceptable untuk MVP |

Tidak ditemukan penggunaan method yang keliru.

## 7. Review Request Schema

### Sample Group Create

Request sudah cukup:

- `questionnaire_id`
- `sample_group_name`
- `target_respondent`
- `notes`
- `targets`

Review:

- Tidak menerima `total_target_sample`, ini benar.
- Tidak menerima `status`, ini benar karena status otomatis Draft.
- Tidak menerima `created_by`, ini benar karena diambil dari user login.
- Tidak menerima data responden individual.

### Sample Group Update

Schema update bersifat partial.

Review:

- Cocok untuk edit Draft.
- Inline `targets` sebagai replacement penuh sudah jelas.
- Perlu dicatat kuat di implementasi agar frontend tidak salah mengirim partial targets.

### Sampling Target Create/Update

Schema sudah minimal:

- `region_type`
- `region_name`
- `target_sample`

Review:

- Cukup untuk MVP.
- Tidak perlu field wilayah administratif yang lebih kompleks pada sprint ini.

## 8. Review Response Schema

Response Sample Group detail sudah baik karena mengembalikan:

- Identitas Sample Group.
- Project summary.
- Questionnaire summary.
- Target wilayah.
- Status dan timestamp.

Kelebihan:

- Frontend bisa menampilkan detail tanpa perlu banyak request tambahan.
- Total target langsung tersedia.
- Pattern A dan Pattern B terlihat dari `questionnaire_id`.

Catatan:

Response list saat ini dirancang bisa mengembalikan targets penuh.

Risiko:

- Jika target wilayah sangat banyak, list Project Detail bisa berat.

Rekomendasi freeze:

- Untuk Sprint 8.2, response list boleh tetap memakai detail penuh agar cepat dibangun.
- Future optimization: buat `SampleGroupListItem` tanpa targets penuh jika performa mulai terasa.

## 9. Review Business Rule

Business rule sudah konsisten:

1. Project harus valid.
2. Project Completed/Cancelled tidak dapat mengubah Sampling Plan.
3. Questionnaire optional saat Draft.
4. Questionnaire harus berasal dari Project yang sama.
5. Sample Group Draft dapat diedit.
6. Sample Group Ready tidak dapat diedit.
7. Sample Group Draft dapat dihapus.
8. Sample Group Ready tidak dapat dihapus.
9. Total target dihitung backend.
10. Draft hanya dapat berubah ke Ready.

Tidak ada business rule yang bertentangan dengan Design Freeze.

## 10. Review Validation

Validation sudah cukup untuk MVP:

- `sample_group_name` required.
- `region_type` required.
- `region_name` required.
- `target_sample > 0`.
- `questionnaire_id` harus valid dan satu Project.
- `targets` minimal satu pada create/update inline.

Catatan:

Untuk endpoint delete individual Sampling Target, perlu keputusan eksplisit:

```text
Tidak boleh menghapus target terakhir.
```

Alasan:

- Konsisten dengan rule Sample Group harus memiliki minimal satu target.
- Mencegah Sample Group Draft menjadi kosong secara tidak sengaja.

Keputusan review:

Delete target terakhir harus return `400 Bad Request`.

## 11. Review Status Code

Status code sudah sesuai:

- `200 OK` untuk read/update/action.
- `201 Created` untuk create.
- `204 No Content` untuk delete Sample Group.
- `400 Bad Request` untuk pelanggaran business rule.
- `401 Unauthorized` untuk belum login.
- `403 Forbidden` sebagai future permission.
- `404 Not Found` untuk resource tidak ditemukan.
- `422 Unprocessable Entity` untuk validation error.

Catatan:

Untuk `DELETE /sampling-targets/{target_id}`, response `200 OK` dengan Sample Group detail terbaru dapat diterima karena frontend butuh total terbaru.

## 12. Review Error Response

Error response masih menggunakan struktur FastAPI:

```json
{
  "detail": "Pesan error"
}
```

Review:

- Konsisten dengan backend yang sudah berjalan.
- Cukup untuk MVP.

Improvement future:

- Standard error object dengan `code`, `message`, dan `fields`.

Tidak menjadi blocker Sprint 8.2.

## 13. Review Activity Logging

Activity logging sudah sesuai prinsip cross-cutting behavior ResearchAI.

Event:

- Sampling Plan dibuat.
- Sampling Plan diperbarui.
- Sampling Plan ditandai Ready.
- Sampling Plan dihapus.

Review:

- Activity dicatat pada event bisnis bermakna.
- Perubahan target wilayah tidak dicatat per baris, tetapi sebagai `Sampling Plan diperbarui`.
- Ini mencegah timeline terlalu ramai.

Catatan:

Design Freeze awal hanya menyebut 3 event:

- dibuat.
- diperbarui.
- ditandai Ready.

Event `Sampling Plan dihapus` adalah tambahan karena Sprint 8.2 merancang delete Sample Group Draft.

Keputusan review:

Event delete dapat diterima karena endpoint delete masuk CRUD Sample Group dan tetap business event penting.

## 14. Review Authorization

Authorization MVP:

```text
Authenticated user
```

Review:

- Sesuai kondisi MVP karena permission granular belum menjadi modul aktif.
- Rancangan sudah menyiapkan future permission.

Risiko:

- Semua user login bisa mengubah Sampling Plan jika belum ada project-level access control.

Mitigation:

- Catat sebagai technical debt/future backlog.
- Saat permission module tersedia, endpoint Sampling Plan harus mengikuti akses Project.

## 15. Support Pattern A dan Pattern B

### Pattern A

Supported.

Karena:

- Setiap Sample Group dapat membawa `questionnaire_id` berbeda.
- API tidak memaksa satu Questionnaire untuk satu Project saja.

### Pattern B

Supported.

Karena:

- Banyak Sample Group dapat menggunakan `questionnaire_id` yang sama.
- API tidak membuat unique constraint di level `questionnaire_id`.

Kesimpulan:

Pattern A dan Pattern B aman.

## 16. Endpoint yang Berpotensi Menyulitkan Frontend

### 16.1 Inline targets pada PATCH Sample Group

Risiko:

Jika frontend hanya ingin mengubah satu wilayah, frontend perlu mengirim seluruh daftar targets agar tidak terhapus.

Mitigation:

- Endpoint target eksplisit tetap diimplementasikan.
- Dokumentasikan bahwa `targets` pada PATCH Sample Group berarti replacement penuh.

### 16.2 Response list dengan targets penuh

Risiko:

Project dengan banyak wilayah dapat membuat response list besar.

Mitigation:

- Untuk MVP boleh diterima.
- Future optimization: list response tanpa targets penuh.

### 16.3 Delete target terakhir

Risiko:

Jika diizinkan, Sample Group bisa kosong dan bertentangan dengan validation create.

Mitigation:

- Freeze rule: delete target terakhir tidak diizinkan.

## 17. Temuan

### Temuan 1 - Open decision perlu ditutup sebelum implementasi

Severity:
Medium

Dokumen API Design masih memiliki beberapa open decisions.

Keputusan review:

1. Endpoint target eksplisit masuk Sprint 8.2.
2. Delete Sample Group Draft masuk Sprint 8.2.
3. Delete target terakhir tidak diizinkan.
4. Filter query pada list ditunda, kecuali implementasinya sangat ringan.
5. Error message boleh mengikuti gaya backend saat ini, tetapi rekomendasi label UI tetap Bahasa Indonesia di frontend.

### Temuan 2 - Activity delete belum ada di Design Freeze awal

Severity:
Low

Keputusan review:

Activity delete diterima karena delete endpoint masuk scope CRUD dan merupakan event bisnis penting.

### Temuan 3 - Permission granular belum tersedia

Severity:
Medium

Keputusan review:

Tidak blocker. MVP memakai authenticated user, future mengikuti permission Project.

## 18. Improvement

Improvement sebelum implementation freeze:

1. Tegaskan bahwa endpoint target eksplisit masuk Sprint 8.2.
2. Tegaskan delete target terakhir tidak boleh.
3. Tegaskan `targets` pada PATCH Sample Group adalah full replacement.
4. Gunakan response Sample Group detail setelah create/update/status/target changes agar frontend mudah refresh UI.
5. Tambahkan API test untuk Pattern A dan Pattern B.
6. Tambahkan API test untuk delete target terakhir.

Improvement future:

1. Standard error object.
2. Project-level permission.
3. Lightweight list response.
4. Pagination jika jumlah Sample Group/target besar.
5. Import/Export Excel.

## 19. Technical Debt

| ID | Debt | Priority | Catatan |
| --- | --- | --- | --- |
| TD-SAMPLING-API-001 | Error response belum standardized | Low | FastAPI detail masih cukup untuk MVP |
| TD-SAMPLING-API-002 | Permission masih authenticated user | Medium | Perlu project-level permission di phase berikutnya |
| TD-SAMPLING-API-003 | Response list bisa berat jika targets banyak | Low | Optimasi setelah kebutuhan performa nyata |
| TD-SAMPLING-API-004 | Filter list belum difreeze sebagai wajib | Low | Bisa dilakukan frontend-side dulu |
| TD-SAMPLING-API-005 | Alembic migration framework belum tersedia | Medium | Sudah masuk technical backlog sebelumnya |

## 20. Risiko

### Risiko 1 - Frontend salah memahami replacement targets

Severity:
Medium

Mitigation:

- API documentation harus jelas.
- Gunakan endpoint target eksplisit untuk edit baris wilayah.

### Risiko 2 - Authorization terlalu longgar

Severity:
Medium

Mitigation:

- Untuk MVP diterima.
- Tambahkan backlog permission project-level.

### Risiko 3 - Delete endpoint menghapus data penting

Severity:
Medium

Mitigation:

- Hanya Draft yang bisa dihapus.
- Ready tidak bisa dihapus.
- Activity delete dicatat.

### Risiko 4 - Total target tidak sinkron

Severity:
Medium

Mitigation:

- Backend selalu hitung ulang total.
- Tambahkan test create, update, target add, target edit, target delete.

## 21. Rekomendasi

Rekomendasi untuk Design Freeze Sprint 8.2:

1. Gunakan endpoint Sample Group dan Sampling Target seperti rancangan.
2. Implementasikan endpoint target eksplisit di Sprint 8.2 agar CRUD Sampling Target benar-benar lengkap.
3. Pertahankan inline `targets` pada create/update Sample Group, tetapi dokumentasikan sebagai full replacement.
4. Delete Sample Group hanya untuk status Draft.
5. Delete Sampling Target terakhir tidak boleh.
6. Semua mutation endpoint harus menjalankan activity logging.
7. Semua mutation endpoint harus menghitung ulang `total_target_sample`.
8. API tests wajib mencakup Pattern A dan Pattern B.
9. Jangan menambahkan import/export Excel.
10. Jangan membuat database responden.

## 22. Final Decision

```text
READY FOR DESIGN FREEZE
```

Tidak ada blocker desain yang harus diperbaiki sebelum Sprint 8.2 masuk tahap Design Freeze.
