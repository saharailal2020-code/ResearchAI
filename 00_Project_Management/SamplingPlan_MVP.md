# Sampling Plan MVP

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. MVP Scope

Sampling Plan MVP berfokus pada target survei yang disepakati dengan client.

MVP tidak mengelola database responden.

MVP mencakup:

- Sample Group.
- Questionnaire yang digunakan.
- Target wilayah.
- Target sample.
- Status.
- Activity Logging.

## 2. Recommended Module Name

Nama modul:

```text
Sampling Plan
```

Nama section di Project Detail:

```text
Sampling Plan
```

Nama action:

```text
+ Tambah Sample Group
```

Nama tabel:

```text
Sample Group
Target Wilayah
```

## 3. MVP Data Structure

### sample_groups

| Field | Required | Notes |
| --- | --- | --- |
| id | Yes | UUID |
| project_id | Yes | Project owner |
| questionnaire_id | Optional Draft, recommended Ready | Questionnaire used |
| sample_group_name | Yes | Rumah Tangga, UMKM, Mitra |
| target_respondent | Optional | Bisa sama dengan sample_group_name |
| total_target_sample | Auto/Stored | Sum target wilayah |
| status | Yes | Draft, Ready |
| notes | Optional | Catatan sampling |
| sort_order | Yes | Urutan tampilan |
| created_by | Optional | Current user |
| ready_at | Optional | Timestamp Ready |
| created_at | Yes | Timestamp |
| updated_at | Yes | Timestamp |

### sampling_targets

| Field | Required | Notes |
| --- | --- | --- |
| id | Yes | UUID |
| sample_group_id | Yes | Parent Sample Group |
| region_type | Yes | Provinsi atau Kabupaten/Kota |
| region_name | Yes | Jawa Barat, Bandung, Surabaya |
| target_sample | Yes | Integer > 0 |
| sort_order | Yes | Urutan tampilan |
| created_at | Yes | Timestamp |
| updated_at | Yes | Timestamp |

## 4. Example Data

### Pattern A

```text
Questionnaire Rumah Tangga
  -> Sample Group Rumah Tangga
       - Jawa Barat: 800
       - Jawa Tengah: 650
       - Jawa Timur: 900

Questionnaire UMKM
  -> Sample Group UMKM
       - Jawa Barat: 200
       - Jawa Tengah: 180
```

### Pattern B

```text
Questionnaire Kepuasan
  -> Sample Group Mitra
       - Jawa Barat: 150
       - Jawa Tengah: 120

Questionnaire Kepuasan
  -> Sample Group Non Mitra
       - Jawa Barat: 180
       - Jawa Tengah: 140
```

## 5. UI MVP

### Project Detail

Sampling Plan section:

```text
Sampling Plan
Target survei yang disepakati dengan client.

[Sample Group: 4] [Total Target: 2.730] [Ready: 3] [Draft: 1]

+ Tambah Sample Group

| Sample Group | Questionnaire | Total Target | Wilayah | Status | Action |
| Rumah Tangga | Q Rumah Tangga | 2.350 | 3 | Ready | Buka |
| UMKM | Q UMKM | 380 | 2 | Draft | Buka |
```

### Create Sample Group

Fields:

- Sample Group Name.
- Questionnaire Used.
- Target Respondent.
- Notes.
- Target Wilayah rows.

Target Wilayah rows:

- Region Type.
- Region Name.
- Target Sample.

Actions:

- Tambah Wilayah.
- Hapus Wilayah.
- Simpan Draft.
- Batal.

### Detail Sample Group

Sections:

- Header.
- Summary cards.
- Questionnaire Reference.
- Target Wilayah table.
- Notes.
- Next Business Action.

## 6. API MVP

Recommended endpoints:

```text
GET /api/v1/projects/{project_id}/sample-groups
POST /api/v1/projects/{project_id}/sample-groups
GET /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}/status
```

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
    },
    {
      "region_type": "Provinsi",
      "region_name": "Jawa Tengah",
      "target_sample": 650
    }
  ]
}
```

## 7. Validation MVP

Required:

- Sample Group Name.
- Minimal satu Target Wilayah.
- Region Type.
- Region Name.
- Target Sample > 0.

Optional:

- Questionnaire saat Draft.
- Target Respondent.
- Notes.

Ready validation:

- Sample Group Name exists.
- Minimal satu target wilayah.
- Total target > 0.
- Questionnaire selected if Product Owner decides it is required before Fieldwork.

## 8. Activity Logging MVP

Events:

- Sampling Plan dibuat.
- Sampling Plan diperbarui.
- Sampling Plan ditandai Ready.

Activity source:

```text
source_type = "SamplingPlan"
source_id = sample_group.id
```

Activity location:

- Client Activity Timeline.
- Future Project Timeline.

## 9. Security MVP

MVP:

- Semua endpoint butuh login.
- Current user menjadi created_by.
- Questionnaire yang dipilih harus milik Project yang sama.
- Sample Group hanya dapat diakses melalui Project yang benar.

Future:

- RBAC.
- Object-level Project authorization.
- Audit log.

## 10. Import/Export Excel

### Manual Input First

Pros:

- Scope kecil.
- Lebih cepat.
- Lebih aman.
- Cocok untuk validasi domain.

Cons:

- Lambat untuk banyak wilayah.
- Tidak ideal untuk project besar.

### Import/Export Excel First

Pros:

- Sesuai workflow nyata tim riset.
- Cepat untuk banyak wilayah.
- Cocok untuk data dari proposal/sampling plan existing.

Cons:

- Scope lebih besar.
- Perlu template.
- Perlu validasi.
- Perlu error report.
- Lebih banyak edge case.

### MVP Recommendation

```text
Manual input pada Sprint implementasi pertama.
Import/Export Excel menjadi sprint berikutnya.
```

Backlog:

```text
SAMPLING-IMPORT-001
Import/Export Excel untuk Sampling Target.
```

Template Excel future:

```text
sample_group_name | questionnaire_name | region_type | region_name | target_sample | notes
```

## 11. Out of Scope MVP

Tidak termasuk:

- Database responden.
- Sample frame.
- Individual respondent.
- Contact respondent.
- Import Excel.
- Export Excel.
- Random sampling.
- Weighting.
- Quota matrix kompleks.
- Monitoring otomatis.
- Fieldwork assignment.

## 12. Recommended Implementation Split

### Sprint 9 - Sampling Plan Backend

Scope:

- sample_groups table.
- sampling_targets table.
- API.
- Validation.
- Activity logging.
- Backend tests.

### Sprint 10 - Sampling Plan Frontend

Scope:

- Project Detail Sampling Plan section.
- Sample Group Create.
- Sample Group Detail.
- Target Wilayah input.
- Status Ready action.
- Browser testing.

### Sprint 10.1 - Excel Import/Export Discovery

Scope:

- Template Excel.
- Validation rules.
- Error report design.

## 13. Final Recommendation

Product recommendation:

Gunakan `Sampling Plan` sebagai nama modul.

Architecture recommendation:

Implementasi MVP memakai:

```text
sample_groups
sampling_targets
```

Jangan membuat database responden pada MVP ini.

Jangan memaksakan relasi Questionnaire 1:1 dengan Sample Group.

Pastikan satu Questionnaire dapat digunakan oleh banyak Sample Group.
