# Sample Workflow

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. Tujuan Workflow

Sample Workflow mendefinisikan bagaimana user membuat dan menyiapkan Sample Group pada Project sebelum masuk ke Fieldwork.

Workflow ini memastikan setiap Fieldwork memiliki target yang jelas:

- Siapa respondennya.
- Berapa targetnya.
- Wilayah atau segmennya apa.
- Questionnaire apa yang digunakan.

## 2. User Utama

### Research Manager

Menentukan desain sample berdasarkan metodologi riset.

### Project Manager

Mengelola kesiapan sample untuk project delivery.

### Fieldwork Manager

Menggunakan sample sebagai dasar rencana fieldwork.

### Statistician atau Analyst

Membantu menentukan target sample, segmentasi, dan quota.

## 3. High Level Flow

```text
Project Detail
  |
  v
Sample Section
  |
  v
Tambah Sample
  |
  v
Isi Sample Draft
  |
  v
Simpan Draft
  |
  v
Sample Detail
  |
  +-- Edit Draft
  |
  +-- Tandai Ready
          |
          v
      Sample Ready
```

## 4. Workflow Detail

### Step 1 - Buka Project Detail

User membuka Project Detail.

System menampilkan:

- Project summary.
- Questionnaire list.
- Sample section.
- Fieldwork placeholder.

Jika belum ada Sample:

```text
Belum ada Sample
Tambahkan target sample untuk project ini sebelum Fieldwork dibuat.
```

Action:

- `+ Tambah Sample`.

### Step 2 - Tambah Sample

User klik `+ Tambah Sample`.

System membuka halaman Sample Create.

Breadcrumb:

```text
Project Detail / Tambah Sample
```

### Step 3 - Isi Sample Draft

Field MVP:

- Questionnaire optional.
- Sample Name.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.

Behavior:

- Jika user memilih Questionnaire, Target Respondent dapat otomatis terisi dari Questionnaire.
- User tetap dapat menyesuaikan Target Respondent jika Product Owner menyetujui.

### Step 4 - Simpan Draft

User klik `Simpan Draft`.

Validasi:

- Sample Name wajib.
- Target Respondent wajib.
- Target Sample Size wajib dan lebih besar dari 0.

System:

- Membuat Sample status Draft.
- Mencatat activity `Sample dibuat`.
- Redirect ke Sample Detail.

### Step 5 - Sample Detail

Sample Detail menampilkan:

- Sample Name.
- Status.
- Project reference.
- Questionnaire reference.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.
- System information.
- Next Business Action.

Jika status Draft:

- Action `Edit Draft`.
- Action `Tandai Ready`.

Jika status Ready:

- Tidak ada edit langsung pada MVP.
- Tampilkan pesan: `Sample sudah siap digunakan untuk Fieldwork.`

### Step 6 - Edit Draft

User dapat mengubah Sample selama status Draft.

Editable fields:

- Questionnaire.
- Sample Name.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.

System:

- Menyimpan perubahan.
- Mencatat activity `Sample diperbarui`.

### Step 7 - Tandai Ready

User klik `Tandai Ready`.

System:

- Validasi required fields.
- Mengubah status Draft menjadi Ready.
- Mengisi ready_at.
- Mencatat activity `Sample ditandai Ready`.

Result:

- Sample dapat digunakan untuk Fieldwork Planning.

## 5. Status Lifecycle

```text
Draft -> Ready
```

Invalid transition:

- Ready -> Draft.
- Ready -> Edit.
- Draft -> Cancelled.

Catatan:

Status Cancelled/Archived dapat dipertimbangkan pada phase berikutnya.

## 6. UI Design

### Project Detail Sample Section

Layout:

```text
------------------------------------------------------
Sample
Target sample dan quota dasar project.
                                      + Tambah Sample
------------------------------------------------------
| Sample Name | Target Respondent | Questionnaire |
| Target      | Region            | Status        |
| Last Update | Action                         |
------------------------------------------------------
```

Summary optional:

```text
Total Sample Group: 4
Total Target Sample: 2.000
Ready: 3
Draft: 1
```

### Sample Create

Layout:

```text
Project Detail / Tambah Sample

Tambah Sample
------------------------------------------------------
Informasi Sample

Questionnaire        [dropdown optional]
Sample Name          [input]
Target Respondent    [input]
Target Sample Size   [number]
Region               [input optional]
Segment              [input optional]
Quota Notes          [textarea optional]

Informasi Sistem
Status               Draft
Project              readonly
Created By           readonly

[Batal] [Simpan Draft]
```

### Sample Detail

Layout:

```text
Project Detail / Sample Detail

SAMPLE NAME                         [Draft/Ready]
Project: PRJ-...
Questionnaire: Questionnaire Rumah Tangga

Summary Cards:
- Target Sample
- Target Respondent
- Region
- Status

Information Card:
- Sample Name
- Questionnaire
- Target Respondent
- Target Sample Size
- Region
- Segment
- Quota Notes

Next Business Action:
- Edit Draft
- Tandai Ready
```

## 7. API Workflow

### List Samples by Project

```text
GET /api/v1/projects/{project_id}/samples
```

Use:

- Project Detail Sample Section.

### Create Sample

```text
POST /api/v1/projects/{project_id}/samples
```

Payload:

```json
{
  "questionnaire_id": "optional-uuid",
  "sample_name": "Sample Rumah Tangga",
  "target_respondent": "Rumah Tangga",
  "target_sample_size": 1200,
  "region": "Nasional",
  "segment": "Urban dan Rural",
  "quota_notes": "Distribusi mengikuti desain STKU."
}
```

### Get Sample Detail

```text
GET /api/v1/samples/{sample_id}
```

### Update Sample

```text
PATCH /api/v1/samples/{sample_id}
```

Allowed:

- Draft only.

### Update Sample Status

```text
PATCH /api/v1/samples/{sample_id}/status
```

Payload:

```json
{
  "status": "Ready"
}
```

## 8. Database Workflow

Create Sample:

1. Validate Project exists.
2. Validate Project status allows sample creation.
3. Validate Questionnaire belongs to same Project if provided.
4. Validate required fields.
5. Generate sort_order.
6. Insert Sample.
7. Record activity.
8. Return Sample Detail.

Update Sample:

1. Load Sample.
2. Reject if not Draft.
3. Validate Questionnaire belongs to same Project if changed.
4. Validate required fields.
5. Update Sample.
6. Record activity.

Mark Ready:

1. Load Sample.
2. Reject if not Draft.
3. Validate readiness fields.
4. Set status Ready.
5. Set ready_at.
6. Record activity.

## 9. Activity Logging

Activity events:

| Event | Trigger | Activity Title |
| --- | --- | --- |
| Create | Sample saved as Draft | Sample dibuat |
| Update | Draft edited | Sample diperbarui |
| Ready | Status changed to Ready | Sample ditandai Ready |

Activity description examples:

```text
Sample Rumah Tangga telah dibuat.
Sample Rumah Tangga telah diperbarui.
Sample Rumah Tangga siap digunakan untuk Fieldwork.
```

## 10. Error State

### Project Not Found

Message:

```text
Project tidak ditemukan.
```

### Questionnaire Invalid

Message:

```text
Questionnaire tidak valid untuk project ini.
```

### Validation Error

Message:

```text
Lengkapi Sample Name, Target Respondent, dan Target Sample Size.
```

### Ready Sample Edited

Message:

```text
Sample Ready tidak dapat diedit pada MVP.
```

### Backend Down

Message:

```text
Tidak dapat terhubung ke server.
```

## 11. Loading State

Loading state diperlukan untuk:

- Project Detail Sample Section.
- Sample Create project/questionnaire data.
- Sample Detail.
- Save Draft.
- Mark Ready.

Button loading text:

- `Menyimpan Sample...`
- `Memperbarui Sample...`
- `Menandai Ready...`

## 12. Security

MVP:

- User harus login.
- Backend mengisi created_by dari current user.
- User tidak boleh mengirim created_by manual.

Future:

- Role permission.
- Project-level access.
- Audit log.

## 13. Out of Scope MVP

Tidak termasuk:

- Sample frame upload.
- Quota matrix multi-level.
- Random sampling generator.
- Respondent database.
- Panel respondent.
- Weighting.
- Fieldwork assignment.
- KoBo target sync.
- Automated quota achievement.

## 14. Acceptance Criteria

1. User dapat melihat Sample section di Project Detail.
2. User dapat membuat Sample dari Project Detail.
3. User dapat memilih Questionnaire optional.
4. User dapat mengisi Sample Name.
5. User dapat mengisi Target Respondent.
6. User dapat mengisi Target Sample Size.
7. User dapat mengisi Region optional.
8. User dapat mengisi Segment optional.
9. User dapat mengisi Quota Notes optional.
10. Sample status awal Draft.
11. Sample Draft dapat diedit.
12. Sample dapat ditandai Ready.
13. Sample Ready tidak dapat diedit.
14. Project Detail menampilkan list Sample.
15. Activity Logging berjalan.
16. Backend test berhasil.
17. Frontend lint berhasil.
18. Frontend build berhasil.
19. Browser testing berhasil.
20. Regression Proposal, Project, Questionnaire tetap berhasil.
