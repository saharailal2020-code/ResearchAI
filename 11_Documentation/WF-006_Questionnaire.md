# WF-006 Questionnaire

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Milestone:
M3 - Research Preparation

Basis:

- Questionnaire Discovery v1
- Domain Model v1
- WF-005 Project Detail
- ADR-003 Project Lifecycle
- Design System v1

## 1. Tujuan Workflow

WF-006 mendefinisikan workflow Questionnaire sebagai modul pertama di bawah Project.

Questionnaire digunakan untuk menyiapkan instrumen riset sebelum Sample dan Fieldwork.

## 2. Workflow Utama

```text
Project Detail
  |
  v
Create Questionnaire
  |
  v
Questionnaire Draft
  |
  v
Edit Questionnaire
  |
  v
Tandai Ready
  |
  v
Questionnaire Ready
  |
  v
Project dapat lanjut ke preparation berikutnya
```

## 3. Create Questionnaire

Trigger:

- User membuka Project Detail.
- User klik card Questionnaire.
- Jika belum ada Questionnaire, user melihat action `Buat Questionnaire`.

Form Create Questionnaire MVP:

- Questionnaire Title.
- Questionnaire Type.
- Description.
- Source Format.
- XLSForm Reference optional.
- KoBo Form URL optional.

Default:

- Status: `Draft`.
- Version: `1`.
- Project: dari Project Detail.

Expected behavior:

- Questionnaire dibuat di bawah Project.
- Activity `Questionnaire dibuat` tercatat.
- User diarahkan ke Questionnaire Detail.

## 4. Edit Questionnaire

Questionnaire dapat diedit selama status `Draft`.

Field yang dapat diedit:

- Questionnaire Title.
- Questionnaire Type.
- Description.
- Source Format.
- XLSForm Reference.
- KoBo Form URL.

Business rule:

- Questionnaire `Ready` tidak diedit langsung.
- Jika perlu revisi setelah Ready, buat versi baru atau kembalikan ke Draft sesuai keputusan Product Owner.

Activity:

- `Questionnaire diperbarui`.

## 5. Versioning

Versioning penting, tetapi harus dijaga agar MVP tidak terlalu besar.

Rekomendasi MVP:

- Simpan `version_number`.
- Default version adalah `1`.
- Tampilkan version di detail.
- Jangan membuat full version history dulu.

Phase berikutnya:

```text
Ready v1
  -> Create Revision
  -> Draft v2
  -> Ready v2
```

Rules yang disarankan:

- Satu versi hanya satu status aktif.
- Versi Ready menjadi referensi Fieldwork.
- Versi lama dapat diarsipkan.

## 6. Publish / Ready

Untuk MVP, gunakan istilah:

```text
Tandai Ready
```

Alasan:

- Lebih sesuai dengan workflow internal.
- Tidak memberi kesan bahwa form otomatis dipublish ke KoBoToolbox.

Action:

```text
Draft -> Ready
```

Validation sebelum Ready:

- Questionnaire Title wajib.
- Questionnaire Type wajib.
- Source Format wajib.
- Jika Source Format = XLSForm, reference/link/file sebaiknya tersedia.
- Jika Source Format = KoBoToolbox, KoBo URL sebaiknya tersedia.

Activity:

- `Questionnaire ditandai Ready`.

## 7. Hubungan dengan Project Status

Questionnaire berada di bawah Project.

Rules:

- Questionnaire dapat dibuat saat Project status `Setup` atau `Ready`.
- Questionnaire Ready menjadi salah satu syarat sebelum Project masuk `Fieldwork`.
- Project `Completed` tidak boleh membuat Questionnaire baru tanpa reopening atau special permission.
- Project `Cancelled` tidak boleh membuat atau mengubah Questionnaire.

Recommended gate:

```text
Ready -> Fieldwork
```

Membutuhkan:

- Minimal satu Questionnaire status `Ready`.

Exception:

- Desk Research atau project tertentu mungkin tidak membutuhkan Questionnaire. Perlu keputusan Product Owner.

## 8. UI Flow

```text
Project Detail
  |
  v
Questionnaire Placeholder / Card
  |
  v
Questionnaire List atau Detail
  |
  v
Create Questionnaire
  |
  v
Questionnaire Detail
  |
  v
Tandai Ready
```

MVP simplification:

- Jika satu Project hanya punya satu Questionnaire, klik Questionnaire langsung membuka Questionnaire Detail jika sudah ada.
- Jika belum ada, membuka Create Questionnaire.

## 9. Questionnaire Detail

Informasi yang tampil:

- Questionnaire Title.
- Status badge.
- Version.
- Questionnaire Type.
- Source Format.
- Project Reference.
- XLSForm Reference.
- KoBo Form URL.
- Created Date.
- Updated Date.
- Ready Date.

Action:

- Edit, jika Draft.
- Tandai Ready, jika Draft.
- Create Revision, phase berikutnya.

## 10. Loading State

Pesan:

```text
Memuat questionnaire...
```

Untuk create/edit:

```text
Menyimpan questionnaire...
```

Untuk ready action:

```text
Menandai questionnaire ready...
```

## 11. Empty State

Jika belum ada Questionnaire:

```text
Belum ada questionnaire
Buat instrumen riset pertama untuk project ini.
```

Action:

```text
Buat Questionnaire
```

## 12. Error State

Error yang perlu ditangani:

### Project tidak ditemukan

```text
Project tidak ditemukan.
```

### Questionnaire tidak ditemukan

```text
Questionnaire tidak ditemukan.
```

### Project tidak valid

```text
Questionnaire tidak dapat dibuat untuk status project ini.
```

### Gagal menyimpan

```text
Questionnaire belum bisa disimpan. Silakan coba lagi.
```

## 13. Business Rules

1. Questionnaire wajib memiliki Project.
2. Questionnaire dibuat dari Project Detail.
3. Untuk MVP, satu Project cukup satu Questionnaire utama.
4. Status awal Questionnaire adalah `Draft`.
5. Questionnaire Draft dapat diedit.
6. Questionnaire Ready tidak diedit langsung.
7. Version number disimpan sejak MVP.
8. `Tandai Ready` membuat Questionnaire siap dipakai Fieldwork.
9. Activity dicatat dari backend service.
10. Integrasi KoBoToolbox API belum masuk MVP.
11. XLSForm dapat disimpan sebagai reference/link pada MVP.

## 14. Acceptance Criteria

1. User dapat membuat Questionnaire dari Project Detail.
2. Questionnaire terhubung ke Project.
3. Questionnaire memiliki status `Draft`.
4. Questionnaire memiliki version number.
5. User dapat melihat Questionnaire Detail.
6. User dapat edit Questionnaire Draft.
7. User dapat menandai Questionnaire menjadi Ready.
8. Questionnaire Ready tampil di Project Detail.
9. Activity `Questionnaire dibuat` tercatat.
10. Activity `Questionnaire diperbarui` tercatat.
11. Activity `Questionnaire ditandai Ready` tercatat.
12. Project tidak dapat masuk Fieldwork tanpa Questionnaire Ready, kecuali exception disetujui.

## 15. Out of Scope Workflow MVP

- Form builder.
- Question editor detail.
- Skip logic editor.
- XLSForm parser.
- KoBoToolbox API integration.
- File upload penuh.
- Client review portal.
- Multi-questionnaire management kompleks.
- Version history lengkap.

## 16. Rekomendasi Final

Implementasi pertama sebaiknya sederhana:

- Questionnaire metadata.
- Link/reference XLSForm atau KoBo.
- Status Draft/Ready.
- Version number.
- Activity logging.
- Project Detail integration.

Dengan ini ResearchAI mulai menyiapkan modul Research Preparation tanpa langsung membangun survey builder besar.
