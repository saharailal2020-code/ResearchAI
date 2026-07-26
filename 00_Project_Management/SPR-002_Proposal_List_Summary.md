# Sprint Implementasi 2

Nama Sprint:
Proposal Management - Proposal List

## Tujuan Sprint

Membangun halaman Proposal List sebagai entry point Proposal Management sesuai baseline WF-001 Proposal Workflow MVP v0.1.

Sprint ini fokus pada tampilan daftar proposal, navigasi dari sidebar, filtering, search, sorting, empty state, dan placeholder awal Proposal Detail. Sprint ini tidak membuat Proposal Form, tidak mengubah workflow backend, dan tidak membuat Project, Quotation, atau Contract.

## Fitur yang berhasil diselesaikan

- Menu Proposal ditambahkan ke sidebar aplikasi.
- Halaman Proposal List dibuat sebagai entry point Proposal Management.
- Proposal List menggunakan data dari backend yang sudah tersedia.
- Tabel Proposal menampilkan:
  - Proposal Number
  - Proposal Title
  - Client
  - Research Type
  - Estimated Budget
  - Proposal Owner
  - Status
  - Created Date
- Search proposal tersedia.
- Filter tersedia untuk:
  - Status
  - Client
  - Research Type
- Sorting tersedia untuk:
  - Created Date
  - Estimated Budget
  - Status
- Tombol "+ Proposal Baru" ditempatkan sebagai primary action di kanan atas.
- Klik proposal membuka halaman Proposal Detail Placeholder.
- Empty State ditampilkan ketika tidak ada data proposal.
- UI Polish Sprint 2.1 selesai:
  - Toolbar dibuat lebih compact.
  - Badge status proposal dibuat konsisten.
  - Proposal Number dibuat lebih mudah dikenali dengan font semibold.
  - Spacing disesuaikan dengan Client Management.

## File yang berubah

- `frontend/src/App.jsx`
- `frontend/src/layouts/AppLayout.jsx`
- `frontend/src/pages/ProposalsPage.jsx`
- `frontend/src/pages/ProposalDetailPage.jsx`
- `00_Project_Management/AUTH-001_Login_Error_Message_Backlog.md`

## Endpoint yang digunakan

- `GET /api/v1/proposals`
- `GET /api/v1/clients`

Endpoint proposal digunakan untuk menampilkan daftar proposal.
Endpoint client digunakan untuk filter client dan pemetaan nama client pada Proposal List.

## Testing yang dilakukan

- Frontend lint berhasil.
- Frontend build berhasil.
- Browser testing berhasil.
- Proposal List dengan data berhasil ditampilkan.
- Proposal List empty state berhasil ditampilkan.
- Search berhasil diuji.
- Filter status berhasil diuji.
- Sorting berhasil diuji.
- Proposal Detail Placeholder berhasil dibuka dari klik proposal.

## Regression testing

- Backend `/health` = OK.
- Login admin berhasil.
- Dashboard berhasil dibuka.
- Client Management tetap berfungsi.
- Proposal List tetap berfungsi.
- Proposal Detail Placeholder tetap berfungsi.
- Backend tetap aktif selama browser testing.
- Frontend tetap aktif selama browser testing.

## Backlog yang dihasilkan

### AUTH-001

Judul:
Perbaikan pesan login ketika backend tidak dapat dihubungi.

Status:
Backlog, tidak dikerjakan pada Sprint 2.

Acceptance Criteria:

- HTTP 401 menampilkan pesan: "Email atau password salah."
- Network Error atau Backend Down menampilkan pesan: "Tidak dapat terhubung ke server."
- Error lain menampilkan pesan: "Terjadi kesalahan. Silakan coba lagi."

## Catatan Product Owner

Product Owner Review menyetujui hasil Sprint Implementasi 2 beserta Sprint 2.1 UI Polish.

Acceptance criteria dinyatakan terpenuhi.

Commit yang dibuat:

`368048b feat(proposal): implement proposal management list`

Push ke branch `main` berhasil.
