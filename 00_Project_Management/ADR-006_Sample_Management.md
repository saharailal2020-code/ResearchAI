# ADR-006 Sample Management

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Milestone:
M3 - Research Preparation

## 1. Tujuan

Mendefinisikan keputusan arsitektur untuk modul Sample Management sebagai jembatan antara Questionnaire dan Fieldwork.

Sample Management diperlukan agar setiap Project memiliki target responden, kuota, wilayah, dan segmentasi yang jelas sebelum pengumpulan data dimulai.

## 2. Latar Belakang

ResearchAI saat ini sudah memiliki:

```text
Client -> Proposal -> Project -> Multiple Questionnaire
```

Pada proses bisnis perusahaan riset seperti Beerka, satu Project dapat memiliki beberapa Questionnaire berdasarkan Target Respondent.

Contoh:

```text
Project STKU 2026
  |
  +-- Questionnaire Rumah Tangga
  +-- Questionnaire UMKM
  +-- Questionnaire Bank Pengelola Kas Titipan
  +-- Questionnaire Bank Peserta
```

Setiap target respondent tersebut dapat memiliki kebutuhan sample yang berbeda.

Karena itu, Fieldwork tidak boleh langsung dibuat hanya dari Project. Fieldwork harus membaca target sample agar progress, quota, dan monitoring punya dasar yang jelas.

## 3. Keputusan Arsitektur

1. Sample adalah operational object di bawah Project.
2. Sample dapat dikaitkan ke Questionnaire.
3. Sample merepresentasikan target responden, kuota, wilayah, dan segmentasi.
4. Satu Project dapat memiliki banyak Sample Group.
5. Satu Questionnaire dapat memiliki nol, satu, atau banyak Sample Group.
6. Sample menjadi dependency untuk Fieldwork.
7. Fieldwork progress pada MVP harus mengacu pada Sample target.
8. Sample memiliki lifecycle sederhana: `Draft -> Ready`.
9. Sample Ready menjadi sinyal bahwa target fieldwork sudah cukup jelas.
10. Sample tidak menggantikan Questionnaire, Fieldwork, atau Dataset.

## 4. Business Rules

### Project

1. Project status `Setup` dan `Ready` dapat membuat Sample.
2. Project `Completed` tidak boleh membuat atau mengubah Sample tanpa reopening.
3. Project `Cancelled` tidak boleh membuat atau mengubah Sample.
4. Project dapat memiliki banyak Sample Group.

### Questionnaire

1. Sample dapat dikaitkan ke Questionnaire jika sample tersebut menggunakan instrumen tertentu.
2. Untuk project multi-questionnaire, Sample sebaiknya mengikuti Target Respondent pada Questionnaire.
3. Questionnaire tidak wajib Ready untuk membuat Sample pada MVP, tetapi sebelum Fieldwork disarankan semua Questionnaire relevan sudah Ready.

### Sample

1. Sample wajib memiliki Project.
2. Sample wajib memiliki Sample Name.
3. Sample wajib memiliki Target Respondent.
4. Sample wajib memiliki Target Sample Size.
5. Target Sample Size harus lebih besar dari 0.
6. Region optional pada MVP.
7. Segment optional pada MVP.
8. Quota Notes optional pada MVP.
9. Status awal Sample adalah `Draft`.
10. Sample Draft dapat diedit.
11. Sample Ready tidak dapat diedit langsung pada MVP.
12. Sample dapat ditandai Ready setelah target minimum diisi.

### Fieldwork Readiness

Rule konseptual:

```text
Fieldwork dapat direncanakan jika Project memiliki minimal satu Sample Ready.
```

Rule ideal pada phase berikutnya:

```text
Fieldwork dapat dimulai jika seluruh Questionnaire wajib Ready dan seluruh Sample wajib Ready.
```

## 5. Entity yang Dibutuhkan

### Sample Group

Entity utama MVP.

Fields:

- Sample ID.
- Project ID.
- Questionnaire ID optional.
- Sample Name.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.
- Status.
- Sort Order.
- Created By.
- Ready At.
- Created At.
- Updated At.

### Future Entity: Sample Quota

Ditunda dari MVP.

Fields potensial:

- Sample Group ID.
- Quota Dimension.
- Quota Value.
- Target Count.
- Achieved Count.

Contoh:

```text
Region = Jakarta, Target = 100
Gender = Female, Target = 150
Age Group = 25-34, Target = 80
```

## 6. Workflow

MVP workflow:

```text
Project Detail
  -> Sample Section
  -> Tambah Sample Group
  -> Simpan Draft
  -> Sample Detail
  -> Edit Draft
  -> Tandai Ready
```

Status lifecycle:

```text
Draft -> Ready
```

## 7. API Decision

Primary endpoint:

```text
GET /api/v1/projects/{project_id}/samples
POST /api/v1/projects/{project_id}/samples
GET /api/v1/samples/{sample_id}
PATCH /api/v1/samples/{sample_id}
PATCH /api/v1/samples/{sample_id}/status
```

Recommended later action convention:

```text
POST /api/v1/samples/{sample_id}/actions/mark-ready
```

Untuk MVP, boleh mengikuti pola status endpoint yang sudah ada agar konsisten dengan Project dan Questionnaire saat ini.

## 8. UI Decision

Project Detail harus memiliki section Sample setelah Questionnaire.

Tampilan MVP:

- Empty state jika belum ada Sample.
- Tombol `+ Tambah Sample`.
- List/table Sample Group.
- Kolom:
  - Sample Name.
  - Target Respondent.
  - Questionnaire.
  - Target Sample Size.
  - Region.
  - Segment.
  - Status.
  - Last Updated.
  - Action.

Sample Detail menampilkan:

- Sample Name.
- Project.
- Questionnaire.
- Target Respondent.
- Target Sample Size.
- Region.
- Segment.
- Quota Notes.
- Status.
- Created At.
- Updated At.
- Ready At.

## 9. Activity Logging

Sample harus mencatat activity otomatis ke Client Activity Timeline melalui Project.

Events MVP:

- Sample dibuat.
- Sample diperbarui.
- Sample ditandai Ready.

Future events:

- Quota ditambahkan.
- Quota diperbarui.
- Sample digunakan untuk Fieldwork.

## 10. Security

MVP:

- Semua endpoint Sample wajib membutuhkan user login.
- Created By diisi dari current user.
- Role-based permission belum wajib jika belum ada RBAC.

Future:

- `sample:create`
- `sample:update`
- `sample:mark_ready`
- `sample:view`

Object-level rule:

- User hanya boleh mengakses Sample dari Project yang diizinkan.

## 11. Out of Scope MVP

Tidak termasuk Sprint 8 MVP:

- Advanced quota matrix.
- Random sampling.
- Sample frame import.
- Respondent database.
- Panel management.
- Weighting.
- Sampling algorithm.
- KoBo integration.
- Fieldwork assignment.
- Monitoring achievement otomatis.
- File upload sample frame.
- Version history sample.

## 12. Konsekuensi

### Positif

- Fieldwork memiliki dasar target yang jelas.
- Project multi-questionnaire menjadi lebih realistis.
- Monitoring dapat menghitung completion rate berdasarkan target sample.
- QC dan Dataset nantinya dapat ditelusuri berdasarkan target respondent.

### Negatif

- Menambah satu domain sebelum Fieldwork.
- Perlu tambahan UI dan API.
- Perlu keputusan relasi Sample ke Questionnaire.

### Netral

- Sample MVP dapat tetap sederhana.
- Advanced sampling method dapat ditunda.

## 13. Open Questions untuk Product Owner

1. Apakah Sample wajib selalu terkait ke Questionnaire, atau boleh hanya terkait Project?
2. Apakah Target Respondent otomatis mengikuti Questionnaire, atau boleh diubah manual?
3. Apakah satu Questionnaire boleh memiliki beberapa Sample Group?
4. Apakah Region wajib pada MVP?
5. Apakah Segment wajib pada MVP?
6. Apakah status Ready cukup, atau perlu status Approved?
7. Apakah Sample Ready harus menjadi syarat Project masuk Ready/Fieldwork?

## 14. Rekomendasi Final

Rekomendasi:

```text
Implement Sample Group sederhana pada MVP.
```

Keputusan paling aman:

- Sample wajib memiliki Project.
- Questionnaire optional tetapi sangat direkomendasikan.
- Target Respondent wajib.
- Target Sample Size wajib.
- Region dan Segment optional.
- Lifecycle cukup `Draft -> Ready`.

Dengan desain ini, ResearchAI dapat lanjut ke Fieldwork tanpa kehilangan struktur quota dan target respondent.
