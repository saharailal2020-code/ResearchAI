# SPR-005 Proposal Create Summary

Nama Sprint:
Proposal Management - Proposal Create

## Tujuan Sprint

Membangun halaman Proposal Create agar Business Development dapat membuat Draft Proposal baru secara cepat sesuai WF-002 Proposal Create.

Sprint ini melengkapi alur Proposal Management MVP:

```text
Proposal List -> Proposal Baru -> Proposal Detail -> Status Actions
```

## Scope

Masuk scope:

- Membuat halaman Proposal Create.
- Menambahkan route `Proposal / Proposal Baru`.
- Menghubungkan tombol `+ Proposal Baru` dari Proposal List ke halaman create.
- Mengambil daftar Client dari backend.
- Mengirim request Create Proposal ke backend.
- Mengarahkan user ke Proposal Detail setelah Draft berhasil dibuat.
- Menampilkan validasi field wajib.
- Menampilkan loading state, error state, dan empty state.
- Menggunakan dropdown Research Type statis sesuai Design Freeze.
- Menampilkan Informasi Sistem dalam bentuk read-only.

Tidak masuk scope:

- Edit Proposal.
- Setup Project.
- Client Contact Integration.
- Attachment.
- Internal Note.
- Research Objective.
- Methodology Summary.
- Timeline.
- Quotation.
- Contract.

## Fitur yang selesai

- Breadcrumb `Proposal / Proposal Baru`.
- Header `Proposal Baru`.
- Section `Informasi Proposal`.
- Field Client dengan dropdown dari API Client.
- Field Proposal Title.
- Field Research Type dengan dropdown statis.
- Field `Estimasi Nilai Proposal (Rp)`.
- Preview nilai Rupiah saat user mengisi estimasi nilai proposal.
- Section `Informasi Sistem` read-only:
  - Proposal Number: dibuat otomatis.
  - Proposal Owner: user login.
  - Status: Draft.
  - Created Date: setelah disimpan.
  - Updated Date: setelah disimpan.
- Tombol `Simpan Draft`.
- Tombol `Batal`.
- Redirect ke Proposal Detail setelah sukses.
- Validasi:
  - Client wajib dipilih.
  - Proposal Title wajib diisi.
  - Proposal Title minimal 3 karakter.
  - Estimasi nilai proposal tidak boleh negatif.
- Error handling jika daftar Client gagal dimuat.
- Empty state jika belum ada Client.
- Loading state saat daftar Client dimuat dan saat Draft disimpan.

## File yang berubah

- `frontend/src/App.jsx`
- `frontend/src/pages/ProposalsPage.jsx`
- `frontend/src/pages/ProposalCreatePage.jsx`
- `frontend/src/services/proposals.js`

## Endpoint yang digunakan

- `GET /api/v1/clients`
- `POST /api/v1/proposals`
- `GET /api/v1/proposals/{proposal_id}`
- `GET /api/v1/clients/{client_id}/activities`

## Testing

- Backend `/health` berhasil.
- API Create Proposal berhasil.
- Proposal Number otomatis berhasil dibuat.
- Proposal Owner otomatis dari user login.
- Status awal otomatis `Draft`.
- Activity `Proposal dibuat` tercatat pada Client Activity Timeline.
- Frontend lint berhasil.
- Frontend build berhasil.
- Browser testing berhasil.
- Screenshot Product Owner Review berhasil dibuat:
  - Proposal Create.
  - Validation.
  - Success Create.
  - Loading State.
  - Error State.

## Regression Testing

- Login berhasil.
- Dashboard berhasil dibuka.
- Client Management tetap berfungsi.
- Proposal List tetap berfungsi.
- Proposal Detail tetap berfungsi.
- Proposal Create berhasil.
- Proposal Status Actions tetap berfungsi.
- Activity Logging tetap berfungsi.

## Product Owner Notes

Product Owner Review Sprint 5 selesai dan Sprint Implementasi 5 disetujui.

Keputusan Product Owner:

- Design Proposal Create dinyatakan Design Freeze.
- Research Type menggunakan dropdown statis untuk MVP.
- Label budget menggunakan `Estimasi Nilai Proposal (Rp)`.
- Proposal Create hanya membuat Draft.
- Pengiriman Proposal tetap dilakukan melalui Status Actions di Proposal Detail.
- Setup Project tidak masuk Sprint 5.

Commit yang dibuat:

`6af1609 feat(proposal): implement proposal create`

Push ke branch `main` berhasil.

## Backlog

Backlog yang tetap relevan:

- BACKLOG-001 Integrasi Proposal dengan Client Contact.
- UI-001 Timeline Proposal.
- UI-002 Activity Timeline.
- UI-003 Quick Actions Proposal.
- AUTH-001 Perbaikan pesan login ketika backend tidak dapat dihubungi.

Catatan tambahan:

- Halaman login masih memiliki beberapa label Bahasa Inggris seperti `Sign in`. Ini tidak diubah karena berada di luar scope Sprint 5.

## Definition of Done

- Implementasi sesuai WF-002.
- Implementasi sesuai SPR-005 Implementation Plan.
- Tidak menambah fitur di luar Sprint 5.
- Tidak mengubah workflow Proposal.
- Tidak mengubah domain model.
- Tidak membuat Project, Quotation, atau Contract.
- Frontend lint berhasil.
- Frontend build berhasil.
- Browser testing berhasil.
- Regression testing berhasil.
- Product Owner Review selesai dan disetujui.
- Commit dan push ke `main` selesai.
