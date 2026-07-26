# ADR-006 Revision - Sampling Plan

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Revisi dari:
ADR-006 Sample Management

## 1. Alasan Revisi

Setelah Discovery Sprint 8, Product Owner memberikan klarifikasi proses bisnis Beerka:

1. Sampling Plan sudah ditentukan sejak Proposal dibuat.
2. Sampling Plan bukan database responden.
3. Sampling Plan berisi target survei yang disepakati dengan klien.
4. Questionnaire dan Sampling Plan tidak selalu memiliki relasi 1:1.
5. Satu Questionnaire dapat digunakan oleh beberapa Sample Group.
6. Database responden akan menjadi modul terpisah pada sprint berikutnya.

Klarifikasi ini mengubah desain domain dari `Sample Management` menjadi domain yang lebih tepat: `Sampling Plan`.

## 2. Review Nama Modul

### Option 1 - Sample Management

Kelebihan:

- Umum digunakan dalam sistem riset.
- Singkat dan mudah dikenali.

Kekurangan:

- Berpotensi disalahpahami sebagai database responden.
- Terdengar seperti mengelola individual sample/respondent.
- Kurang menekankan bahwa target sudah direncanakan di tahap Proposal.

Kesimpulan:

Tidak direkomendasikan sebagai nama modul MVP.

### Option 2 - Sampling Plan

Kelebihan:

- Paling sesuai dengan proses bisnis Beerka.
- Menjelaskan bahwa ini adalah rencana target sampling, bukan daftar responden.
- Cocok karena sampling target sudah muncul sejak Proposal.
- Fleksibel untuk target per wilayah dan target per sample group.
- Tetap dapat menjadi dasar Fieldwork dan Monitoring.

Kekurangan:

- Sedikit lebih formal.
- Perlu penjelasan UI agar user paham isinya adalah target sampling.

Kesimpulan:

Direkomendasikan sebagai nama modul utama.

### Option 3 - Target Sampling

Kelebihan:

- Menjelaskan bahwa fokusnya target.
- Lebih jelas untuk user operasional.

Kekurangan:

- Kurang natural sebagai nama modul.
- Lebih cocok sebagai section atau sub-komponen dalam Sampling Plan.

Kesimpulan:

Cocok sebagai istilah UI untuk tabel target, bukan nama domain utama.

### Option 4 - Sample Planning

Kelebihan:

- Menjelaskan proses perencanaan.

Kekurangan:

- Terdengar kurang baku.
- Masih bisa tertukar dengan sample/respondent management.

Kesimpulan:

Tidak sekuat Sampling Plan.

## 3. Keputusan Arsitektur

Nama domain yang direkomendasikan:

```text
Sampling Plan
```

Istilah entity:

```text
Sampling Plan
  -> Sample Group
  -> Sampling Target
```

Penjelasan:

- `Sampling Plan` adalah rencana sampling pada level Project.
- `Sample Group` adalah kelompok target survei, misalnya Rumah Tangga, UMKM, Bank Pengelola, Bank Peserta.
- `Sampling Target` adalah rincian target per wilayah, misalnya Jawa Barat 800, Jawa Tengah 650.

## 4. Business Rules Baru

### Proposal

1. Sampling Plan secara bisnis sudah ditentukan saat Proposal dibuat.
2. Pada MVP, Sampling Plan dapat dibuat setelah Project terbentuk, tetapi harus tetap merepresentasikan kesepakatan Proposal.
3. Pada phase berikutnya, Proposal dapat memiliki draft Sampling Plan yang diwariskan ke Project.

### Project

1. Project memiliki satu Sampling Plan aktif pada MVP.
2. Sampling Plan berada di bawah Project.
3. Project dapat memiliki banyak Sample Group.
4. Sample Group dapat memiliki banyak Sampling Target per wilayah.

### Questionnaire

1. Questionnaire tidak selalu 1:1 dengan Sample Group.
2. Satu Sample Group dapat menggunakan satu Questionnaire.
3. Satu Questionnaire dapat digunakan oleh banyak Sample Group.
4. Sample Group boleh belum memilih Questionnaire saat Draft, tetapi harus memilih Questionnaire sebelum Fieldwork.

### Sample Group

1. Sample Group merepresentasikan kelompok survei yang disepakati dengan klien.
2. Sample Group bukan daftar responden.
3. Sample Group wajib memiliki nama.
4. Sample Group wajib memiliki target total.
5. Sample Group dapat memiliki banyak target wilayah.
6. Target total dapat dihitung dari jumlah target wilayah.

### Sampling Target

1. Sampling Target merepresentasikan target sample per wilayah.
2. Wilayah dapat berupa Provinsi atau Kabupaten/Kota.
3. Target Sample wajib lebih besar dari 0.
4. Sampling Target bukan individual respondent.

## 5. Pattern yang Harus Didukung

### Pattern A - Banyak Questionnaire

```text
Sample Group Rumah Tangga -> Questionnaire Rumah Tangga
Sample Group UMKM -> Questionnaire UMKM
Sample Group Bank Pengelola -> Questionnaire Bank Pengelola
Sample Group Bank Peserta -> Questionnaire Bank Peserta
```

Makna:

- Setiap Sample Group memakai instrumen berbeda.
- Cocok untuk project multi-target dengan kebutuhan pertanyaan berbeda.

### Pattern B - Satu Questionnaire untuk Beberapa Sample Group

```text
Questionnaire Kepuasan
  |
  +-- Sample Group Mitra
  +-- Sample Group Non Mitra
```

Makna:

- Instrumen sama.
- Segment target berbeda.
- Monitoring tetap perlu melihat progress per Sample Group.

## 6. Entity Decision

### Sampling Plan

Level:
Project

Fungsi:

Menjadi container rencana sampling project.

### Sample Group

Level:
Di bawah Sampling Plan/Project

Fungsi:

Menjadi kelompok target survei.

### Sampling Target

Level:
Di bawah Sample Group

Fungsi:

Menjadi rincian target per wilayah.

## 7. Rekomendasi MVP

Untuk MVP, implementasi dapat disederhanakan:

1. Tidak perlu table `sampling_plans` terpisah jika satu Project hanya memiliki satu Sampling Plan.
2. Gunakan `sample_groups` sebagai entity utama.
3. Gunakan `sampling_targets` untuk rincian wilayah.
4. Field `questionnaire_id` berada di `sample_groups`.
5. Target total dapat disimpan di `sample_groups` dan/atau dihitung dari `sampling_targets`.

Rekomendasi paling aman:

```text
Project
  -> SampleGroup
       -> SamplingTarget
```

Dengan optional reference:

```text
SampleGroup.questionnaire_id
```

## 8. UI Decision

Label modul di UI:

```text
Sampling Plan
```

Tombol:

```text
+ Tambah Sample Group
```

Tabel utama:

- Sample Group.
- Questionnaire.
- Total Target.
- Jumlah Wilayah.
- Status.
- Last Updated.
- Action.

Detail Sample Group:

- Sample Group name.
- Questionnaire used.
- Total target.
- Target by region.
- Status.

## 9. Import/Export Excel Decision

### Option A - Manual Input Only

Kelebihan:

- Lebih sederhana.
- Lebih cepat dibangun.
- Risiko bug lebih kecil.
- Cocok untuk validasi MVP awal.

Kekurangan:

- Input target wilayah banyak akan lambat.
- Tidak ideal untuk project besar seperti STKU.

### Option B - Import/Export Excel sejak MVP

Kelebihan:

- Lebih sesuai kebiasaan kerja riset.
- Mempercepat input target wilayah.
- Cocok untuk project besar dengan banyak provinsi/kota.

Kekurangan:

- Scope bertambah.
- Perlu template Excel.
- Perlu validasi file.
- Perlu error handling import.
- Perlu export format.

### Rekomendasi

Untuk MVP awal Sprint 9/10:

```text
Manual input terlebih dahulu.
```

Namun desain database dan UI harus siap untuk import/export pada sprint berikutnya.

Rekomendasi backlog:

```text
BACKLOG-SAMPLING-001
Import/Export Excel untuk Sampling Target.
```

Alasan:

- Manual input cukup untuk membuktikan workflow.
- Import Excel penting, tetapi lebih aman setelah struktur Sampling Plan disetujui.

## 10. Konsekuensi

### Positif

- Nama modul lebih sesuai proses bisnis.
- Tidak tertukar dengan database responden.
- Mendukung Pattern A dan Pattern B.
- Fieldwork dan Monitoring mendapat dasar target yang jelas.

### Negatif

- Desain sedikit lebih kompleks karena ada Sample Group dan Sampling Target.
- UI perlu menampilkan hierarchy group dan wilayah.

### Netral

- Database responden tetap menjadi modul terpisah.
- Advanced sampling algorithm tetap out of scope.

## 11. Final Recommendation

Gunakan nama:

```text
Sampling Plan
```

Untuk MVP:

```text
Project
  -> Sample Group
       -> Sampling Target
```

Relasi ke Questionnaire:

```text
Sample Group many-to-one Questionnaire optional saat Draft, wajib sebelum Fieldwork.
```

Keputusan ini membuat ResearchAI siap mendukung dua pola bisnis Beerka tanpa mencampur Sampling Plan dengan database responden.
