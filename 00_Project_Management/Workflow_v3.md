# Workflow v3 - Sampling Plan

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

## 1. Tujuan Workflow

Workflow ini menggantikan workflow Sample Management sebelumnya.

Fokus baru:

```text
Sampling Plan sebagai rencana target survei yang disepakati dengan client.
```

Bukan:

```text
Database responden.
```

## 2. End-to-End Position

```text
Proposal
  -> Project
  -> Questionnaire
  -> Sampling Plan
  -> Fieldwork
  -> Monitoring
  -> QC
  -> Dataset
```

## 3. Business Timing

Secara bisnis Beerka:

```text
Sampling Plan sudah ditentukan saat Proposal dibuat.
```

Namun untuk MVP implementation:

```text
Sampling Plan dibuat setelah Proposal Approved menjadi Project.
```

Alasan:

- Modul Proposal saat ini belum memiliki Sampling Plan section.
- Project sudah menjadi root operasional.
- Lebih aman membangun Sampling Plan di Project terlebih dahulu.

Future:

```text
Proposal Draft Sampling Plan -> Setup Project -> Project Sampling Plan
```

## 4. High Level Workflow

```text
Project Detail
  |
  v
Sampling Plan Section
  |
  +-- Tambah Sample Group
  |       |
  |       v
  |   Isi Sample Group
  |       |
  |       v
  |   Tambah Target Wilayah
  |       |
  |       v
  |   Simpan Draft
  |
  +-- Buka Sample Group
          |
          +-- Edit Draft
          |
          +-- Tandai Ready
```

## 5. Workflow Pattern A

Pattern A:
Setiap Sample Group menggunakan Questionnaire berbeda.

```text
Project Detail
  |
  +-- Questionnaire Rumah Tangga
  +-- Questionnaire UMKM
  +-- Questionnaire Bank Pengelola
  +-- Questionnaire Bank Peserta
  |
  +-- Sampling Plan
          |
          +-- Sample Group Rumah Tangga
          |      Questionnaire: Rumah Tangga
          |      Jawa Barat: 800
          |      Jawa Tengah: 650
          |
          +-- Sample Group UMKM
          |      Questionnaire: UMKM
          |      Jawa Barat: 200
          |      Jawa Tengah: 180
          |
          +-- Sample Group Bank Pengelola
          |      Questionnaire: Bank Pengelola
          |
          +-- Sample Group Bank Peserta
                 Questionnaire: Bank Peserta
```

## 6. Workflow Pattern B

Pattern B:
Beberapa Sample Group menggunakan Questionnaire yang sama.

```text
Project Detail
  |
  +-- Questionnaire Kepuasan
  |
  +-- Sampling Plan
          |
          +-- Sample Group Mitra
          |      Questionnaire: Kepuasan
          |      Jawa Barat: 150
          |      Jawa Tengah: 120
          |
          +-- Sample Group Non Mitra
                 Questionnaire: Kepuasan
                 Jawa Barat: 180
                 Jawa Tengah: 140
```

## 7. UI MVP

### Project Detail - Sampling Plan Section

Layout:

```text
Sampling Plan
Target survei yang disepakati untuk project ini.

Summary:
[Sample Group: 4] [Total Target: 2.730] [Ready: 3] [Draft: 1]

+ Tambah Sample Group

Table:
| Sample Group | Questionnaire | Total Target | Wilayah | Status | Action |
| Rumah Tangga | Q Rumah Tangga | 2.350 | 3 | Ready | Buka |
| UMKM | Q UMKM | 380 | 2 | Draft | Buka |
```

### Sample Group Create/Edit

Layout:

```text
Project Detail / Sampling Plan / Tambah Sample Group

Informasi Sample Group
- Sample Group Name
- Questionnaire Used
- Target Respondent
- Notes

Target Wilayah
| Region Type | Region Name | Target Sample |
| Provinsi | Jawa Barat | 800 |
| Provinsi | Jawa Tengah | 650 |

[+ Tambah Wilayah]

Informasi Sistem
- Status: Draft
- Total Target: auto sum

[Batal] [Simpan Draft]
```

### Sample Group Detail

Layout:

```text
Sample Group: Rumah Tangga              [Draft/Ready]
Questionnaire: Questionnaire Rumah Tangga
Total Target: 2.350

Target Wilayah
| Wilayah | Target |
| Jawa Barat | 800 |
| Jawa Tengah | 650 |
| Jawa Timur | 900 |

Next Business Action
[Edit Draft] [Tandai Ready]
```

## 8. Workflow Steps

### Step 1 - Open Project Detail

User membuka Project Detail.

System menampilkan Sampling Plan section.

Jika belum ada Sample Group:

```text
Belum ada Sampling Plan.
Tambahkan Sample Group untuk menentukan target survei project ini.
```

### Step 2 - Add Sample Group

User klik:

```text
+ Tambah Sample Group
```

System membuka form Sample Group.

### Step 3 - Select Questionnaire

User memilih Questionnaire.

Rules:

- Optional saat Draft.
- Harus berasal dari Project yang sama.
- Boleh digunakan oleh lebih dari satu Sample Group.

### Step 4 - Add Regional Targets

User mengisi wilayah dan target.

Fields:

- Region Type.
- Region Name.
- Target Sample.

System menghitung:

```text
Total Target = sum(Target Sample)
```

### Step 5 - Save Draft

System:

- Membuat Sample Group Draft.
- Membuat Sampling Target rows.
- Mencatat activity `Sampling Plan dibuat`.

### Step 6 - Mark Ready

User klik:

```text
Tandai Ready
```

Validation:

- Sample Group Name wajib.
- Minimal satu Sampling Target.
- Total Target > 0.
- Questionnaire wajib jika Product Owner menetapkan sebagai readiness rule.

System:

- Status menjadi Ready.
- Activity `Sampling Plan ditandai Ready`.

## 9. API MVP

Recommended endpoints:

```text
GET /api/v1/projects/{project_id}/sampling-plan
GET /api/v1/projects/{project_id}/sample-groups
POST /api/v1/projects/{project_id}/sample-groups
GET /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}
PATCH /api/v1/sample-groups/{sample_group_id}/status
```

Optional target endpoints:

```text
POST /api/v1/sample-groups/{sample_group_id}/targets
PATCH /api/v1/sampling-targets/{target_id}
DELETE /api/v1/sampling-targets/{target_id}
```

MVP simplification:

Create/update Sample Group can accept targets inline.

## 10. Database MVP

Core tables:

```text
sample_groups
sampling_targets
```

No respondent table.

## 11. Activity Logging

Events:

- Sampling Plan dibuat.
- Sampling Plan diperbarui.
- Sampling Plan ditandai Ready.
- Sampling Target ditambahkan.
- Sampling Target diperbarui.

MVP recommendation:

Untuk menghindari timeline terlalu ramai:

- Catat activity pada level Sample Group.
- Jangan catat setiap perubahan target wilayah sebagai activity terpisah kecuali perubahan besar.

## 12. Security

MVP:

- User harus login.
- created_by dari backend.
- Questionnaire harus milik Project yang sama.
- Sample Group harus milik Project yang sama.

Future:

- `sampling_plan:view`
- `sampling_plan:create`
- `sampling_plan:update`
- `sampling_plan:mark_ready`

## 13. Import/Export Excel Analysis

### Manual Input

Kelebihan:

- Cepat dibuat.
- Lebih kecil risiko bug.
- Cocok untuk validasi workflow awal.

Kekurangan:

- Lambat untuk project besar.
- Input banyak provinsi/kota menjadi melelahkan.

### Import/Export Excel

Kelebihan:

- Sesuai kebiasaan kerja tim riset.
- Lebih cepat untuk target wilayah banyak.
- Bisa menjadi bridge dari file proposal/sampling plan existing.

Kekurangan:

- Perlu template.
- Perlu validasi kolom.
- Perlu error report.
- Perlu handling duplicate wilayah.
- Perlu export formatting.

Recommendation:

```text
MVP Sprint pertama: manual input.
Sprint berikutnya: Import/Export Excel.
```

Reason:

- Manual input membuktikan domain dan workflow.
- Import/Export lebih aman setelah struktur final disetujui.

## 14. Out of Scope MVP

- Database responden.
- Sample frame.
- Import Excel pada sprint pertama.
- Export Excel pada sprint pertama.
- Random sampling.
- Weighting.
- Quota matrix kompleks.
- Enumerator assignment.
- KoBo sync.
- Monitoring otomatis.

## 15. Acceptance Criteria MVP

1. Project Detail menampilkan Sampling Plan section.
2. User dapat membuat Sample Group.
3. Sample Group dapat memilih Questionnaire.
4. Satu Questionnaire dapat dipilih oleh beberapa Sample Group.
5. User dapat menambahkan target wilayah.
6. Total target dihitung dari target wilayah.
7. Sample Group dapat ditandai Ready.
8. Sampling Plan tidak menyimpan data responden individual.
9. Activity Logging berjalan.
10. Pattern A dan Pattern B dapat dibuat.
