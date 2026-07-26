# Sprint 8.2 Planning

Nama Sprint:
Sampling Plan API

Status:
READY FOR DESIGN REVIEW

Tanggal:
26 Juli 2026

## 1. Tujuan Sprint

Sprint 8.2 bertujuan merancang API untuk modul Sampling Plan berdasarkan Sprint 8.1 Backend Foundation.

API ini akan menjadi jembatan antara backend foundation dan frontend Sampling Plan pada sprint berikutnya.

Fokus API:

- Mengelola Sample Group di bawah Project.
- Mengelola Sampling Target di bawah Sample Group.
- Mendukung status flow `Draft -> Ready`.
- Menjaga relasi Project, Questionnaire, Sample Group, dan Sampling Target tetap konsisten.

## 2. Referensi

Dokumen acuan:

- `Sprint8_Design_Freeze.md`
- `Domain_Model_v3.md`
- `ADR-006_Revision.md`
- Implementasi Sprint 8.1 Backend Foundation

Catatan:

`Sprint8_1_Summary.md` belum ditemukan di folder project saat planning ini dibuat. Planning ini menggunakan hasil implementasi Sprint 8.1 yang sudah tersedia di backend sebagai referensi tambahan.

## 3. Scope Sprint 8.2

Scope API:

1. Endpoint list Sample Group per Project.
2. Endpoint create Sample Group.
3. Endpoint get Sample Group detail.
4. Endpoint update Sample Group Draft.
5. Endpoint delete Sample Group Draft.
6. Endpoint update status Sample Group dari Draft ke Ready.
7. Endpoint CRUD Sampling Target eksplisit untuk kebutuhan API.
8. Activity logging untuk event bisnis penting.
9. Authorization berbasis user login.
10. Error response yang konsisten.

## 4. Out of Scope

Tidak termasuk Sprint 8.2:

- Frontend.
- Import Excel.
- Export Excel.
- Sample Database.
- Enumerator.
- Fieldwork.
- QC.
- Dashboard.
- Respondent individual.
- Random sampling.
- Quota matrix kompleks.

## 5. Domain API Strategy

Nama domain UI tetap:

```text
Sampling Plan
```

Resource API utama:

```text
sample-groups
sampling-targets
```

Alasan:

- Sampling Plan adalah domain/section bisnis.
- Sample Group adalah resource utama yang benar-benar disimpan.
- Sampling Target adalah rincian target wilayah di bawah Sample Group.

## 6. Endpoint Summary

Endpoint utama:

```text
GET    /api/v1/projects/{project_id}/sample-groups
POST   /api/v1/projects/{project_id}/sample-groups
GET    /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}
DELETE /api/v1/sample-groups/{sample_group_id}
PATCH  /api/v1/sample-groups/{sample_group_id}/status
```

Endpoint Sampling Target eksplisit:

```text
POST   /api/v1/sample-groups/{sample_group_id}/targets
PATCH  /api/v1/sampling-targets/{target_id}
DELETE /api/v1/sampling-targets/{target_id}
```

Catatan desain:

- Create/update Sample Group tetap boleh menerima `targets` secara inline.
- Endpoint target eksplisit disiapkan agar API mendukung CRUD Sampling Target secara jelas.
- Jika frontend MVP lebih sederhana, frontend boleh menggunakan inline `targets` dulu.

## 7. Business Rules

Business rules final:

1. Sample Group wajib berada di bawah Project.
2. Project harus valid.
3. Project dengan status `Completed` atau `Cancelled` tidak boleh mengubah Sampling Plan.
4. Questionnaire optional saat Draft.
5. Jika Questionnaire dipilih, Questionnaire wajib berasal dari Project yang sama.
6. Satu Questionnaire boleh dipakai banyak Sample Group.
7. Sample Group wajib memiliki nama.
8. Sample Group Draft dapat diedit.
9. Sample Group Ready tidak dapat diedit pada MVP.
10. Sample Group Draft dapat dihapus.
11. Sample Group Ready tidak dapat dihapus pada MVP.
12. Sampling Target wajib memiliki region type, region name, dan target sample lebih dari 0.
13. Total target sample dihitung dari seluruh Sampling Target.
14. Status flow hanya `Draft -> Ready`.
15. Ready hanya bisa dilakukan jika Sample Group memiliki minimal satu Sampling Target dan total target lebih dari 0.

## 8. Pattern Support

### Pattern A

Banyak Questionnaire dan banyak Sample Group.

```text
Questionnaire Rumah Tangga -> Sample Group Rumah Tangga
Questionnaire UMKM -> Sample Group UMKM
```

Didukung karena:

- `questionnaire_id` berada di Sample Group.
- Tidak ada unique constraint pada `questionnaire_id`.

### Pattern B

Satu Questionnaire digunakan banyak Sample Group.

```text
Questionnaire Kepuasan -> Sample Group Mitra
Questionnaire Kepuasan -> Sample Group Non Mitra
```

Didukung karena:

- Banyak Sample Group dapat mereferensikan Questionnaire yang sama.

## 9. Authorization

Semua endpoint Sampling Plan membutuhkan user login.

Authorization MVP:

- Semua authenticated user yang dapat mengakses Project dapat membaca Sampling Plan.
- Semua authenticated user yang dapat mengelola Project dapat membuat dan mengubah Sampling Plan.

Role detail ditunda sampai modul permission dibuat.

Rekomendasi future:

- Admin: full access.
- Project Manager: full access pada project terkait.
- Research Executive: create/update Draft.
- Viewer: read only.

## 10. Activity Logging

Activity dicatat pada level event bisnis, bukan setiap perubahan kecil.

Event:

- `Sampling Plan dibuat`
- `Sampling Plan diperbarui`
- `Sampling Plan ditandai Ready`
- `Sampling Plan dihapus`

Activity source:

```text
source_type = "SamplingPlan"
source_id = sample_group.id
activity_type = "SamplingPlan"
```

Catatan:

- Tambah/update/delete Sampling Target dicatat sebagai `Sampling Plan diperbarui`.
- Tidak perlu activity per wilayah agar timeline tidak terlalu ramai.

## 11. Testing Plan

Backend API testing:

1. List Sample Group per Project.
2. Create Sample Group dengan target inline.
3. Get Sample Group detail.
4. Update Draft Sample Group.
5. Delete Draft Sample Group.
6. Mark Ready.
7. Reject edit Ready.
8. Reject delete Ready.
9. Reject Questionnaire dari Project lain.
10. Pattern A.
11. Pattern B.
12. Activity logging.
13. Validation error.
14. Not found error.

Regression:

- Login.
- Project Detail existing endpoint.
- Questionnaire existing endpoint.
- Client Activity Timeline.

## 12. Risiko

### Risiko 1 - API terlalu banyak variasi

Severity:
Medium

Mitigation:

- Jadikan Sample Group endpoint sebagai API utama.
- Endpoint Sampling Target eksplisit tetap sederhana.

### Risiko 2 - Data target tidak sinkron

Severity:
Medium

Mitigation:

- Backend selalu menghitung ulang `total_target_sample`.
- Jangan menerima `total_target_sample` dari frontend.

### Risiko 3 - Activity timeline terlalu ramai

Severity:
Low

Mitigation:

- Target-level changes dicatat sebagai satu event `Sampling Plan diperbarui`.

### Risiko 4 - Permission belum granular

Severity:
Medium

Mitigation:

- MVP gunakan authenticated user.
- Buat backlog permission granular setelah role system matang.

## 13. Acceptance Criteria

Sprint 8.2 Design dianggap selesai jika:

1. Semua endpoint REST API didefinisikan.
2. URI dan HTTP method jelas.
3. Request dan response body jelas.
4. Business rule per endpoint jelas.
5. Validation jelas.
6. Status code jelas.
7. Error response jelas.
8. Activity logging jelas.
9. Authorization jelas.
10. API mendukung CRUD Sample Group.
11. API mendukung CRUD Sampling Target.
12. API mendukung status `Draft -> Ready`.
13. API mendukung Pattern A.
14. API mendukung Pattern B.
15. Out of Scope tetap terjaga.

## 14. Recommendation

Rekomendasi implementasi Sprint 8.2:

1. Implementasikan route FastAPI untuk Sample Group terlebih dahulu.
2. Gunakan service layer Sprint 8.1.
3. Tambahkan service delete Sample Group Draft.
4. Tambahkan service CRUD Sampling Target eksplisit.
5. Tambahkan API tests sebelum browser/frontend sprint.
6. Jangan implement frontend pada Sprint 8.2.

## 15. Final Decision

```text
READY FOR DESIGN REVIEW
```
