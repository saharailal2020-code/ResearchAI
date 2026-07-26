# Questionnaire Discovery v1

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Milestone:
M3 - Research Preparation

## 1. Tujuan Discovery

Dokumen ini menganalisis bagaimana modul Questionnaire harus bekerja dalam konteks perusahaan riset seperti Beerka.

Questionnaire adalah modul pertama di bawah Project yang digunakan sebelum Sample dan Fieldwork. Modul ini menjadi fondasi instrumen riset yang akan dipakai untuk pengumpulan data, baik melalui survey digital, wawancara, FGD/IDI guide, mystery shopping checklist, atau instrumen riset lain.

## 2. Tujuan Questionnaire

Questionnaire bertujuan untuk:

- Menyusun instrumen riset yang digunakan dalam Project.
- Menjadi sumber pertanyaan, alur, instruksi interviewer, dan logic survey.
- Menjadi dokumen operasional sebelum Sample dan Fieldwork dimulai.
- Menyediakan status kesiapan instrumen.
- Menjaga versioning agar perubahan questionnaire dapat dilacak.
- Menjadi referensi bagi Fieldwork, QC, Dataset, Dashboard, dan Report.

Questionnaire bukan sekadar file lampiran. Questionnaire adalah operational object di bawah Project.

## 3. Hubungan dengan Project

Relasi domain:

```text
Project
  |
  +-- Questionnaire
        |
        +-- Version
        +-- XLSForm / KoBo Form Reference
        +-- Ready Status
        +-- Fieldwork Dependency
```

Business dependency:

- Project wajib ada sebelum Questionnaire dibuat.
- Questionnaire berada di bawah Project.
- Satu Project dapat memiliki satu atau lebih Questionnaire.
- Untuk MVP, satu Project cukup memiliki satu Questionnaire utama.
- Fieldwork idealnya tidak dimulai sebelum Questionnaire berstatus `Ready`.

## 4. Peran Questionnaire dalam Workflow ResearchAI

Posisi Questionnaire dalam alur M3:

```text
Project Setup
  -> Project Ready
  -> Questionnaire Draft
  -> Questionnaire Review
  -> Questionnaire Ready
  -> Sample
  -> Fieldwork
```

Questionnaire menjadi bridge antara desain riset dan pelaksanaan lapangan.

## 5. Siklus Hidup Questionnaire

Lifecycle yang direkomendasikan:

```text
Draft
  -> In Review
  -> Ready
```

Status tambahan:

```text
Archived
```

Jika versioning diterapkan:

```text
Draft v1
  -> In Review v1
  -> Ready v1
  -> Revision creates Draft v2
  -> Ready v2
```

## 6. Status Questionnaire

| Status | Tujuan | Keterangan |
| --- | --- | --- |
| Draft | Menyusun instrumen awal | Masih dapat diedit |
| In Review | Review internal/client | Perubahan besar sebaiknya dikontrol |
| Ready | Siap digunakan untuk Fieldwork | Menjadi acuan operasional |
| Archived | Tidak aktif | Untuk versi lama atau instrumen yang tidak dipakai |

Rekomendasi MVP:

- Gunakan `Draft` dan `Ready` terlebih dahulu.
- `In Review` dapat ditambahkan jika workflow review internal diperlukan.
- `Archived` diperlukan jika versioning sudah berjalan.

## 7. Business Rules

1. Questionnaire wajib terkait dengan Project.
2. Project harus minimal berada pada status `Setup` atau `Ready`.
3. Untuk MVP, Questionnaire dapat dibuat saat Project status `Setup`.
4. Questionnaire harus `Ready` sebelum Project masuk `Fieldwork`.
5. Satu Project MVP cukup memiliki satu Questionnaire utama.
6. Questionnaire `Ready` tidak boleh diedit langsung tanpa membuat versi baru.
7. Perubahan dari `Ready` harus menghasilkan Draft version baru jika versioning aktif.
8. Activity harus tercatat saat:
   - Questionnaire dibuat.
   - Questionnaire diperbarui.
   - Questionnaire ditandai Ready.
   - Versi baru dibuat.
9. Questionnaire bukan Sample.
10. Questionnaire bukan Fieldwork.
11. Questionnaire dapat memiliki referensi ke file XLSForm atau form KoBoToolbox.

## 8. Data Utama Questionnaire

Candidate field:

- `id`
- `project_id`
- `questionnaire_title`
- `questionnaire_type`
- `status`
- `version_number`
- `description`
- `source_format`
- `xlsform_file_url`
- `kobo_form_id`
- `kobo_project_url`
- `created_by`
- `ready_at`
- `created_at`
- `updated_at`

Questionnaire Type:

- Quantitative Survey.
- Qualitative Guide.
- FGD Guide.
- IDI Guide.
- Mystery Shopping Checklist.
- Observation Checklist.
- Screener.
- Other.

Source Format:

- Manual.
- XLSForm.
- KoBoToolbox.
- Document.

## 9. Hubungan dengan KoBoToolbox / XLSForm

KoBoToolbox dan XLSForm relevan jika Beerka menggunakan survey digital untuk pengumpulan data.

### XLSForm

XLSForm biasanya menjadi format struktur survey yang dapat memuat:

- Survey questions.
- Choices.
- Skip logic.
- Constraints.
- Required rules.
- Calculations.
- Relevance logic.

ResearchAI dapat menyimpan:

- File XLSForm.
- Metadata XLSForm.
- Status validasi XLSForm.
- Link upload/export.

### KoBoToolbox

KoBoToolbox dapat menjadi deployment tool untuk form.

ResearchAI dapat menyimpan:

- KoBo form ID.
- KoBo project URL.
- Deployment status.
- Last sync date.

Rekomendasi MVP:

- Jangan integrasi API KoBoToolbox dulu.
- Simpan referensi manual:
  - XLSForm file/link.
  - KoBo form URL atau form ID.
- Integrasi API KoBoToolbox menjadi phase berikutnya.

## 10. Hubungan dengan Modul Berikutnya

### Sample

Sample membutuhkan konteks dari Questionnaire:

- Target responden.
- Screening criteria.
- Segment/quota logic jika tersedia.

### Fieldwork

Fieldwork membutuhkan Questionnaire `Ready`:

- Link instrumen.
- Versi yang digunakan.
- Instruksi lapangan.

### QC

QC membutuhkan Questionnaire untuk:

- Validasi jawaban.
- Required field.
- Logic consistency.
- Backcheck reference.

### Dataset

Dataset membutuhkan Questionnaire untuk:

- Variable name.
- Label pertanyaan.
- Answer choices.
- Data dictionary.

### Dashboard dan Report

Dashboard dan Report membutuhkan Questionnaire untuk:

- Struktur indikator.
- Pertanyaan kunci.
- Breakdown variable.

## 11. Activity Logging

Activity masuk ke Client Activity Timeline melalui Project.

Event MVP:

- `Questionnaire dibuat`.
- `Questionnaire diperbarui`.
- `Questionnaire ditandai Ready`.

Event phase berikutnya:

- `Questionnaire versi baru dibuat`.
- `XLSForm diunggah`.
- `KoBoToolbox form direferensikan`.
- `Questionnaire diarsipkan`.

## 12. MVP Recommendation

Untuk MVP awal Questionnaire:

- Satu Project memiliki satu Questionnaire utama.
- Questionnaire dibuat dari Project Detail.
- Field minimal:
  - Questionnaire Title.
  - Questionnaire Type.
  - Description.
  - Source Format.
  - XLSForm Link/File Reference optional.
  - KoBo Form URL optional.
- Status:
  - Draft.
  - Ready.
- Versioning disiapkan sebagai field `version_number`, tetapi versi kompleks ditunda.
- Publish memakai istilah `Tandai Ready`, bukan publish penuh.

## 13. Risiko

### Risiko 1: Questionnaire menjadi terlalu kompleks

Jika ResearchAI langsung membuat form builder lengkap, scope MVP akan membesar drastis.

Mitigasi:

- MVP hanya metadata dan reference.
- Form builder ditunda.

### Risiko 2: Integrasi KoBo terlalu awal

Integrasi API KoBo membutuhkan credential, permission, error handling, dan sync.

Mitigasi:

- Simpan link/reference manual dulu.
- API integration menjadi phase berikutnya.

### Risiko 3: Versioning terlalu berat

Versioning penuh dapat memperbesar scope.

Mitigasi:

- Simpan `version_number`.
- Atur rule sederhana: Ready tidak diedit langsung.
- Implementasi versi baru ditunda jika belum perlu.

### Risiko 4: Fieldwork dimulai tanpa Questionnaire Ready

Ini bisa membuat pelaksanaan lapangan memakai instrumen yang belum final.

Mitigasi:

- Project status Fieldwork membutuhkan minimal satu Questionnaire Ready.

## 14. Open Questions

1. Untuk Beerka, apakah satu Project umumnya memakai satu Questionnaire atau bisa lebih dari satu sejak MVP?
2. Apakah Questionnaire harus mencakup FGD/IDI guide, atau hanya survey kuantitatif dulu?
3. Apakah Beerka saat ini rutin memakai KoBoToolbox?
4. Apakah XLSForm menjadi format utama untuk survey digital?
5. Apakah file upload perlu masuk MVP, atau cukup link/reference?
6. Apakah client ikut review Questionnaire di ResearchAI, atau review tetap di luar sistem?
7. Apakah Questionnaire `Ready` boleh dikembalikan ke Draft?
8. Apakah Project boleh masuk Fieldwork tanpa Questionnaire Ready untuk project non-survey seperti Desk Research?
9. Apakah perlu approval internal sebelum Ready?

## 15. Rekomendasi Product Development

Rekomendasi:

- Sprint 7 fokus pada Questionnaire MVP metadata dan status.
- Jangan membuat form builder.
- Jangan integrasi API KoBoToolbox dulu.
- Buat hubungan jelas dengan Project Detail.
- Tambahkan gate ringan: Project masuk Fieldwork membutuhkan Questionnaire Ready, kecuali Research Type tertentu disetujui Product Owner.
