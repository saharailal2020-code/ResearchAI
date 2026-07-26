# Domain Model v3

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Topik:
Proposal, Project, Questionnaire, Sampling Plan, Fieldwork, QC, Dataset

## 1. Perubahan Utama dari Domain Model Sebelumnya

Perubahan utama:

```text
Sample Management -> Sampling Plan
```

Alasan:

Sampling yang dimaksud dalam proses Beerka bukan database responden dan bukan daftar individual respondent.

Sampling Plan adalah rencana target survei yang sudah disepakati dengan klien, biasanya sejak Proposal.

## 2. Domain Chain

```text
Proposal
  -> Project
  -> Questionnaire
  -> Sampling Plan
  -> Fieldwork
  -> QC
  -> Dataset
```

Penjelasan:

- Proposal menyimpan janji bisnis dan target riset yang disepakati.
- Project menjalankan pekerjaan operasional.
- Questionnaire menyimpan instrumen survei.
- Sampling Plan menyimpan target survei per kelompok dan wilayah.
- Fieldwork menjalankan pengumpulan data berdasarkan Questionnaire dan Sampling Plan.
- QC memeriksa kualitas data Fieldwork.
- Dataset menyimpan data hasil yang sudah siap diproses.

## 3. Conceptual Domain Diagram

```text
Proposal
  |
  | approved
  v
Project
  |
  +-- Questionnaire
  |      id
  |      questionnaire_name
  |      target_respondent
  |      status
  |
  +-- Sampling Plan
         |
         +-- Sample Group
                id
                sample_group_name
                questionnaire_id
                status
                |
                +-- Sampling Target
                       region_type
                       region_name
                       target_sample
```

## 4. Entity Definitions

### Proposal

Tujuan:

Mencatat penawaran bisnis dan rancangan riset yang disepakati dengan client.

Hubungan:

- Proposal memiliki Client.
- Proposal Approved dapat menjadi Project.
- Proposal secara bisnis dapat memuat draft Sampling Plan.

MVP note:

- Draft Sampling Plan di Proposal belum wajib diimplementasikan.
- Sampling Plan dapat dibuat setelah Project terbentuk.

### Project

Tujuan:

Menjadi root operasional delivery riset.

Hubungan:

- Project berasal dari Proposal Approved.
- Project memiliki Questionnaire.
- Project memiliki Sampling Plan.
- Project akan memiliki Fieldwork, QC, Dataset, Report, Invoice.

### Questionnaire

Tujuan:

Menyimpan metadata instrumen survei.

Hubungan:

- Questionnaire dimiliki Project.
- Questionnaire dapat digunakan oleh satu atau banyak Sample Group.

Pattern:

```text
Questionnaire 1 -> many Sample Groups
```

### Sampling Plan

Tujuan:

Menyimpan rencana target sampling yang disepakati dengan client.

Hubungan:

- Sampling Plan dimiliki Project.
- Sampling Plan memiliki banyak Sample Group.
- Pada MVP, Sampling Plan dapat direpresentasikan langsung oleh collection Sample Group di Project.

### Sample Group

Tujuan:

Mewakili kelompok target survei.

Contoh:

- Rumah Tangga.
- UMKM.
- Bank Pengelola.
- Bank Peserta.
- Mitra.
- Non Mitra.

Hubungan:

- Sample Group dimiliki Project/Sampling Plan.
- Sample Group dapat menggunakan Questionnaire.
- Sample Group memiliki banyak Sampling Target per wilayah.
- Fieldwork progress dapat dilacak per Sample Group.

### Sampling Target

Tujuan:

Mewakili target sample berdasarkan wilayah.

Contoh:

```text
Sample Group Rumah Tangga
  - Jawa Barat: 800
  - Jawa Tengah: 650
  - Jawa Timur: 900
```

Hubungan:

- Sampling Target dimiliki Sample Group.
- Monitoring membaca target ini untuk menghitung progress.

### Fieldwork

Tujuan:

Mengelola proses pengumpulan data.

Hubungan:

- Fieldwork menggunakan Sample Group dan Sampling Target.
- Fieldwork menggunakan Questionnaire yang direferensikan oleh Sample Group.
- Fieldwork menghasilkan submission/data yang akan masuk QC.

### QC

Tujuan:

Memeriksa kualitas data hasil Fieldwork.

Hubungan:

- QC membaca data dari Fieldwork.
- QC dapat dikelompokkan berdasarkan Sample Group.
- QC menghasilkan data valid/reject untuk Dataset.

### Dataset

Tujuan:

Menyimpan data akhir atau data siap analisis.

Hubungan:

- Dataset berasal dari hasil Fieldwork yang sudah melalui QC.
- Dataset dapat dianalisis untuk Dashboard dan Report.

## 5. Pattern A - Banyak Questionnaire

```text
Project STKU
  |
  +-- Questionnaire Rumah Tangga
  +-- Questionnaire UMKM
  +-- Questionnaire Bank Pengelola
  +-- Questionnaire Bank Peserta
  |
  +-- Sample Group Rumah Tangga
  |      questionnaire_id -> Questionnaire Rumah Tangga
  |
  +-- Sample Group UMKM
  |      questionnaire_id -> Questionnaire UMKM
  |
  +-- Sample Group Bank Pengelola
  |      questionnaire_id -> Questionnaire Bank Pengelola
  |
  +-- Sample Group Bank Peserta
         questionnaire_id -> Questionnaire Bank Peserta
```

Makna:

- Masing-masing kelompok memiliki instrumen sendiri.

## 6. Pattern B - Satu Questionnaire untuk Banyak Sample Group

```text
Project Kepuasan
  |
  +-- Questionnaire Kepuasan
  |
  +-- Sample Group Mitra
  |      questionnaire_id -> Questionnaire Kepuasan
  |
  +-- Sample Group Non Mitra
         questionnaire_id -> Questionnaire Kepuasan
```

Makna:

- Instrumen sama.
- Kelompok target berbeda.
- Monitoring tetap dipisahkan per Sample Group.

## 7. Entity Relationship MVP

```text
Project 1 -> many Questionnaire
Project 1 -> many SampleGroup
Questionnaire 1 -> many SampleGroup
SampleGroup 1 -> many SamplingTarget
SampleGroup 1 -> many FieldworkRecord future
Fieldwork 1 -> many QCRecord future
QC 1 -> Dataset future
```

## 8. Proposed Tables MVP

### sample_groups

Purpose:

Menyimpan kelompok target sampling.

Fields:

- id.
- project_id.
- questionnaire_id nullable.
- sample_group_name.
- target_respondent.
- total_target_sample.
- status.
- notes.
- sort_order.
- created_by.
- ready_at.
- created_at.
- updated_at.

### sampling_targets

Purpose:

Menyimpan target sample per wilayah.

Fields:

- id.
- sample_group_id.
- region_type.
- region_name.
- target_sample.
- sort_order.
- created_at.
- updated_at.

## 9. Why Not Respondent Database

Sampling Plan tidak menyimpan:

- Nama responden.
- Nomor HP responden.
- Alamat responden.
- Identitas individual responden.
- Status wawancara per responden.

Data tersebut masuk modul berbeda:

```text
Respondent Database / Sample Frame
```

Modul itu dapat dirancang setelah Sampling Plan MVP stabil.

## 10. Business Rule Summary

1. Sampling Plan adalah bagian dari kesepakatan riset.
2. Sampling Plan dapat dibuat setelah Project terbentuk pada MVP.
3. Sample Group adalah target survei, bukan daftar responden.
4. Sampling Target adalah target wilayah.
5. Questionnaire tidak selalu 1:1 dengan Sample Group.
6. Sample Group dapat memakai Questionnaire yang sama.
7. Fieldwork harus mengacu pada Sampling Plan.
8. Monitoring menghitung progress terhadap Sampling Target.
9. QC dan Dataset mengikuti data hasil Fieldwork.

## 11. Recommendation

Domain Model v3 harus menjadi baseline untuk Sprint 8 Review.

Nama modul:

```text
Sampling Plan
```

Entity utama:

```text
Sample Group
Sampling Target
```

Database responden:

```text
Out of scope MVP Sampling Plan.
```
