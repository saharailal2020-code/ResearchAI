# SPR-005 Implementation Plan

Nama Sprint:
Proposal Management - Create Proposal

Status:
Draft for Product Owner Review

Basis:

- WF-001 Proposal Workflow MVP v0.1
- WF-002 Proposal Create
- ADR-002 Proposal vs Project
- Domain Model v1

## 1. Tujuan Sprint

Membangun Proposal Create Page agar Business Development dapat membuat Draft Proposal dari frontend secara cepat dan konsisten.

Sprint ini melengkapi Proposal Management yang sudah memiliki:

- Proposal List
- Proposal Detail
- Proposal Status Actions

Setelah Sprint 5 selesai, user dapat membuat Proposal baru dari UI dan langsung melanjutkan workflow melalui Proposal Detail.

## 2. Scope

Masuk scope:

- Mengaktifkan tombol `+ Proposal Baru`.
- Membuat halaman Proposal Create.
- Menampilkan daftar Client untuk dipilih.
- Menampilkan form minimum:
  - Client
  - Proposal Title
  - Research Type
  - Estimasi Nilai Proposal (Rp)
- Validasi form.
- Submit sebagai `Simpan Draft`.
- Menggunakan endpoint create proposal yang sudah tersedia.
- Redirect ke Proposal Detail setelah berhasil.
- Loading state.
- Error state.
- Empty state jika belum ada Client.
- Browser testing dan regression testing.

Tidak masuk scope:

- Edit Proposal.
- Upload attachment.
- Internal Note.
- Kirim ke Client langsung dari create page.
- Status Action baru.
- Setup Project.
- Project.
- Quotation.
- Contract.

## 3. Komponen Frontend

Komponen atau file yang kemungkinan disentuh pada sprint implementasi:

- `frontend/src/App.jsx`
- `frontend/src/pages/ProposalsPage.jsx`
- `frontend/src/pages/ProposalCreatePage.jsx`
- `frontend/src/services/proposals.js`
- `frontend/src/services/clients.js` jika diperlukan

Routing yang disarankan:

```text
/proposals/new
```

Navigasi:

```text
Proposal List -> + Proposal Baru -> Proposal Create -> Proposal Detail
```

## 4. Backend

Backend idealnya tidak perlu perubahan jika endpoint berikut sudah tersedia:

```text
POST /api/v1/proposals
```

Expected behavior:

- Membuat `proposal_number` otomatis.
- Mengisi `proposal_owner_id` otomatis dari current user.
- Mengisi status awal `Draft`.
- Mencatat activity `Proposal dibuat`.
- Mengembalikan Proposal Detail response.

Jika ditemukan gap backend saat implementasi, hentikan dan laporkan untuk review Product Owner sebelum mengubah backend.

## 5. API

API yang digunakan:

```text
GET /api/v1/clients
POST /api/v1/proposals
```

Payload create proposal:

```json
{
  "client_id": "uuid",
  "proposal_title": "Customer Satisfaction Survey 2026",
  "research_type": "Customer Satisfaction",
  "estimated_budget": 25000000
}
```

Response yang dibutuhkan:

```json
{
  "id": "uuid",
  "proposal_number": "PROP-YYYYMMDD-0001",
  "client_id": "uuid",
  "proposal_owner": {
    "id": "uuid",
    "full_name": "ResearchAI Admin",
    "email": "admin@researchai.local"
  },
  "proposal_title": "Customer Satisfaction Survey 2026",
  "research_type": "Customer Satisfaction",
  "estimated_budget": 25000000,
  "status": "Draft",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 6. UI Layout

Layout desktop:

```text
Breadcrumb
Proposal / Proposal Baru

Header
Proposal Baru
Buat draft proposal baru untuk client.

Main grid
Left: Form
Right: Informasi Sistem
```

Form section:

- Informasi Utama
- Ringkasan Riset
- Action Buttons

System card:

- Proposal Number: dibuat otomatis
- Proposal Owner: user saat ini
- Status: Draft

## 7. Validation Rules

Client:

- Required.
- Must be selected from client list.

Proposal Title:

- Required.
- Trim whitespace.
- Minimum 3 characters.
- Maximum 150 characters.

Research Type:

- Optional.
- Tidak menggunakan free text.
- Menggunakan dropdown dari master data.
- Untuk MVP, daftar master data boleh statis di frontend.
- Pada sprint berikutnya, master data dapat dipindahkan ke konfigurasi atau backend.

Opsi dropdown MVP:

- Quantitative
- Qualitative
- Mystery Shopping
- FGD
- IDI
- Desk Research
- Market Assessment
- Customer Satisfaction
- Brand Health
- Tracking
- Social Research
- Other

Estimasi Nilai Proposal (Rp):

- Optional.
- Numeric.
- Cannot be negative.
- Empty value sent as `null` or omitted.

## 8. Loading, Error, Empty State

Loading client list:

```text
Memuat daftar client...
```

Saving draft:

```text
Menyimpan...
```

Client list error:

```text
Daftar client belum bisa dimuat. Pastikan backend sedang berjalan.
```

Create error:

```text
Proposal belum bisa disimpan. Silakan coba lagi.
```

No client empty state:

```text
Belum ada client. Buat client terlebih dahulu sebelum membuat proposal.
```

## 9. Acceptance Criteria

1. Tombol `+ Proposal Baru` di Proposal List membuka Proposal Create Page.
2. Proposal Create Page memiliki breadcrumb `Proposal / Proposal Baru`.
3. User dapat memilih Client.
4. User dapat mengisi Proposal Title.
5. User dapat memilih Research Type dari dropdown.
6. User dapat mengisi Estimasi Nilai Proposal (Rp).
7. Client wajib dipilih.
8. Proposal Title wajib diisi.
9. Estimasi Nilai Proposal (Rp) tidak boleh negatif.
10. Proposal Number tidak dapat diisi manual.
11. Proposal Owner tidak dapat dipilih manual.
12. Status tidak dapat dipilih manual.
13. Klik `Simpan Draft` membuat Proposal berstatus Draft.
14. Setelah berhasil, user diarahkan ke Proposal Detail.
15. Proposal Detail menampilkan Proposal baru.
16. Activity `Proposal dibuat` tercatat di Client Activity Timeline.
17. Empty state tampil jika belum ada Client.
18. Loading state tampil saat data dimuat atau draft disimpan.
19. Error state tampil jika load atau submit gagal.
20. Tidak membuat Project.
21. Tidak membuat Quotation.
22. Tidak membuat Contract.
23. Frontend lint berhasil.
24. Frontend build berhasil.
25. Browser testing berhasil.
26. Regression testing berhasil.

## 10. Regression Testing

Minimal regression:

- Login.
- Dashboard.
- Client Management.
- Client Detail.
- Proposal List.
- Proposal Detail.
- Proposal Status Actions.
- Proposal Create.
- Activity Logging.

## 11. Risiko

### Risiko 1: User mengira proposal sudah dikirim ke client

Mitigasi:

- Gunakan tombol `Simpan Draft`.
- Jangan gunakan label `Submit`.
- Setelah create, arahkan ke Proposal Detail dengan status Draft.

### Risiko 2: Client belum tersedia

Mitigasi:

- Empty state jelas.
- Arahkan user kembali ke Client Management.

### Risiko 3: Format estimasi nilai proposal membingungkan

Mitigasi:

- Input boleh angka sederhana.
- Display setelah tersimpan memakai format Rupiah.

### Risiko 4: Backend response tidak sesuai kebutuhan redirect

Mitigasi:

- Pastikan response create mengembalikan `id`.
- Jika tidak, hentikan implementasi dan review backend.

### Risiko 5: Scope melebar ke edit/status/project

Mitigasi:

- Sprint 5 hanya create draft.
- Status action tetap di Proposal Detail.
- Setup Project tetap ditunda.

## 12. Estimasi

Estimasi:
1 hari kerja.

Breakdown:

- Review endpoint dan existing UI: 0.25 hari.
- Implementasi page dan route: 0.25 hari.
- Validasi dan state handling: 0.25 hari.
- Browser testing dan regression: 0.25 hari.

## 13. Definition of Done

- Design Review disetujui Product Owner.
- Implementation mengikuti WF-002.
- Tidak ada perubahan database.
- Tidak ada Project, Quotation, atau Contract.
- Proposal baru dapat dibuat dari UI.
- Activity logging berhasil.
- Lint dan build berhasil.
- Browser testing berhasil.
- Product Owner Review selesai sebelum commit.
