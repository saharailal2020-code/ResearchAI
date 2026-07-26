# BACKLOG-001 Proposal Client Contact Integration

Status:
Backlog

Tanggal:
26 Juli 2026

## Judul

Integrasi Proposal dengan Client Contact

## Tujuan

Pada sprint mendatang, Proposal dapat memilih PIC Client langsung dari daftar Client Contact milik Client yang dipilih.

## Latar Belakang

Saat ini Proposal Create MVP hanya memilih Client. Dalam proses bisnis nyata, proposal biasanya dikirim atau dibahas dengan contact person tertentu di sisi client.

Karena Client 360 sudah mendukung lebih dari satu Contact Person, Proposal sebaiknya dapat menyimpan PIC Client agar komunikasi proposal lebih jelas.

## Scope Masa Depan

- Setelah user memilih Client, sistem menampilkan daftar Contact Person milik Client tersebut.
- User dapat memilih PIC Client untuk Proposal.
- Primary Contact dapat dijadikan default pilihan.
- Proposal Detail menampilkan PIC Client.
- Activity proposal dapat menampilkan konteks PIC jika diperlukan.

## Tidak Termasuk Sprint 5

Backlog ini tidak diimplementasikan pada Sprint 5.

Sprint 5 tetap fokus pada Proposal Create MVP dengan field:

- Client
- Proposal Title
- Research Type
- Estimasi Nilai Proposal (Rp)

## Acceptance Criteria Masa Depan

1. User dapat memilih PIC Client dari Contact Person milik Client.
2. Jika Client memiliki Primary Contact, contact tersebut otomatis menjadi default.
3. User dapat mengganti PIC Client ke contact lain.
4. Proposal Detail menampilkan PIC Client.
5. Proposal List dapat menampilkan PIC Client jika Product Owner menyetujui.
6. Validasi memastikan PIC yang dipilih benar-benar milik Client tersebut.

## Catatan Arsitektur

Relasi ini sebaiknya menggunakan `client_contact_id` pada Proposal atau mekanisme equivalent yang disetujui pada design review backend.

Jangan membuat free text PIC pada Proposal karena akan memutus hubungan dengan Client 360.
