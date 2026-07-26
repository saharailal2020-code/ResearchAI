# Sprint 8 Design Freeze

Nama Sprint:
Sampling Plan MVP

Status:
READY FOR IMPLEMENTATION

Tanggal:
26 Juli 2026

Basis Review:

- `ADR-006_Revision.md`
- `Domain_Model_v3.md`
- `Workflow_v3.md`
- `SamplingPlan_MVP.md`

## 1. Design Freeze Summary

Discovery Sprint 8 telah direvisi dan disetujui oleh Product Owner.

Hasil review menunjukkan bahwa desain domain sudah konsisten dan siap menjadi dasar implementasi Sprint 9 dan Sprint 10.

Keputusan utama:

```text
Nama modul final: Sampling Plan
Entity utama: Sample Group dan Sampling Target
```

Sampling Plan adalah target sampling yang disepakati dengan client.

Sampling Plan bukan database responden.

## 2. Review Konsistensi Dokumen

Hasil review:

- Tidak ditemukan kontradiksi utama antar dokumen.
- Semua dokumen sudah menggunakan istilah `Sampling Plan` sebagai domain utama.
- Semua dokumen memisahkan Sampling Plan dari database responden.
- Semua dokumen mendukung Pattern A dan Pattern B.
- Semua dokumen menyatakan bahwa database responden berada di luar scope MVP.

Catatan freeze:

Endpoint `GET /projects/{project_id}/sampling-plan` disebut sebagai opsi di `Workflow_v3.md`, tetapi untuk implementasi MVP endpoint utama yang dibekukan adalah endpoint `sample-groups`.

Keputusan:

```text
Sampling Plan adalah nama domain/section.
Sample Group adalah resource API utama.
```

## 3. Final Business Rule

1. Sampling Plan sudah ditentukan secara bisnis sejak Proposal dibuat.
2. Pada MVP, Sampling Plan dibuat setelah Proposal Approved menjadi Project.
3. Sampling Plan merepresentasikan target survei yang disepakati dengan client.
4. Sampling Plan bukan database responden.
5. Sampling Plan tidak menyimpan data individual respondent.
6. Satu Project memiliki satu Sampling Plan aktif pada MVP.
7. Satu Project dapat memiliki banyak Sample Group.
8. Satu Sample Group dapat memiliki banyak Sampling Target per wilayah.
9. Satu Sample Group dapat menggunakan satu Questionnaire.
10. Satu Questionnaire dapat digunakan oleh banyak Sample Group.
11. Questionnaire optional saat Draft.
12. Questionnaire direkomendasikan/wajib sebelum Fieldwork dimulai.
13. Import/Export Excel tidak masuk implementasi pertama.

## 4. Final Domain Model

Domain chain:

```text
Proposal
  -> Project
  -> Questionnaire
  -> Sampling Plan
  -> Fieldwork
  -> QC
  -> Dataset
```

MVP implementation model:

```text
Project
  -> Questionnaire
  -> Sample Group
       -> Sampling Target
```

Penjelasan:

- `Project` adalah root operasional.
- `Questionnaire` adalah instrumen survei.
- `Sampling Plan` adalah konsep bisnis rencana target sampling.
- `Sample Group` adalah kelompok target survei.
- `Sampling Target` adalah target sample per wilayah.

## 5. Final Entity

### 5.1 Sample Group

Entity utama untuk MVP.

Final fields:

- `id`
- `project_id`
- `questionnaire_id`
- `sample_group_name`
- `target_respondent`
- `total_target_sample`
- `status`
- `notes`
- `sort_order`
- `created_by`
- `ready_at`
- `created_at`
- `updated_at`

Notes:

- `questionnaire_id` nullable saat Draft.
- `target_respondent` optional tetapi direkomendasikan.
- `total_target_sample` dapat dihitung dari total Sampling Target.
- Jika disimpan di database, nilainya harus disinkronkan dengan total target wilayah.

### 5.2 Sampling Target

Entity rincian target wilayah.

Final fields:

- `id`
- `sample_group_id`
- `region_type`
- `region_name`
- `target_sample`
- `sort_order`
- `created_at`
- `updated_at`

### 5.3 Entity yang Tidak Dibuat pada MVP

- Respondent.
- Respondent Database.
- Sample Frame.
- Sample Quota Matrix.
- Sampling Plan table terpisah.

Keputusan:

Untuk MVP, table `sampling_plans` tidak dibuat dulu karena satu Project hanya memiliki satu Sampling Plan aktif dan dapat direpresentasikan melalui collection `sample_groups`.

## 6. Final Relationship

Final relationship:

```text
Project 1 -> many Questionnaire
Project 1 -> many SampleGroup
Questionnaire 1 -> many SampleGroup
SampleGroup 1 -> many SamplingTarget
```

Future relationship:

```text
SampleGroup 1 -> many FieldworkRecord
Fieldwork 1 -> many QCRecord
QC -> Dataset
```

Validation relationship:

- Sample Group harus berada di Project yang valid.
- Jika `questionnaire_id` diisi, Questionnaire harus berada pada Project yang sama.
- Sampling Target harus berada di bawah Sample Group yang valid.

## 7. Pattern Support

### Pattern A - Banyak Questionnaire dan Banyak Sample Group

Supported.

```text
Questionnaire Rumah Tangga -> Sample Group Rumah Tangga
Questionnaire UMKM -> Sample Group UMKM
Questionnaire Bank Pengelola -> Sample Group Bank Pengelola
Questionnaire Bank Peserta -> Sample Group Bank Peserta
```

### Pattern B - Satu Questionnaire dan Banyak Sample Group

Supported.

```text
Questionnaire Kepuasan
  -> Sample Group Mitra
  -> Sample Group Non Mitra
```

Keputusan:

Tidak ada unique constraint pada `sample_groups.questionnaire_id`.

## 8. Final Workflow

MVP workflow:

```text
Project Detail
  -> Sampling Plan Section
  -> Tambah Sample Group
  -> Isi Sample Group
  -> Tambah Target Wilayah
  -> Simpan Draft
  -> Sample Group Detail
  -> Edit Draft
  -> Tandai Ready
```

Future workflow:

```text
Proposal Draft Sampling Plan
  -> Setup Project
  -> Project Sampling Plan
```

Tidak masuk MVP pertama.

## 9. Final UI Scope

### 9.1 Project Detail

Tambahkan section:

```text
Sampling Plan
```

Konten:

- Summary card:
  - Total Sample Group.
  - Total Target.
  - Ready.
  - Draft.
- Button:
  - `+ Tambah Sample Group`
- Table:
  - Sample Group.
  - Questionnaire.
  - Total Target.
  - Wilayah.
  - Status.
  - Action.

### 9.2 Sample Group Create/Edit

Fields:

- Sample Group Name.
- Questionnaire Used.
- Target Respondent.
- Notes.
- Target Wilayah rows:
  - Region Type.
  - Region Name.
  - Target Sample.

Actions:

- Tambah Wilayah.
- Hapus Wilayah.
- Simpan Draft.
- Batal.

### 9.3 Sample Group Detail

Sections:

- Header.
- Status badge.
- Project reference.
- Questionnaire reference.
- Summary cards.
- Target Wilayah table.
- Notes.
- Next Business Action.

Actions:

- Edit Draft.
- Tandai Ready.

## 10. Final API Scope

Endpoint utama Sprint implementasi:

```text
GET /api/v1/projects/{project_id}/sample-groups
POST /api/v1/projects/{project_id}/sample-groups
GET /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}/status
```

MVP simplification:

Create/update Sample Group menerima `targets` secara inline.

Payload create:

```json
{
  "sample_group_name": "Rumah Tangga",
  "questionnaire_id": "optional-questionnaire-id",
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

Endpoint target terpisah dapat ditunda:

```text
POST /api/v1/sample-groups/{sample_group_id}/targets
PATCH /api/v1/sampling-targets/{target_id}
DELETE /api/v1/sampling-targets/{target_id}
```

## 11. Final Status Flow

Status Sample Group MVP:

```text
Draft -> Ready
```

Rules:

- Status awal adalah Draft.
- Draft dapat diedit.
- Ready tidak dapat diedit langsung pada MVP.
- Ready hanya dapat dicapai jika:
  - Sample Group Name terisi.
  - Minimal satu Sampling Target tersedia.
  - Total Target > 0.
  - Questionnaire dipilih jika Product Owner menetapkan wajib sebelum Fieldwork.

Invalid transition:

- Ready -> Draft.
- Ready -> Edit.
- Draft -> Cancelled.

Cancelled/Archived ditunda.

## 12. Final Activity Logging

Activity dicatat pada level Sample Group, bukan setiap perubahan kecil target wilayah.

Event MVP:

- Sampling Plan dibuat.
- Sampling Plan diperbarui.
- Sampling Plan ditandai Ready.

Activity source:

```text
source_type = "SamplingPlan"
source_id = sample_group.id
activity_type = "SamplingPlan"
```

Activity location:

- Client Activity Timeline.
- Future Project Timeline.

Catatan:

Jika target wilayah diubah saat update Sample Group, cukup dicatat sebagai `Sampling Plan diperbarui`.

## 13. Acceptance Criteria Sprint 8

Sprint 8 adalah design/discovery sprint. Acceptance criteria:

1. Nama modul final ditetapkan sebagai Sampling Plan.
2. Sampling Plan dikonfirmasi sebagai Target Sampling, bukan database responden.
3. Domain Model mendukung Pattern A.
4. Domain Model mendukung Pattern B.
5. Entity final ditetapkan: Sample Group dan Sampling Target.
6. Relationship final ditetapkan.
7. Workflow end-to-end disetujui.
8. UI MVP scope disetujui.
9. API MVP scope disetujui.
10. Status flow Draft -> Ready disetujui.
11. Activity Logging scope disetujui.
12. Import/Export Excel ditunda dari MVP pertama.
13. Out of Scope Sprint 8 jelas.
14. Dokumen Design Freeze tersedia.

## 14. Acceptance Criteria Implementasi Berikutnya

Untuk Sprint implementasi backend/frontend:

1. Project Detail menampilkan Sampling Plan section.
2. User dapat membuat Sample Group.
3. User dapat menambahkan Target Wilayah.
4. Total target dihitung dari target wilayah.
5. User dapat memilih Questionnaire dari Project yang sama.
6. Satu Questionnaire dapat dipakai oleh beberapa Sample Group.
7. Sample Group dapat dibuka ke detail.
8. Sample Group Draft dapat diedit.
9. Sample Group dapat ditandai Ready.
10. Activity Logging berjalan.
11. Tidak ada data responden individual yang disimpan.
12. Regression Proposal, Project, Questionnaire tetap berhasil.

## 15. Out of Scope Sprint 8

Tidak termasuk Sprint 8:

- Coding backend.
- Coding frontend.
- Database migration.
- API implementation.
- Commit.
- Import Excel.
- Export Excel.
- Database responden.
- Sample frame.
- Individual respondent.
- Random sampling.
- Weighting.
- Quota matrix kompleks.
- Fieldwork assignment.
- Monitoring otomatis.
- KoBo sync.

## 16. Risiko Implementasi

### Risiko 1 - Salah paham antara Sampling Plan dan database responden

Severity:
High

Mitigation:

- Gunakan label `Sampling Plan`.
- Hindari istilah `Sample Management` sebagai nama modul.
- Jangan membuat entity respondent pada MVP.

### Risiko 2 - Relasi Questionnaire dibuat 1:1 secara tidak sengaja

Severity:
High

Mitigation:

- Jangan buat unique constraint pada `questionnaire_id`.
- Test Pattern B wajib dilakukan.

### Risiko 3 - Target total tidak sinkron dengan target wilayah

Severity:
Medium

Mitigation:

- Hitung total dari `sampling_targets`.
- Jika menyimpan `total_target_sample`, update setiap create/update target.

### Risiko 4 - UI terlalu kompleks untuk input wilayah banyak

Severity:
Medium

Mitigation:

- MVP manual input dulu.
- Import/Export Excel menjadi backlog sprint berikutnya.

### Risiko 5 - Migration debt bertambah

Severity:
Medium

Mitigation:

- Product Owner perlu memutuskan apakah Alembic baseline dikerjakan sebelum Sprint implementasi database.

## 17. Rekomendasi Sprint 8

Sprint 8 Design Freeze dinyatakan selesai.

Rekomendasi setelah Sprint 8:

1. Jangan langsung coding frontend.
2. Mulai dengan Sprint 9 Backend Design/Implementation untuk Sampling Plan.
3. Sebelum membuat table baru, review keputusan Technical Foundation:
   - Apakah Alembic Migration Baseline dilakukan dulu.
   - Atau tetap memakai script upgrade sementara.
4. Backend implementation harus menguji Pattern A dan Pattern B.
5. Frontend implementation harus menampilkan Sampling Plan di Project Detail.

## 18. Final Decision

```text
READY FOR IMPLEMENTATION
```

Tidak ada blocker desain yang harus diselesaikan sebelum masuk sprint implementasi.
