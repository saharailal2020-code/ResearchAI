# UI-003 Quick Actions Proposal

Status:
Backlog

## Judul

Quick Actions Proposal

## Tujuan

Menyediakan area aksi cepat pada Proposal Detail untuk mempercepat pekerjaan Business Development.

## Deskripsi

Quick Actions dapat berisi aksi yang sering digunakan pada Proposal Detail.

Contoh kandidat aksi:

- Edit Proposal.
- Kirim ke Client.
- Tandai Perlu Revisi.
- Setujui Proposal.
- Tolak Proposal.
- Lihat Client 360.

## Acceptance Criteria

- Quick Actions hanya menampilkan aksi yang valid untuk status proposal saat ini.
- Aksi status mengikuti WF-001.
- Aksi tidak membuat Project, Quotation, atau Contract sebelum sprint terkait disetujui.
- Activity dicatat dari backend service untuk event bisnis yang relevan.

## Catatan

Tidak dikerjakan pada Sprint 3.
