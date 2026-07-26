# ADR-005 Multiple Questionnaire per Project

Status:
Proposed for Product Owner Review

Tanggal:
26 Juli 2026

Milestone:
M3 - Research Preparation

## 1. Tujuan

Mendefinisikan keputusan arsitektur bahwa satu Project ResearchAI dapat memiliki lebih dari satu Questionnaire.

Keputusan ini menggantikan keputusan sebelumnya yang membatasi satu Project hanya memiliki satu Questionnaire pada MVP.

## 2. Latar Belakang

Pada proses bisnis Beerka, satu Project dapat memiliki beberapa instrumen survey yang berbeda untuk kelompok responden atau unit observasi yang berbeda.

Contoh:

```text
Project STKU 2026
  |
  +-- Questionnaire Rumah Tangga
  +-- Questionnaire UMKM
  +-- Questionnaire Bank Pengelola Kas Titipan
  +-- Questionnaire Bank Peserta
```

Semua Questionnaire tersebut berada di bawah satu Project yang sama, tetapi masing-masing memiliki target responden, instrumen, KoBo link, XLSForm link, dan status kesiapan sendiri.

## 3. Keputusan Arsitektur

1. Relasi Project ke Questionnaire adalah one-to-many.
2. Satu Project dapat memiliki banyak Questionnaire.
3. Questionnaire tetap merupakan operational object di bawah Project.
4. Questionnaire bukan attachment biasa.
5. Questionnaire bukan Sample dan bukan Fieldwork.
6. Setiap Questionnaire memiliki status sendiri.
7. Setiap Questionnaire memiliki version number sendiri.
8. Setiap Questionnaire dapat memiliki KoBo Link dan XLSForm Link sendiri.
9. Project Detail harus menampilkan daftar Questionnaire.
10. Fieldwork readiness perlu mempertimbangkan kesiapan semua Questionnaire yang relevan.

## 4. Business Rules

### Project

1. Project dapat memiliki nol, satu, atau banyak Questionnaire.
2. Project status `Setup` dan `Ready` dapat membuat Questionnaire.
3. Project `Completed` tidak boleh membuat Questionnaire baru tanpa reopening atau special permission.
4. Project `Cancelled` tidak boleh membuat atau mengubah Questionnaire.

### Questionnaire

1. Questionnaire wajib memiliki Project.
2. Questionnaire wajib memiliki nama.
3. Questionnaire wajib memiliki target atau kelompok responden.
4. Status awal Questionnaire adalah `Draft`.
5. Status MVP:
   - Draft
   - Ready
6. Questionnaire Draft dapat diedit.
7. Questionnaire Ready tidak diedit langsung pada MVP.
8. Version number dimulai dari `1`.
9. KoBo Link optional.
10. XLSForm Link optional.
11. Activity dicatat saat Questionnaire dibuat, diperbarui, dan ditandai Ready.

### Fieldwork Readiness

Rule konseptual:

```text
Project dapat masuk Fieldwork jika seluruh Questionnaire wajib sudah Ready.
```

Exception:

- Research Type `Desk Research` tidak memerlukan Questionnaire.
- Exception lain harus ditentukan Product Owner pada sprint berikutnya.

## 5. Field Tambahan yang Direkomendasikan

Field tambahan untuk mendukung multiple questionnaire:

| Field | Tujuan | MVP |
| --- | --- | --- |
| `respondent_group` | Kelompok responden/unit observasi | Ya |
| `instrument_type` | Jenis instrumen survey | Ya |
| `sort_order` | Urutan tampilan pada Project Detail | Ya |
| `is_required` | Menentukan apakah wajib Ready sebelum Fieldwork | Optional |

Rekomendasi MVP:

- `respondent_group` wajib.
- `instrument_type` wajib dengan default `Quantitative Survey`.
- `sort_order` optional dengan default incremental.
- `is_required` dapat ditunda jika gate Fieldwork belum diimplementasikan.

## 6. Konsekuensi

### Konsekuensi Positif

- Lebih sesuai dengan proses bisnis Beerka.
- Mendukung project multi-responden seperti STKU.
- Sample dan Fieldwork bisa berkembang lebih natural.
- Setiap instrumen dapat memiliki KoBo/XLSForm masing-masing.
- Project Detail menjadi pusat preparation yang lebih realistis.

### Konsekuensi Negatif

- Scope Sprint 7 bertambah.
- UI Project Detail perlu menampilkan daftar Questionnaire.
- Endpoint singular perlu direvisi.
- Constraint unik `project_id` pada questionnaires harus dihapus.
- Need migration strategy untuk data yang sudah dibuat di local development.

### Konsekuensi Netral

- Questionnaire Detail tetap dapat digunakan.
- Status Draft/Ready tetap digunakan.
- Version history penuh tetap out of scope.
- KoBo API tetap out of scope.

## 7. Backward Compatibility

Backward compatibility perlu dijaga karena implementasi Sprint 7 awal sudah memakai endpoint singular.

Rekomendasi:

- Endpoint baru menggunakan plural:

```text
GET /api/v1/projects/{project_id}/questionnaires
POST /api/v1/projects/{project_id}/questionnaires
```

- Endpoint singular lama dapat dipertahankan sementara:

```text
GET /api/v1/projects/{project_id}/questionnaire
POST /api/v1/projects/{project_id}/questionnaire
```

Perilaku endpoint singular:

- `GET` mengembalikan Questionnaire pertama berdasarkan `sort_order` atau `created_at`.
- `POST` tetap bisa membuat Questionnaire pertama jika belum ada, tetapi deprecated.
- Frontend baru harus memakai endpoint plural.

## 8. Future Consideration

Phase berikutnya dapat menambahkan:

- Questionnaire version history.
- Instrument templates.
- XLSForm upload dan parser.
- KoBoToolbox API integration.
- Readiness checklist per Questionnaire.
- Link Questionnaire ke Sample group.
- Link Questionnaire ke Fieldwork assignment.

## 9. Decision Owner

Product Owner, Product Architecture, dan Engineering.

## 10. Rekomendasi

Perubahan ini sebaiknya dilakukan sebagai Sprint 7.1 jika Product Owner ingin menjaga Sprint 7 review tetap bersih.

Namun secara teknis perubahan dapat dimasukkan ke Sprint 7 sebelum commit karena implementasi Sprint 7 belum di-commit.

Rekomendasi final:

```text
Lakukan sebagai Sprint 7 Revision / Sprint 7.1 sebelum commit Sprint 7.
```

Alasan:

- Business rule berubah fundamental.
- Perlu revisi database model, API, Project Detail UI, dan test.
- Lebih aman diperlakukan sebagai revision sprint yang eksplisit.
