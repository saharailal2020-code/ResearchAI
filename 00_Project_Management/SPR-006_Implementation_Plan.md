# SPR-006 Implementation Plan

Nama Sprint:
Project Management - Review Setup Project

Status:
Draft for Product Owner Review

Basis:

- WF-003 Setup Project
- WF-004 Project Setup Review
- ADR-001 Proposal to Project
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1

## 1. Tujuan Sprint

Membangun fondasi UI/UX dan workflow implementasi untuk halaman Review Setup Project.

Sprint ini bertujuan memastikan transisi dari Proposal `Approved` ke Project dilakukan secara sadar melalui halaman review, bukan otomatis dan bukan popup.

Alur yang dituju:

```text
Proposal Detail -> Setup Project -> Review Setup Project -> Buat Project -> Project Detail / Project Setup
```

## 2. Scope

Masuk scope Sprint 6:

- Menambahkan action `Setup Project` pada Proposal Detail untuk Proposal `Approved`.
- Membuat halaman Review Setup Project.
- Menampilkan Ringkasan Proposal.
- Menampilkan Ringkasan Client.
- Menampilkan field Project Name dengan default dari Proposal Title.
- Menampilkan Informasi Sistem.
- Menampilkan Checklist Data.
- Menampilkan tombol `Batal`.
- Menampilkan tombol `Buat Project`.
- Menampilkan loading state.
- Menampilkan error state.
- Menangani success flow setelah Project dibuat.

Scope yang tergantung backend:

- Membuat Project dari Proposal.
- Mencegah Project ganda.
- Membuat Project Number otomatis.
- Mencatat Activity `Project dibuat dari Proposal`.

Tidak masuk scope:

- Project List lengkap.
- Project Detail lengkap.
- Project Status Actions.
- Questionnaire.
- Sampling.
- Fieldwork.
- QC.
- Dataset.
- Dashboard.
- Report.
- Invoice.
- Contract.
- Quotation.
- Payment.
- Assignment team.
- Timeline detail.

## 3. Workflow Implementasi

```text
User membuka Proposal Detail
  |
  v
Jika status Approved dan belum ada Project:
  tampilkan action Setup Project
  |
  v
User klik Setup Project
  |
  v
Frontend membuka /proposals/:proposalId/setup-project
  |
  v
Frontend load Proposal dan Client
  |
  v
User review checklist dan Project Name
  |
  v
User klik Buat Project
  |
  v
Backend membuat Project
  |
  v
Frontend redirect ke Project Detail / Project Setup
```

## 4. Komponen Frontend

File atau komponen yang kemungkinan disentuh saat implementasi:

- `frontend/src/App.jsx`
- `frontend/src/pages/ProposalDetailPage.jsx`
- `frontend/src/pages/ProjectSetupReviewPage.jsx`
- `frontend/src/services/proposals.js`
- `frontend/src/services/projects.js`
- `frontend/src/services/clients.js`

Routing yang disarankan:

```text
/proposals/:proposalId/setup-project
```

Future route setelah sukses:

```text
/projects/:projectId
```

Jika Project Detail belum tersedia:

```text
/projects/:projectId/setup
```

atau placeholder:

```text
/projects/:projectId
```

## 5. Komponen Backend

Backend kemungkinan perlu fondasi Project sebelum frontend bisa selesai penuh.

Candidate endpoint:

```text
POST /api/v1/proposals/{proposal_id}/setup-project
```

Expected behavior:

- Validasi user login.
- Validasi Proposal ditemukan.
- Validasi Proposal status `Approved`.
- Validasi Client Proposal valid.
- Validasi belum ada Project untuk Proposal tersebut.
- Membuat Project Number otomatis.
- Membuat Project dengan status awal `Setup`.
- Menyimpan `client_id`.
- Menyimpan `proposal_id`.
- Menyimpan `project_name`.
- Menyimpan `research_type`.
- Menyimpan `project_value` dari estimated budget jika tersedia.
- Menyimpan `business_development_owner_id` dari Proposal Owner jika tersedia.
- Mencatat Activity `Project dibuat dari Proposal`.
- Mengembalikan Project response.

Idempotency:

- Jika Project sudah ada, backend mengembalikan Project existing atau error terstruktur yang menyertakan `project_id`.
- Backend harus aman dari double click.

## 6. API

API yang digunakan frontend:

```text
GET /api/v1/proposals/{proposal_id}
GET /api/v1/clients/{client_id}
POST /api/v1/proposals/{proposal_id}/setup-project
```

Candidate payload:

```json
{
  "project_name": "Customer Satisfaction Survey 2026"
}
```

Candidate response:

```json
{
  "id": "uuid",
  "project_number": "PRJ-20260726-0001",
  "client_id": "uuid",
  "proposal_id": "uuid",
  "project_name": "Customer Satisfaction Survey 2026",
  "research_type": "Customer Satisfaction",
  "project_value": 25000000,
  "status": "Setup",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 7. UI Layout

Desktop layout:

```text
Breadcrumb
Proposal / Proposal Detail / Setup Project

Header
Setup Project
Review data proposal sebelum membuat project operasional.

Main grid
Left:
- Ringkasan Proposal
- Ringkasan Client
- Project Information

Right:
- Informasi Sistem
- Checklist Data
- Action Panel
```

Primary action:

- `Buat Project`

Secondary action:

- `Batal`

## 8. Validation Rules

Project Name:

- Required.
- Trim whitespace.
- Minimum 3 characters.
- Maximum 150 characters.

Proposal:

- Must exist.
- Must be `Approved`.
- Must not already have Project.

Client:

- Must exist.
- Must match Proposal Client.

## 9. Loading, Error, Success State

### Loading Page

```text
Memuat data setup project...
```

### Loading Submit

```text
Membuat Project...
```

### Error: Proposal Not Approved

```text
Project hanya dapat dibuat dari Proposal yang sudah disetujui.
```

### Error: Existing Project

```text
Project untuk proposal ini sudah tersedia.
```

### Error: Network

```text
Tidak dapat terhubung ke server.
```

### Error: General

```text
Project belum bisa dibuat. Silakan coba lagi.
```

### Success

```text
Project berhasil dibuat.
```

Redirect:

- Ke Project Detail / Project Setup Page.

## 10. Acceptance Criteria

1. Proposal Detail status `Approved` menampilkan action `Setup Project`.
2. Proposal non-Approved tidak menampilkan action `Setup Project`.
3. Klik `Setup Project` membuka halaman Review Setup Project.
4. Halaman menampilkan breadcrumb.
5. Halaman menampilkan Ringkasan Proposal.
6. Halaman menampilkan Ringkasan Client.
7. Halaman menampilkan Project Name default dari Proposal Title.
8. Project Name dapat diubah.
9. Halaman menampilkan Informasi Sistem.
10. Halaman menampilkan Checklist Data.
11. Tombol `Batal` kembali ke Proposal Detail.
12. Tombol `Buat Project` menjalankan proses setup.
13. Loading page tampil saat data dimuat.
14. Loading submit tampil saat Project dibuat.
15. Error state tampil untuk Proposal belum Approved.
16. Error state tampil untuk Project existing.
17. Error state tampil untuk backend/network error.
18. Project dibuat dengan status awal `Setup`.
19. Project Number dibuat otomatis backend.
20. Activity `Project dibuat dari Proposal` tercatat.
21. Satu Proposal tidak dapat membuat lebih dari satu Project.
22. Contract tidak diwajibkan.
23. Project Manager optional.
24. Tidak ada modul Project lain yang dibuat di luar scope.

## 11. Testing Plan

Backend testing:

- Create Project dari Proposal Approved.
- Reject Setup Project dari Proposal Draft.
- Reject Setup Project dari Proposal Sent.
- Reject Setup Project dari Proposal Revision.
- Reject Setup Project dari Proposal Rejected.
- Idempotency saat request dua kali.
- Activity logging.

Frontend testing:

- Lint.
- Build.
- Browser testing halaman Review Setup Project.
- Browser testing validation Project Name.
- Browser testing loading state.
- Browser testing error state.
- Browser testing success flow.

Regression testing:

- Login.
- Dashboard.
- Client Management.
- Proposal List.
- Proposal Detail.
- Proposal Create.
- Proposal Status Actions.
- Activity Logging.

## 12. Risiko Implementasi

### Risiko 1: Backend Project belum ada

Jika schema dan endpoint Project belum tersedia, Sprint 6 implementasi perlu dimulai dari backend foundation.

Mitigasi:

- Pisahkan Sprint 6 menjadi Backend Project Setup dan Frontend Review Setup jika terlalu besar.

### Risiko 2: Idempotency terlupakan

Jika double click membuat Project ganda, data bisnis akan rusak.

Mitigasi:

- Constraint unik pada `proposal_id`.
- Backend check existing Project.
- Frontend disable tombol saat submit.

### Risiko 3: Project Detail belum siap

Jika Project berhasil dibuat tetapi halaman tujuan belum tersedia, user bisa bingung.

Mitigasi:

- Buat Project Detail placeholder minimal.
- Atau arahkan ke Project Setup placeholder yang menjelaskan status.

### Risiko 4: Data mapping berubah

Jika field Proposal belum lengkap, mapping ke Project bisa parsial.

Mitigasi:

- Mapping hanya data yang tersedia.
- Field operasional dilengkapi pada sprint Project Management berikutnya.

### Risiko 5: Permission belum matang

MVP belum memiliki permission granular.

Mitigasi:

- Gunakan Administrator dan Proposal Owner sebagai rule awal.
- Catat permission granular sebagai backlog.

## 13. Estimasi Pekerjaan

Estimasi jika backend Project belum tersedia:

- Backend schema Project dan migration: 0.5 hari.
- Backend service Setup Project dan idempotency: 0.5 hari.
- Backend API dan schema response: 0.5 hari.
- Backend tests/API verification: 0.5 hari.
- Frontend route dan page: 0.5 hari.
- Frontend UI states dan validation: 0.5 hari.
- Browser testing dan regression: 0.5 hari.

Total estimasi:

```text
3 sampai 4 hari kerja
```

Estimasi jika backend Project sudah tersedia:

```text
1.5 sampai 2 hari kerja
```

## 14. Rekomendasi Sprint Berikutnya

Sebelum implementasi, lakukan Product Owner Review terhadap WF-004 dan SPR-006.

Jika disetujui, rekomendasi implementasi bertahap:

1. Project backend foundation.
2. Setup Project API.
3. Review Setup Project frontend.
4. Browser testing.
5. Product Owner Review.
6. Commit setelah approval.
