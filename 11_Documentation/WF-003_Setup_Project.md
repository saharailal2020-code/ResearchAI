# WF-003 Setup Project

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- WF-001 Proposal Workflow MVP v0.1
- WF-002 Proposal Create
- ADR-001 Proposal to Project
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1
- Product Owner Decision Sprint A0

## 1. Tujuan Workflow

Workflow Setup Project merancang transisi dari Proposal yang sudah `Approved` menjadi Project operasional.

Tujuan utama:

- Memastikan Project hanya dibuat dari Proposal yang valid.
- Menjaga Proposal sebagai historical record.
- Menyalin data awal yang relevan dari Proposal ke Project.
- Mencegah Project dibuat lebih dari satu kali dari Proposal yang sama pada MVP.
- Menyiapkan Project agar dapat masuk lifecycle:

```text
Setup -> Ready -> Fieldwork -> QC -> Analysis -> Reporting -> Completed
```

Dengan status tambahan:

```text
Cancelled
```

## 2. Trigger Setup Project

Setup Project dimulai dari Proposal Detail.

Trigger utama:

```text
User membuka Proposal Detail
  |
  v
Proposal status = Approved
  |
  v
Tombol Setup Project tampil
  |
  v
User klik Setup Project
  |
  v
Sistem membuat Project dengan status awal Setup
```

Action `Setup Project` tidak boleh otomatis berjalan saat Proposal berubah menjadi `Approved`.

## 3. Hak Akses

Untuk MVP, hak akses dibuat sederhana.

Role yang boleh melakukan Setup Project:

- Administrator.
- Business Development Owner dari Proposal.
- User internal yang diberi permission Project Setup pada phase berikutnya.

Rule MVP:

- User harus login.
- User harus memiliki akses ke Proposal.
- Proposal harus berada pada status `Approved`.
- Jika permission granular belum tersedia, Administrator dan Proposal Owner boleh melakukan Setup Project.

Role yang tidak boleh:

- Client.
- External vendor.
- User yang tidak memiliki akses ke Client atau Proposal.

## 4. Business Rules

### Rule Proposal

1. Proposal wajib memiliki Client.
2. Proposal wajib memiliki Proposal Number.
3. Proposal harus berstatus `Approved`.
4. Proposal `Draft`, `Sent`, `Revision`, dan `Rejected` tidak dapat melakukan Setup Project.
5. Proposal tetap menjadi historical record setelah Project dibuat.
6. Proposal tidak berubah menjadi Project.
7. Proposal tidak boleh otomatis membuat Project saat status berubah menjadi `Approved`.

### Rule Project

1. Project wajib memiliki Client.
2. Project wajib menyimpan referensi ke Proposal asal.
3. Untuk MVP, satu Proposal maksimal menghasilkan satu Project.
4. Project status awal adalah `Setup`.
5. Project Number dibuat otomatis oleh backend.
6. Project tidak wajib memiliki Project Manager pada MVP.
7. Start Date dan End Date tidak wajib pada MVP.
8. Contract bersifat opsional pada MVP.

### Rule Setelah Project Dibuat

Setelah Project dibuat, Proposal tidak read-only total.

Field Proposal yang tidak boleh diubah:

- Client.
- Proposal Title.
- Research Type.
- Objective.
- Methodology.
- Budget Estimation.

Field Proposal yang masih boleh diubah:

- Attachment.
- Internal Note.

Proposal Detail harus menampilkan bahwa Project sudah dibuat dan menyediakan link ke Project Detail ketika modul Project tersedia.

## 5. Data Mapping Proposal ke Project

Data yang diwariskan sebagai nilai awal:

| Proposal | Project | Catatan |
| --- | --- | --- |
| `client_id` | `client_id` | Wajib sama |
| `id` | `proposal_id` | Referensi asal |
| `proposal_title` | `project_name` | Nilai awal, dapat dikunci sesuai rule |
| `research_type` | `research_type` | Nilai awal |
| `research_objective` | `project_objective` | Jika field sudah tersedia |
| `methodology_summary` | `methodology_summary` | Jika field sudah tersedia |
| `estimated_budget` | `project_value` | Nilai awal, bukan nilai invoice final |
| `proposal_owner_id` | `business_development_owner_id` | Referensi BD, bukan Project Manager |
| `approved_at` | `approved_at` | Referensi approval, bukan start date |

Data yang tidak diwariskan otomatis:

- Proposal Number menjadi Project Number.
- Proposal Status menjadi Project Status.
- Proposal Owner menjadi Project Manager.
- Proposal Activity menjadi Project Activity.
- Approved Date menjadi Start Date.
- Estimated Budget menjadi Invoice Final.
- Attachment Proposal menjadi Attachment Project tanpa Document Management.
- Quotation.
- Contract.
- Invoice.
- Payment Terms.

## 6. UI Flow

### Dari Proposal Detail

```text
Proposal Detail
  |
  | Jika status Approved dan belum ada Project
  v
Card "Ready for Project Setup"
  |
  v
Button "Setup Project"
  |
  v
Review Setup Project
  |
  v
Confirm Setup Project
  |
  v
Project dibuat
  |
  v
Project Detail / Project Setup Page
```

### Review Setup Project

Sebelum Project dibuat, user melihat ringkasan:

- Proposal Number.
- Proposal Title.
- Client.
- Research Type.
- Estimasi Nilai Proposal.
- Proposal Owner.
- Status Project awal: `Setup`.

Untuk MVP, form Setup Project sebaiknya tetap ringan.

Field yang boleh muncul:

- Project Name, prefilled dari Proposal Title.
- Project Notes, optional.

Field yang ditunda:

- Project Manager.
- Start Date.
- End Date.
- Contract.
- Detailed timeline.
- Team assignment.

## 7. Error Handling

Error yang perlu ditangani:

### Proposal belum Approved

Pesan:

```text
Project hanya dapat dibuat dari Proposal yang sudah disetujui.
```

### Project sudah pernah dibuat

Pesan:

```text
Project untuk proposal ini sudah tersedia.
```

Action:

- Tampilkan link ke Project yang sudah ada.
- Jangan membuat Project baru.

### Proposal tidak ditemukan

Pesan:

```text
Proposal tidak ditemukan.
```

### Client tidak valid

Pesan:

```text
Client pada proposal tidak valid.
```

### Backend gagal membuat Project

Pesan:

```text
Project belum bisa dibuat. Silakan coba lagi.
```

### Network Error

Pesan:

```text
Tidak dapat terhubung ke server.
```

## 8. Idempotency

Idempotency wajib dipikirkan sejak MVP agar Project tidak dibuat dua kali.

Business rule:

- Satu Proposal maksimal memiliki satu Project pada MVP.

Strategi backend:

1. Tambahkan constraint unik pada `projects.proposal_id`.
2. Saat action `Setup Project` dipanggil, backend cek apakah Project dengan `proposal_id` sudah ada.
3. Jika sudah ada, backend mengembalikan Project existing, bukan membuat Project baru.
4. Endpoint harus aman jika user double click.
5. Frontend harus menampilkan loading state dan disable tombol saat request sedang berjalan.

Expected behavior:

```text
Klik pertama -> Project dibuat
Klik kedua -> Project existing dikembalikan
```

## 9. Activity Logging

Activity tetap menjadi cross-cutting behavior.

Event yang perlu dicatat:

- `Project dibuat dari Proposal`.

Event ditulis oleh backend service.

Activity masuk ke:

- Client Activity Timeline.
- Future Project Activity Timeline jika modul Project sudah tersedia.

Contoh activity:

```text
Project dibuat dari Proposal PROP-20260726-0001.
```

## 10. Acceptance Criteria

1. Tombol `Setup Project` hanya muncul pada Proposal status `Approved`.
2. Tombol `Setup Project` tidak muncul pada status:
   - Draft.
   - Sent to Client.
   - Revision.
   - Rejected.
3. User login dapat menjalankan Setup Project sesuai hak akses MVP.
4. Project dibuat dengan status awal `Setup`.
5. Project memiliki `client_id`.
6. Project memiliki `proposal_id`.
7. Project Number dibuat otomatis.
8. Data awal Project terisi dari Proposal sesuai data mapping.
9. Satu Proposal tidak dapat membuat lebih dari satu Project.
10. Jika Project sudah ada, sistem menampilkan Project existing.
11. Activity `Project dibuat dari Proposal` tercatat dari backend service.
12. Setelah sukses, user diarahkan ke Project Detail atau Project Setup Page.
13. Proposal tetap dapat dibuka sebagai historical record.
14. Tidak ada Quotation, Contract, Invoice, atau Payment yang dibuat otomatis.

## 11. Risiko

### Risiko 1: Boundary Proposal dan Project menjadi kabur

Jika terlalu banyak field operasional dimasukkan ke Proposal, Proposal akan menjadi terlalu berat.

Mitigasi:

- Proposal tetap fokus pada penawaran.
- Detail operasional masuk ke Project.

### Risiko 2: Project dibuat dua kali

Double click atau retry request dapat membuat duplikasi Project.

Mitigasi:

- Constraint unik pada `proposal_id`.
- Backend idempotent.
- Tombol loading dan disabled di frontend.

### Risiko 3: Data Proposal belum cukup lengkap

Proposal MVP saat ini masih minimal.

Mitigasi:

- Project tetap bisa dibuat dengan data minimum.
- Field tambahan dapat dilengkapi di Project Setup.

### Risiko 4: Hak akses belum granular

Permission module belum lengkap pada MVP.

Mitigasi:

- Gunakan rule sederhana: Administrator dan Proposal Owner.
- Catat kebutuhan permission granular sebagai backlog.

### Risiko 5: Contract belum menjadi gate

Pada MVP, Contract opsional sehingga Project dapat dibuat dari Approved Proposal tanpa Contract.

Mitigasi:

- Catat future consideration untuk Contract Gate.

## 12. Open Questions untuk Product Owner

1. Pada MVP, setelah klik `Setup Project`, apakah user langsung masuk Project Detail atau masuk halaman Project Setup Form terlebih dahulu?
2. Apakah Project Name boleh diedit saat Setup Project, atau harus selalu sama dengan Proposal Title pada MVP?
3. Apakah Project Number perlu memiliki format khusus sejak MVP?
4. Jika Proposal Approved tetapi Contract belum ada, apakah tetap boleh Setup Project?
5. Apakah Business Development Owner otomatis tetap terhubung ke Project sebagai referensi komersial?
6. Apakah Project Setup perlu memilih Team atau cukup ditunda sampai Project Management sprint berikutnya?
7. Jika Proposal diubah setelah Project dibuat, apakah perubahan Attachment dan Internal Note perlu masuk Activity Timeline?

## 13. Rekomendasi Awal

Rekomendasi untuk MVP:

1. Setup Project dibuat sebagai action di Proposal Detail pada status `Approved`.
2. Setelah klik Setup Project, tampilkan halaman Review Setup Project sederhana sebelum confirm.
3. Project status awal adalah `Setup`.
4. Project Manager, Start Date, End Date, Team, dan Contract tidak wajib.
5. Backend harus idempotent sejak awal.
6. Activity `Project dibuat dari Proposal` wajib dicatat dari backend.
7. Sprint berikutnya sebaiknya dimulai dari Project backend foundation sebelum frontend Project Detail dibuat.
