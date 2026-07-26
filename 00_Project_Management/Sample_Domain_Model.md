# Sample Domain Model

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. Tujuan Modul

Sample Management bertujuan mengelola target responden, jumlah sample, wilayah, segmentasi, dan catatan quota untuk Project riset.

Sample adalah jembatan antara:

```text
Questionnaire -> Fieldwork
```

Tanpa Sample, Fieldwork tidak memiliki target yang jelas untuk dihitung progress-nya.

## 2. Posisi Sample dalam Domain ResearchAI

```text
Client
  |
  +-- Proposal
          |
          +-- Project
                  |
                  +-- Questionnaire
                  |       |
                  |       +-- Sample Group
                  |
                  +-- Fieldwork
                          |
                          +-- Monitoring
                          +-- QC
```

## 3. Core Entity

### 3.1 Sample Group

Sample Group adalah unit target sample yang digunakan untuk Fieldwork.

Contoh:

```text
Project STKU 2026
  |
  +-- Sample Rumah Tangga
  |     Target: 1.200 responden
  |
  +-- Sample UMKM
  |     Target: 600 responden
  |
  +-- Sample Bank Peserta
        Target: 80 responden
```

### Fields MVP

| Field | Type | Required | Keterangan |
| --- | --- | --- | --- |
| `id` | UUID | Yes | Primary key |
| `project_id` | UUID | Yes | Project pemilik Sample |
| `questionnaire_id` | UUID | Optional | Questionnaire terkait |
| `sample_name` | String | Yes | Nama Sample Group |
| `target_respondent` | String | Yes | Kelompok responden |
| `target_sample_size` | Integer | Yes | Target jumlah responden |
| `region` | String | Optional | Wilayah/geografi |
| `segment` | String | Optional | Segmentasi responden |
| `quota_notes` | Text | Optional | Catatan quota |
| `status` | String | Yes | Draft atau Ready |
| `sort_order` | Integer | Yes | Urutan tampilan |
| `created_by` | UUID | Optional | User pembuat |
| `ready_at` | DateTime | Optional | Waktu ditandai Ready |
| `created_at` | DateTime | Yes | Waktu dibuat |
| `updated_at` | DateTime | Yes | Waktu terakhir update |

## 4. Relationship

### Project to Sample

```text
Project 1 -> many Sample Groups
```

Alasan:

Satu Project bisa memiliki banyak target respondent dan banyak kebutuhan sample.

### Questionnaire to Sample

```text
Questionnaire 1 -> many Sample Groups
```

Alasan:

Satu Questionnaire dapat digunakan untuk beberapa wilayah atau segmen sample.

Untuk MVP:

- `questionnaire_id` optional.
- Jika dipilih, Sample mengambil konteks Target Respondent dari Questionnaire.

### Sample to Fieldwork

```text
Sample Group 1 -> many Fieldwork Assignments
```

Belum diimplementasikan pada MVP Sample, tetapi harus dipertimbangkan.

### Sample to Monitoring

```text
Monitoring reads Sample target
```

Monitoring akan memakai target sample untuk menghitung:

- Completed sample.
- Remaining sample.
- Completion rate.

## 5. Conceptual ERD

```text
Project
  id
  project_number
  project_name
  status
      |
      | 1..many
      v
SampleGroup
  id
  project_id
  questionnaire_id
  sample_name
  target_respondent
  target_sample_size
  region
  segment
  quota_notes
  status
  sort_order
  ready_at
      ^
      | optional many..1
Questionnaire
  id
  project_id
  questionnaire_name
  target_respondent
  status
```

## 6. Sample Status

MVP status:

```text
Draft -> Ready
```

### Draft

Tujuan:

Sample sedang disusun.

Aktivitas utama:

- Isi target respondent.
- Isi target sample size.
- Isi region/segment bila ada.
- Isi quota notes.

Output:

- Sample belum siap untuk Fieldwork.

Status berikutnya:

- Ready.

### Ready

Tujuan:

Sample sudah cukup jelas untuk menjadi dasar Fieldwork.

Aktivitas utama:

- Sample digunakan untuk rencana Fieldwork.
- Monitoring dapat membaca target.

Output:

- Sample siap digunakan.

Status berikutnya:

- Untuk MVP tidak ada status berikutnya.

## 7. Business Rules

1. Sample wajib berada di bawah Project.
2. Sample boleh terkait ke Questionnaire.
3. Sample wajib memiliki Target Respondent.
4. Target Sample Size wajib lebih besar dari 0.
5. Sample Draft dapat diedit.
6. Sample Ready tidak diedit langsung pada MVP.
7. Sample tidak boleh dibuat pada Project Cancelled.
8. Sample tidak boleh dibuat pada Project Completed tanpa reopening.
9. Activity harus tercatat saat Sample dibuat, diperbarui, dan ditandai Ready.

## 8. Data Validation

### Required

- Sample Name.
- Target Respondent.
- Target Sample Size.

### Optional

- Questionnaire.
- Region.
- Segment.
- Quota Notes.

### Numeric Validation

- Target Sample Size harus integer.
- Target Sample Size minimum 1.
- Target Sample Size maksimum MVP disarankan 1.000.000 untuk mencegah input tidak masuk akal.

## 9. UI Data Requirements

### Project Detail Sample Section

Data yang perlu ditampilkan:

- Total Sample Group.
- Total Target Sample.
- Ready Sample.
- Draft Sample.
- List Sample.

### Sample List Columns

- Sample Name.
- Target Respondent.
- Questionnaire.
- Target Sample Size.
- Region.
- Segment.
- Status.
- Last Updated.
- Action.

### Sample Detail

- Header Sample.
- Status badge.
- Project reference.
- Questionnaire reference.
- Target details.
- Quota notes.
- System information.
- Next Business Action.

## 10. API Data Requirements

### Create Sample

Input:

- questionnaire_id optional.
- sample_name.
- target_respondent.
- target_sample_size.
- region optional.
- segment optional.
- quota_notes optional.

System generated:

- id.
- status Draft.
- sort_order.
- created_by.
- created_at.
- updated_at.

### Update Sample

Allowed only if status Draft.

Editable:

- questionnaire_id.
- sample_name.
- target_respondent.
- target_sample_size.
- region.
- segment.
- quota_notes.

### Mark Ready

Allowed only from Draft.

System updates:

- status Ready.
- ready_at.
- activity log.

## 11. Activity Model

Activity source:

```text
source_type = "Sample"
source_id = sample.id
activity_type = "Sample"
```

Events:

- Sample dibuat.
- Sample diperbarui.
- Sample ditandai Ready.

Activity location:

- Client Activity Timeline.
- Future Project Timeline.

## 12. Future Expansion

Future entities:

- Sample Quota.
- Sample Frame.
- Respondent List.
- Sampling Method.
- Weighting.
- Sample Allocation.

Future fields:

- sampling_method.
- confidence_level.
- margin_of_error.
- population_size.
- achieved_sample_size.
- is_required.

## 13. MVP Recommendation

MVP harus fokus pada:

```text
Sample Group + Target Respondent + Target Sample Size
```

Jangan membuat quota matrix kompleks pada Sprint 8/9.

Alasan:

- Target sample sederhana sudah cukup untuk membuka Fieldwork.
- Quota detail dapat ditambahkan setelah monitoring dasar berjalan.
