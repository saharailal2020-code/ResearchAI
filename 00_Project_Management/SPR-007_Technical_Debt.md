# Sprint 7 Technical Debt

Nama Sprint:
Questionnaire Foundation MVP

Tanggal:
26 Juli 2026

## High Priority

### TD-007-001 Database Migration Framework

ResearchAI belum menggunakan migration framework resmi seperti Alembic.

Dampak:

- Schema versioning belum formal.
- Rollback belum tersedia.
- Perbedaan schema antar environment berisiko terjadi.

Rekomendasi:

- Kerjakan TECH-001 sebelum schema semakin kompleks.

### TD-007-002 Role-Based Access Control

Endpoint Questionnaire saat ini hanya membutuhkan user login.

Dampak:

- Belum ada pembatasan siapa yang boleh membuat, mengedit, atau menandai Ready.

Rekomendasi:

- Tambahkan permission matrix saat modul Project dan Fieldwork mulai berkembang.

## Medium Priority

### TD-007-003 URL Validation

KoBo Link dan XLSForm Link belum divalidasi sebagai URL.

Dampak:

- User dapat menyimpan teks yang bukan link valid.

Rekomendasi:

- Tambahkan validasi URL pada backend dan frontend.

### TD-007-004 Deprecated Endpoint Documentation

Endpoint singular lama masih dipertahankan tetapi belum ditandai formal sebagai deprecated di dokumentasi API.

Dampak:

- Developer bisa bingung memilih endpoint utama.

Rekomendasi:

- Tandai deprecated pada Swagger atau dokumentasi API.

### TD-007-005 Terminology Consistency

UI masih menggunakan beberapa istilah campuran seperti Questionnaire, Target Respondent, Instrument Type.

Dampak:

- User non-teknis dapat merasa istilah belum sepenuhnya konsisten.

Rekomendasi:

- Lakukan terminology review sebelum modul Questionnaire diperluas.

## Low Priority

### TD-007-006 Sort Order Management

`sort_order` sudah ada tetapi belum ada UI untuk mengubah urutan Questionnaire.

Dampak:

- Urutan masih mengikuti pembuatan.

Rekomendasi:

- Tambahkan reorder saat jumlah Questionnaire per Project mulai banyak.

### TD-007-007 Automated Frontend Test

Browser testing sudah dilakukan manual/automation-assisted, tetapi belum ada automated frontend test permanen.

Dampak:

- Regression UI masih bergantung pada pengujian manual.

Rekomendasi:

- Tambahkan test suite frontend setelah workflow Project dan Questionnaire stabil.

## Ringkasan Prioritas

| ID | Judul | Prioritas |
| --- | --- | --- |
| TD-007-001 | Database Migration Framework | High |
| TD-007-002 | Role-Based Access Control | High |
| TD-007-003 | URL Validation | Medium |
| TD-007-004 | Deprecated Endpoint Documentation | Medium |
| TD-007-005 | Terminology Consistency | Medium |
| TD-007-006 | Sort Order Management | Low |
| TD-007-007 | Automated Frontend Test | Low |
