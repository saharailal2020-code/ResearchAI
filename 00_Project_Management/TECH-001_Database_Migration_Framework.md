# TECH-001 Database Migration Framework

Status:
Backlog

Tanggal:
26 Juli 2026

Kategori:
Technical Backlog

Prioritas:
High

## 1. Latar Belakang

ResearchAI saat ini sudah memiliki beberapa domain inti:

- Client.
- Contact.
- Activity.
- Proposal.
- Project.

Pada fase awal, schema lokal masih dapat dibuat dengan SQLAlchemy `Base.metadata.create_all`. Pendekatan ini cukup untuk development awal, tetapi tidak cukup aman untuk Product Build Phase yang akan menambah banyak modul operasional seperti Questionnaire, Sample, Fieldwork, QC, Dataset, Dashboard, Report, dan Invoice.

ResearchAI membutuhkan database migration framework agar perubahan schema dapat dikelola secara terkontrol.

## 2. Tujuan

TECH-001 bertujuan menyiapkan standar migrasi database ResearchAI.

Tujuan utama:

- Menambahkan Alembic Migration.
- Menyediakan schema versioning.
- Menyediakan rollback strategy.
- Menyediakan seed data strategy.
- Menjaga environment consistency antara laptop development, staging, dan production.

## 3. Scope

Masuk scope:

- Setup Alembic.
- Membuat struktur migration folder.
- Membuat migration baseline dari schema saat ini.
- Membuat standar penamaan migration.
- Membuat panduan upgrade dan downgrade.
- Membuat strategy seed data.
- Membuat panduan environment consistency.

Tidak masuk scope:

- Mengubah schema bisnis baru.
- Membuat modul baru.
- Mengubah UI.
- Mengubah workflow produk.
- Mengubah data production tanpa approval.

## 4. Alembic Migration

Alembic akan digunakan sebagai migration framework untuk SQLAlchemy.

Target:

```text
backend/
  alembic/
    versions/
  alembic.ini
```

Command yang nantinya digunakan:

```text
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
```

Catatan:

- Autogenerate harus tetap direview manual.
- Migration tidak boleh langsung dipercaya tanpa membaca diff.
- Migration yang menghapus data harus memerlukan review khusus.

## 5. Schema Versioning

Setiap perubahan schema harus memiliki versi migration.

Standar:

- Satu migration untuk satu perubahan domain yang jelas.
- Nama migration harus menjelaskan perubahan.
- Migration harus dapat dijalankan berurutan.
- Migration harus dicatat di repository.

Contoh:

```text
20260726_001_create_projects_table.py
20260726_002_add_project_status_index.py
```

## 6. Rollback

Setiap migration harus memiliki downgrade jika memungkinkan.

Rollback harus menjawab:

- Apa yang terjadi jika migration gagal?
- Apakah data dapat dikembalikan?
- Apakah perubahan destructive?
- Apakah perlu backup sebelum dijalankan?

Kategori migration:

### Safe Migration

Contoh:

- Add nullable column.
- Add table baru.
- Add index.

### Risky Migration

Contoh:

- Drop column.
- Rename column.
- Change data type.
- Add non-null column tanpa default.

### Destructive Migration

Contoh:

- Delete table.
- Delete data.
- Merge table.

Destructive migration harus membutuhkan Product Owner dan Technical approval.

## 7. Seed Data

ResearchAI membutuhkan seed data untuk development lokal.

Seed data yang perlu distandarkan:

- Default roles.
- Default admin user.
- Master data Research Type.
- Project status.
- Proposal status.
- Sample placeholder master data pada phase berikutnya.

Aturan seed:

- Seed development boleh membuat sample data.
- Seed production hanya boleh membuat data sistem minimum.
- Password default hanya boleh untuk local development.
- Seed harus idempotent.

## 8. Environment Consistency

Migration harus membantu menjaga konsistensi environment.

Environment:

- Local development.
- Test.
- Staging.
- Production.

Standar:

- Semua environment menjalankan migration yang sama.
- Tidak ada perubahan schema manual tanpa migration.
- Status migration dapat dicek.
- Developer baru dapat setup database dari nol.

Command target:

```text
alembic current
alembic history
alembic upgrade head
```

## 9. Acceptance Criteria

TECH-001 dianggap selesai jika:

1. Alembic terpasang di backend.
2. Migration folder tersedia.
3. Baseline migration dibuat dari schema saat ini.
4. `alembic upgrade head` berhasil pada database kosong.
5. `alembic current` menampilkan versi aktif.
6. Minimal satu rollback sederhana berhasil diuji.
7. Seed data development terdokumentasi.
8. Panduan environment consistency tersedia.
9. README backend diperbarui dengan cara menjalankan migration.
10. Tidak ada perubahan schema manual tanpa migration setelah TECH-001 selesai.

## 10. Risiko

### Risiko 1: Baseline tidak cocok dengan database lokal yang sudah ada

Mitigasi:

- Audit schema existing.
- Gunakan baseline migration dengan hati-hati.
- Dokumentasikan langkah untuk database baru dan database existing.

### Risiko 2: Autogenerate membuat migration yang salah

Mitigasi:

- Review manual setiap migration.
- Jalankan migration di database test sebelum dipakai.

### Risiko 3: Rollback tidak aman

Mitigasi:

- Klasifikasikan migration safe/risky/destructive.
- Destructive migration wajib approval khusus.

### Risiko 4: Seed data membuat duplikasi

Mitigasi:

- Seed harus idempotent.
- Gunakan unique key untuk data master.

## 11. Rekomendasi Implementasi

Rekomendasi:

- TECH-001 dikerjakan sebelum modul operasional bertambah jauh.
- Idealnya dikerjakan sebelum Sprint Questionnaire dan Sample.
- Jangan digabung dengan sprint fitur besar.

Urutan implementasi TECH-001:

1. Install dan konfigurasi Alembic.
2. Hubungkan Alembic dengan SQLAlchemy metadata.
3. Buat baseline migration.
4. Uji upgrade pada database kosong.
5. Uji current/history.
6. Buat seed strategy.
7. Update backend README.
8. Product/Tech review.

## 12. Dependency

Dependency:

- SQLAlchemy models existing.
- PostgreSQL local.
- Backend config database URL.
- Docker/PostgreSQL local development.

## 13. Catatan Product Development

TECH-001 bukan fitur user-facing, tetapi sangat penting untuk menjaga ResearchAI tetap aman berkembang sebagai ERP riset.

Semakin banyak modul yang ditambahkan tanpa migration framework, semakin besar risiko environment developer dan database production tidak konsisten.
