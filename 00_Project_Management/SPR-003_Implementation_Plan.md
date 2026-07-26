# SPR-003 Implementation Plan

Nama Sprint:
Proposal Management - Proposal Detail

Baseline:
WF-001 Proposal Workflow MVP v0.1

Status:
Draft untuk Product Owner Review

## 1. Tujuan Sprint

Membangun halaman Proposal Detail sebagai pusat informasi untuk satu proposal.

Proposal Detail harus memungkinkan user Business Development membaca informasi proposal secara lengkap, memahami status proposal, melihat relasi ke client, dan menjadi dasar untuk status action pada sprint berikutnya.

Sprint ini tetap mengikuti prinsip MVP:

- Tidak membuat Project.
- Tidak membuat Quotation.
- Tidak membuat Contract.
- Tidak membuat Document Management.
- Tidak mengubah workflow yang sudah disetujui.
- Tidak mengubah Client Management yang sudah berjalan.

## 2. Scope

Masuk scope Sprint 3:

- Mengganti Proposal Detail Placeholder menjadi halaman detail yang fungsional.
- Mengambil data proposal berdasarkan ID dari backend.
- Menampilkan informasi utama proposal.
- Menampilkan status proposal dengan badge.
- Menampilkan informasi client terkait proposal.
- Menampilkan proposal owner.
- Menampilkan estimated budget, research type, objective, methodology summary, estimated timeline, created date, updated date, dan approved date jika tersedia.
- Menambahkan link kembali ke Proposal List.
- Menambahkan link ke Client Detail.
- Menampilkan informational note untuk proposal Approved: "Siap untuk Project Setup".
- Menyiapkan area status action secara UI jika endpoint sudah tersedia dan sesuai WF-001.

Tidak masuk scope Sprint 3:

- Create Proposal Form.
- Edit Proposal Form.
- Status update jika endpoint belum final atau belum direview.
- Project creation.
- Quotation.
- Contract.
- File upload.
- AI proposal draft.
- Kanban pipeline.
- Advanced approval workflow.

## 3. Komponen Frontend

Komponen atau halaman yang akan disentuh:

- `frontend/src/pages/ProposalDetailPage.jsx`
- `frontend/src/App.jsx` jika routing perlu disesuaikan minor.
- Komponen reusable yang sudah ada dapat digunakan jika sesuai style aplikasi.

Layout Proposal Detail yang disarankan:

- Header:
  - Proposal Number
  - Proposal Title
  - Status Badge
  - Back to Proposal List

- Summary Panel:
  - Client
  - Proposal Owner
  - Research Type
  - Estimated Budget
  - Created Date
  - Updated Date

- Detail Sections:
  - Research Objective
  - Methodology Summary
  - Estimated Timeline
  - Approved Date jika status Approved

- Relationship Section:
  - Link ke Client Detail
  - Informasi bahwa Approved Proposal siap masuk Project Setup pada phase berikutnya

- Empty/Error State:
  - Proposal tidak ditemukan
  - Gagal mengambil data dari server
  - Loading state

## 4. Komponen Backend

Komponen backend ideal yang digunakan:

- Endpoint detail proposal berdasarkan ID.
- Response proposal harus menyertakan:
  - proposal_number
  - proposal_title
  - client
  - proposal_owner
  - research_type
  - research_objective
  - methodology_summary
  - estimated_timeline
  - estimated_budget
  - status
  - approved_at
  - created_at
  - updated_at

Catatan:

Jika endpoint detail proposal belum tersedia atau response belum cukup, perubahan backend harus direview terlebih dahulu sebelum implementasi frontend dilanjutkan. Namun Sprint 3 sebaiknya memakai endpoint yang sudah ada jika memungkinkan.

## 5. API yang digunakan

API utama:

- `GET /api/v1/proposals/{proposal_id}`

API pendukung jika dibutuhkan:

- `GET /api/v1/clients/{client_id}`

Preferensi:

Proposal detail sebaiknya sudah mengembalikan data client dan proposal owner agar frontend tidak perlu terlalu banyak request.

## 6. Acceptance Criteria

Sprint 3 dianggap selesai jika:

1. User dapat membuka Proposal Detail dari Proposal List.
2. Proposal Detail menampilkan Proposal Number dengan jelas.
3. Proposal Detail menampilkan Proposal Title.
4. Proposal Detail menampilkan Client terkait.
5. Proposal Detail menampilkan Proposal Owner.
6. Proposal Detail menampilkan Research Type.
7. Proposal Detail menampilkan Estimated Budget dalam format Rupiah.
8. Proposal Detail menampilkan Status Badge yang konsisten dengan Proposal List.
9. Proposal Detail menampilkan Created Date dan Updated Date.
10. Jika proposal Approved, halaman menampilkan informasi "Siap untuk Project Setup".
11. User dapat kembali ke Proposal List.
12. User dapat membuka Client Detail dari Proposal Detail.
13. Loading state tampil saat data sedang diambil.
14. Error state tampil jika proposal tidak ditemukan atau server gagal dihubungi.
15. Frontend lint berhasil.
16. Frontend build berhasil.
17. Browser testing berhasil.
18. Client Management tetap berfungsi.
19. Proposal List tetap berfungsi.
20. Tidak ada Project, Quotation, Contract, atau Document Management yang dibuat.

## 7. Risiko

- Endpoint detail proposal mungkin belum mengembalikan semua field yang dibutuhkan frontend.
- Data client atau proposal owner mungkin belum lengkap pada response detail.
- Status backend mungkin memakai nilai teknis seperti `Sent` dan `Revised`, sedangkan UI harus menampilkan label yang mudah dipahami.
- Jika status action ikut dimasukkan terlalu cepat, scope Sprint 3 bisa melebar.
- Jika detail page terlalu padat, Business Development bisa kesulitan membaca informasi utama.

Mitigasi:

- Mulai dari read-only Proposal Detail terlebih dahulu.
- Gunakan label Bahasa Indonesia yang konsisten.
- Status action ditunda jika endpoint atau workflow implementasinya belum direview.
- Pertahankan visual style yang sama dengan Client Management dan Proposal List.

## 8. Estimasi pekerjaan

Estimasi:
1 sampai 2 hari kerja.

Rincian estimasi:

- Review endpoint detail proposal: 0.5 hari.
- Implementasi halaman Proposal Detail read-only: 0.5 hari.
- Loading, empty, dan error state: 0.25 hari.
- Browser testing dan regression testing: 0.25 hari.
- Perbaikan minor setelah Product Owner Review: 0.5 hari jika diperlukan.

Rekomendasi urutan Sprint 3:

1. Design Review Proposal Detail.
2. Review API detail proposal.
3. Implementasi Proposal Detail read-only.
4. Testing.
5. Product Owner Review.
6. Commit setelah disetujui.
