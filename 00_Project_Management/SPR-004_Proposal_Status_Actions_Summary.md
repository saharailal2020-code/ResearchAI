# SPR-004 Proposal Status Actions Summary

Nama Sprint:
Proposal Management - Proposal Status Actions

## Tujuan Sprint

Membangun Status Actions pada Proposal Detail agar perubahan status proposal mengikuti workflow MVP dan tercatat sebagai event bisnis.

## Scope

Masuk scope:

- Menampilkan Next Business Action sesuai status proposal.
- Mengubah status proposal melalui backend.
- Memperbarui tampilan Proposal Detail setelah status berubah.
- Menampilkan loading action.
- Menampilkan error action.
- Memastikan activity logging tercatat dari backend service.

Tidak masuk scope:

- Edit Proposal.
- Proposal Form.
- Project.
- Quotation.
- Contract.
- File upload.
- Alasan revisi atau alasan penolakan.

## Fitur yang selesai

- Status `Draft` menampilkan action `Kirim ke Client`.
- Status `Sent` atau `Dikirim` menampilkan action:
  - `Tandai Perlu Revisi`
  - `Setujui Proposal`
  - `Tolak Proposal`
- Status `Revised` atau `Revisi` menampilkan action:
  - `Kirim Ulang ke Client`
  - `Setujui Proposal`
  - `Tolak Proposal`
- Status `Approved` atau `Disetujui` tidak menampilkan action lanjutan dan menampilkan informasi siap Project Setup.
- Status `Rejected` atau `Ditolak` tidak menampilkan action lanjutan.
- Loading action tampil saat status sedang diproses.
- Error action tampil jika update status gagal.
- Activity proposal tercatat di Client Activity Timeline melalui backend.

## File yang berubah

- `frontend/src/pages/ProposalDetailPage.jsx`
- `frontend/src/services/proposals.js`

## Endpoint yang digunakan

- `PATCH /api/v1/proposals/{proposal_id}/status`
- `GET /api/v1/proposals/{proposal_id}`
- `GET /api/v1/clients/{client_id}`
- `GET /api/v1/clients/{client_id}/activities`

## Testing

- Frontend lint berhasil.
- Frontend build berhasil.
- Browser testing berhasil.
- Loading action berhasil diuji.
- Error action berhasil diuji.
- Activity logging berhasil diverifikasi melalui API.

## Regression Testing

- Login berhasil.
- Dashboard berhasil.
- Client Management tetap berfungsi.
- Proposal List tetap berfungsi.
- Proposal Detail tetap berfungsi.
- Status Actions berhasil.
- Activity Logging tampil di Client Activity Timeline.

## Product Owner Notes

Product Owner Review Sprint 4 selesai dan Sprint Implementasi 4 disetujui.

Keputusan Product Owner:

- Workflow mengikuti proses bisnis Beerka.
- Tidak meminta alasan revisi atau alasan penolakan.
- Status Actions tampil sebagai Next Business Action.
- Action hanya muncul sesuai status proposal saat ini.
- Tidak menambahkan fitur di luar scope Sprint 4.

Commit yang dibuat:

`31a0f73 feat(proposal): implement proposal status actions`

Push ke branch `main` berhasil.

## Backlog

Backlog yang sudah ada dan tetap relevan:

- UI-001 Timeline Proposal.
- UI-002 Activity Timeline.
- UI-003 Quick Actions Proposal.
- AUTH-001 Perbaikan pesan login ketika backend tidak dapat dihubungi.

## Definition of Done

- Implementasi sesuai WF-001.
- Implementasi sesuai SPR-004 Implementation Plan.
- Tidak ada dropdown status bebas.
- Tidak ada alasan revisi atau alasan penolakan.
- Tidak ada Project, Quotation, atau Contract.
- Activity logging berasal dari backend service.
- Frontend lint berhasil.
- Frontend build berhasil.
- Browser testing berhasil.
- Regression testing berhasil.
- Product Owner Review selesai dan disetujui.
- Commit dan push ke `main` selesai.
