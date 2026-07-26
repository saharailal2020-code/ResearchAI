# SPR-004 Implementation Plan

Nama Sprint:
Proposal Management - Proposal Status Actions

Baseline:
WF-001 Proposal Workflow MVP v0.1

Status:
Draft untuk Product Owner Review

## Tujuan Sprint

Membangun Status Actions pada Proposal Detail agar user dapat mengubah status proposal sesuai lifecycle MVP yang sudah disetujui.

Status Actions harus memperlakukan perubahan status sebagai event bisnis, bukan sebagai field biasa di form.

## Scope

Masuk scope:

- Menampilkan action yang valid berdasarkan status proposal saat ini.
- Mengubah status proposal melalui endpoint backend yang sudah tersedia.
- Memperbarui tampilan Proposal Detail setelah status berubah.
- Menampilkan loading state saat status sedang diproses.
- Menampilkan error state jika perubahan status gagal.
- Memastikan activity proposal otomatis tercatat dari backend service.
- Memastikan status badge dan Approved note diperbarui setelah status berubah.

Tidak masuk scope:

- Edit Proposal.
- Proposal Form.
- Project creation.
- Quotation.
- Contract.
- File upload.
- Approval internal.
- Kanban pipeline.

## Workflow

Lifecycle MVP:

```text
Draft -> Sent to Client -> Revision -> Approved / Rejected
```

Transisi status yang valid:

- Draft -> Sent to Client
- Sent to Client -> Revision
- Sent to Client -> Approved
- Sent to Client -> Rejected
- Revision -> Sent to Client
- Revision -> Approved
- Revision -> Rejected

Status final:

- Approved
- Rejected

Untuk MVP, status final tidak perlu memiliki action lanjutan.

## Backend

Backend yang digunakan:

- Endpoint status proposal yang sudah tersedia.
- Activity logging tetap dilakukan di backend service.

Hal yang perlu diverifikasi sebelum implementasi:

- Endpoint status menerima status `Sent`, `Revised`, `Approved`, dan `Rejected`.
- Backend mengisi `approved_at` saat status menjadi `Approved`.
- Backend menghapus atau mengosongkan `approved_at` jika status berubah dari Approved ke status lain, jika transisi tersebut nantinya diizinkan.
- Backend mencatat activity:
  - Proposal dikirim ke client.
  - Proposal perlu revisi.
  - Proposal disetujui.
  - Proposal ditolak.

Catatan:

Jika backend sudah memenuhi kebutuhan Sprint 4, tidak perlu perubahan backend.

## Frontend

Komponen yang akan disentuh:

- `frontend/src/pages/ProposalDetailPage.jsx`
- `frontend/src/services/proposals.js`

Komponen UI:

- Section `Status & Next Step`.
- Tombol status action.
- Loading state per action.
- Error message jika action gagal.

Label action yang disarankan:

- `Kirim ke Client`
- `Tandai Perlu Revisi`
- `Setujui Proposal`
- `Tolak Proposal`

Prinsip UI:

- Tampilkan hanya action yang valid.
- Hindari dropdown status bebas.
- Gunakan tombol aksi agar event bisnis jelas.
- Untuk action penting seperti Approved dan Rejected, pertimbangkan konfirmasi sederhana jika Product Owner menyetujui.

## API

API utama:

- `PATCH /api/v1/proposals/{proposal_id}/status`

Payload:

```json
{
  "status": "Sent"
}
```

Status payload yang digunakan:

- `Sent`
- `Revised`
- `Approved`
- `Rejected`

API pendukung:

- `GET /api/v1/proposals/{proposal_id}`
- `GET /api/v1/clients/{client_id}`

## Acceptance Criteria

Sprint 4 dianggap selesai jika:

1. Proposal Detail menampilkan Status Actions sesuai status saat ini.
2. Draft hanya dapat dikirim ke client.
3. Sent dapat diubah menjadi Revision, Approved, atau Rejected.
4. Revision dapat dikirim ulang ke client, Approved, atau Rejected.
5. Approved menampilkan informasi siap untuk Project Setup.
6. Rejected tidak menampilkan action lanjutan pada MVP.
7. Perubahan status menggunakan endpoint backend.
8. Setelah status berubah, UI langsung menampilkan status terbaru.
9. Activity proposal tercatat di Client Activity Timeline melalui backend service.
10. Loading state tampil saat action diproses.
11. Error state tampil jika action gagal.
12. Tidak ada Edit Proposal.
13. Tidak ada Proposal Form.
14. Tidak ada Project, Quotation, atau Contract.
15. Frontend lint berhasil.
16. Frontend build berhasil.
17. Browser testing berhasil.
18. Regression testing berhasil.

## Risiko

- User bisa salah klik status penting seperti Approved atau Rejected.
- Jika action terlalu banyak tampil sekaligus, user bisa bingung.
- Jika activity gagal tercatat, timeline Client 360 menjadi tidak lengkap.
- Jika status label UI tidak konsisten dengan nilai backend, user bisa salah paham.
- Jika transisi status tidak divalidasi di frontend, action tidak valid bisa muncul.

Mitigasi:

- Tampilkan hanya action yang valid untuk status saat ini.
- Gunakan label Bahasa Indonesia yang jelas.
- Pastikan backend tetap menjadi sumber utama activity logging.
- Verifikasi Client Activity Timeline setelah status berubah.
- Pertimbangkan konfirmasi untuk Approved dan Rejected pada Design Review.

## Estimasi

Estimasi pekerjaan:
1 sampai 2 hari kerja.

Rincian:

- Review backend endpoint status: 0.25 hari.
- Design Review Status Actions: 0.25 hari.
- Implementasi frontend Status Actions: 0.5 hari.
- Browser testing dan regression testing: 0.25 hari.
- Perbaikan minor setelah Product Owner Review: 0.5 hari jika diperlukan.

## Rekomendasi Sebelum Implementasi

Lakukan Design Review Sprint 4 terlebih dahulu sebelum coding.

Hal yang perlu disetujui:

- Apakah Approved dan Rejected perlu dialog konfirmasi.
- Apakah action ditempatkan di section `Status & Next Step` atau di header.
- Apakah status final benar-benar tidak bisa diubah pada MVP.
- Apakah label `Sent to Client` di UI diterjemahkan menjadi `Dikirim ke Client`.
