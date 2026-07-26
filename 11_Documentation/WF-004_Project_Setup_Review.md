# WF-004 Project Setup Review

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- WF-003 Setup Project
- ADR-001 Proposal to Project
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1
- Product Owner Decision Sprint 6

## 1. Tujuan Halaman

Project Setup Review Page adalah halaman konfirmasi sebelum Proposal `Approved` diubah menjadi Project operasional.

Halaman ini tidak langsung membuat Project saat dibuka. Halaman ini berfungsi sebagai checkpoint agar user dapat melihat data apa saja yang akan dibawa dari Proposal ke Project sebelum klik `Buat Project`.

Tujuan utama:

- Memastikan Project hanya dibuat dari Proposal yang sudah `Approved`.
- Memberi kesempatan user meninjau data Proposal dan Client.
- Mengizinkan user mengubah `Project Name` sebelum Project dibuat.
- Menampilkan checklist data yang akan dibawa ke Project.
- Mencegah Project dibuat dua kali dari Proposal yang sama.
- Menjaga Proposal tetap menjadi historical record.

## 2. Workflow

```text
Proposal Detail
  |
  | Proposal status = Approved
  | Project belum dibuat
  v
Action: Setup Project
  |
  v
Project Setup Review Page
  |
  | User review data
  | User dapat mengubah Project Name
  v
Klik Buat Project
  |
  v
Backend validasi Proposal Approved dan belum punya Project
  |
  v
Project dibuat dengan status Setup
  |
  v
User diarahkan ke Project Detail / Project Setup Page
```

Jika Project sudah pernah dibuat:

```text
Proposal Detail / Setup Review
  |
  v
Sistem menampilkan Project existing
  |
  v
User diarahkan ke Project existing
```

## 3. Layout Halaman

Layout desktop menggunakan pola profesional yang konsisten dengan Proposal Detail dan Client Management.

```text
Breadcrumb
Proposal / Proposal Detail / Setup Project

Header
Setup Project
Review data proposal sebelum membuat project.

Main Layout
┌──────────────────────────────────────────────┬──────────────────────────────┐
│ Left Column                                  │ Right Column                 │
│                                              │                              │
│ Ringkasan Proposal                           │ Informasi Sistem             │
│ Ringkasan Client                             │ Checklist Data               │
│ Project Information                          │                              │
│                                              │ Action Panel                 │
│                                              │ [Batal] [Buat Project]       │
└──────────────────────────────────────────────┴──────────────────────────────┘
```

Prinsip layout:

- Data sumber ditampilkan jelas di sisi kiri.
- Data sistem dan checklist ditampilkan di sisi kanan.
- Tombol utama `Buat Project` berada di area action yang mudah ditemukan.
- Halaman tidak menggunakan popup.

## 4. Breadcrumb

```text
Proposal / Proposal Detail / Setup Project
```

Behavior:

- `Proposal` kembali ke Proposal List.
- `Proposal Detail` kembali ke Proposal Detail.
- `Setup Project` adalah halaman aktif.

## 5. Header

Judul:

```text
Setup Project
```

Subjudul:

```text
Review data proposal sebelum membuat project operasional.
```

Badge:

- Proposal Status: `Disetujui`
- Project Status awal: `Setup`

## 6. Ringkasan Proposal

Section ini menampilkan sumber data bisnis yang menjadi dasar Project.

Field:

- Proposal Number.
- Proposal Title.
- Research Type.
- Estimasi Nilai Proposal (Rp).
- Proposal Owner.
- Approved Date jika tersedia.

Catatan:

- Proposal Number tidak menjadi Project Number.
- Proposal Title menjadi default Project Name tetapi masih dapat diubah.
- Estimasi Nilai Proposal menjadi project value awal, bukan invoice final.

## 7. Ringkasan Client

Section ini memastikan Project dibuat untuk Client yang benar.

Field:

- Nama Client.
- Industry.
- Kota.
- Status Client.
- PIC utama jika tersedia.
- Email PIC jika tersedia.
- Nomor HP PIC jika tersedia.

Jika data PIC belum tersedia:

```text
-
```

Business rule:

- Client Project harus sama dengan Client Proposal.
- User tidak boleh mengganti Client di halaman Setup Project.

## 8. Project Information

Section ini berisi data yang dapat dikonfirmasi sebelum Project dibuat.

Field:

### Project Name

Default:

```text
Proposal Title
```

Rules:

- Wajib.
- Dapat diubah oleh user.
- Minimal 3 karakter.
- Maksimal 150 karakter.
- Tidak boleh hanya spasi.

### Project Manager

Status MVP:

- Optional.
- Boleh kosong.
- Jika belum ada field atau endpoint user list, tampilkan sebagai `Belum ditentukan` read-only.

Rekomendasi MVP:

- Jangan memaksa user memilih Project Manager pada Sprint 6.
- Field dapat disiapkan sebagai informasi optional, tetapi pemilihan Project Manager dapat ditunda.

### Project Notes

Status:

- Optional.
- Dapat ditunda jika backend belum mendukung.

Rekomendasi MVP:

- Tidak wajib di Sprint 6 Implementation jika backend belum memiliki field notes.

## 9. Informasi Sistem

Section read-only.

Field:

- Project Number: dibuat otomatis.
- Project Status: `Setup`.
- Proposal Reference: Proposal Number.
- Created By: user login.
- Created Date: setelah Project dibuat.

Tujuan:

- Menjelaskan kepada user bahwa nomor Project, status awal, dan timestamp tidak perlu diisi manual.

## 10. Checklist Data

Checklist menampilkan data yang akan dibawa dari Proposal ke Project.

Checklist:

- Client akan dibawa ke Project.
- Proposal Reference akan disimpan.
- Project Name berasal dari Proposal Title, dapat diubah sebelum simpan.
- Research Type akan dibawa ke Project.
- Estimasi Nilai Proposal akan menjadi Project Value awal.
- Proposal Owner akan disimpan sebagai referensi Business Development.
- Project Status awal adalah `Setup`.
- Contract tidak menjadi syarat Setup Project pada MVP.
- Project Manager optional pada MVP.

Checklist yang tidak dibawa otomatis:

- Proposal Number tidak menjadi Project Number.
- Proposal Activity tidak menjadi Project Activity.
- Attachment tidak dibawa otomatis tanpa Document Management.
- Quotation tidak dibuat otomatis.
- Invoice tidak dibuat otomatis.
- Payment tidak dibuat otomatis.

## 11. Action Buttons

### Batal

Label:

```text
Batal
```

Behavior:

- Kembali ke Proposal Detail.
- Tidak membuat Project.
- Tidak mengubah Proposal.

### Buat Project

Label:

```text
Buat Project
```

Behavior:

- Menjalankan request Setup Project.
- Tombol disabled saat loading.
- Setelah sukses, user diarahkan ke Project Detail atau Project Setup Page.

Loading label:

```text
Membuat Project...
```

## 12. Loading State

### Loading halaman

Saat mengambil Proposal dan Client:

```text
Memuat data setup project...
```

UI:

- Skeleton atau panel loading.
- Action button belum aktif.

### Loading submit

Saat membuat Project:

```text
Membuat Project...
```

Rules:

- Disable tombol `Buat Project`.
- Disable tombol `Batal` jika request sudah berjalan, atau tetap boleh jika request belum terkirim.

## 13. Error State

### Proposal belum disetujui

```text
Project hanya dapat dibuat dari Proposal yang sudah disetujui.
```

Action:

- Tampilkan tombol kembali ke Proposal Detail.

### Project sudah tersedia

```text
Project untuk proposal ini sudah tersedia.
```

Action:

- Tampilkan tombol `Buka Project`.

### Proposal tidak ditemukan

```text
Proposal tidak ditemukan.
```

Action:

- Tampilkan tombol kembali ke Proposal List.

### Client tidak valid

```text
Client pada proposal tidak valid.
```

Action:

- Tampilkan tombol kembali ke Proposal Detail.

### Gagal membuat Project

```text
Project belum bisa dibuat. Silakan coba lagi.
```

Action:

- User dapat mencoba lagi.

### Network Error

```text
Tidak dapat terhubung ke server.
```

Action:

- User dapat mencoba lagi setelah backend aktif.

## 14. Success Flow

Setelah Project berhasil dibuat:

```text
Backend mengembalikan Project
  |
  v
Frontend menampilkan feedback sukses singkat
  |
  v
User diarahkan ke Project Detail / Project Setup Page
```

Feedback:

```text
Project berhasil dibuat.
```

Jika Project module detail belum lengkap pada awal implementasi, user dapat diarahkan ke Project placeholder yang jelas.

## 15. Business Rules

1. Setup Project hanya dimulai dari Proposal `Approved`.
2. Setup Project membuka halaman review terlebih dahulu.
3. Project dibuat hanya setelah user klik `Buat Project`.
4. Default Project Name berasal dari Proposal Title.
5. Project Name dapat diubah sebelum Project dibuat.
6. Project Number dibuat otomatis oleh backend.
7. Contract tidak menjadi syarat Setup Project pada MVP.
8. Project Manager optional pada MVP.
9. Client tidak dapat diganti saat Setup Project.
10. Research Type dibawa dari Proposal dan tidak diubah pada halaman review.
11. Project status awal adalah `Setup`.
12. Satu Proposal maksimal menghasilkan satu Project pada MVP.
13. Proposal tetap menjadi historical record.
14. Activity `Project dibuat dari Proposal` wajib dicatat dari backend service.

## 16. Validation Rules

### Project Name

Rules:

- Wajib.
- Minimal 3 karakter.
- Maksimal 150 karakter.
- Tidak boleh hanya spasi.

Error:

```text
Nama project wajib diisi.
```

### Proposal Status

Rules:

- Harus `Approved`.

Error:

```text
Project hanya dapat dibuat dari Proposal yang sudah disetujui.
```

### Existing Project

Rules:

- Jika Project sudah ada untuk Proposal tersebut, jangan buat Project baru.

Error:

```text
Project untuk proposal ini sudah tersedia.
```

## 17. Wireframe

```text
Proposal / Proposal Detail / Setup Project

Setup Project                                      [Disetujui] [Status Project: Setup]
Review data proposal sebelum membuat project operasional.

┌──────────────────────────────────────────────────────────────────────────────┐
│ Ringkasan Proposal                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ Proposal Number        PROP-20260726-0001                                    │
│ Proposal Title         Customer Satisfaction Survey 2026                     │
│ Research Type          Customer Satisfaction                                 │
│ Estimasi Nilai         Rp 25.000.000                                         │
│ Proposal Owner         ResearchAI Admin                                      │
│ Approved Date          26 Jul 2026                                           │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────┬──────────────────────────────┐
│ Ringkasan Client                             │ Informasi Sistem             │
├──────────────────────────────────────────────┼──────────────────────────────┤
│ Client              PT Contoh Riset          │ Project Number   Otomatis    │
│ Industry            Market Research          │ Status Awal      Setup       │
│ Kota                Jakarta                  │ Proposal Ref     PROP-...    │
│ PIC                 Budi                     │ Created By       Admin       │
│ Email               budi@example.com         │ Created Date     Setelah buat│
│ Nomor HP            0812xxxx                 │                              │
└──────────────────────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────────────────────┬──────────────────────────────┐
│ Project Information                          │ Checklist Data               │
├──────────────────────────────────────────────┼──────────────────────────────┤
│ Project Name *                               │ ✓ Client dibawa              │
│ [Customer Satisfaction Survey 2026       ]   │ ✓ Proposal ref disimpan      │
│                                              │ ✓ Research type dibawa       │
│ Project Manager                             │ ✓ Nilai proposal dibawa      │
│ Belum ditentukan                             │ ✓ Status awal Setup          │
│                                              │ ✓ Contract tidak wajib       │
│                                              │ ✓ PM optional                │
└──────────────────────────────────────────────┴──────────────────────────────┘

                                                        [Batal] [Buat Project]
```

## 18. Acceptance Criteria

1. Halaman Setup Project Review dapat dibuka dari Proposal Detail yang berstatus `Approved`.
2. Halaman tidak dapat digunakan untuk Proposal yang belum `Approved`.
3. Halaman menampilkan ringkasan Proposal.
4. Halaman menampilkan ringkasan Client.
5. Halaman menampilkan Project Name dengan default dari Proposal Title.
6. User dapat mengubah Project Name sebelum membuat Project.
7. Halaman menampilkan Informasi Sistem read-only.
8. Halaman menampilkan checklist data yang akan dibawa ke Project.
9. Tombol `Batal` mengembalikan user ke Proposal Detail.
10. Tombol `Buat Project` membuat Project setelah konfirmasi user.
11. Loading state tampil saat data dimuat.
12. Loading submit tampil saat Project dibuat.
13. Error state tampil jika Proposal belum Approved.
14. Error state tampil jika Project sudah tersedia.
15. Error state tampil jika backend gagal.
16. Project yang dibuat memiliki status awal `Setup`.
17. Project Number dibuat backend.
18. Contract tidak diwajibkan.
19. Project Manager optional.
20. Tidak ada Quotation, Contract, Invoice, atau Payment yang dibuat otomatis.

## 19. Risiko Implementasi

### Risiko 1: Endpoint Project belum tersedia

Mitigasi:

- Sprint implementasi harus dimulai dari backend foundation jika endpoint belum tersedia.

### Risiko 2: Idempotency belum kuat

Mitigasi:

- Backend wajib melakukan pengecekan Project existing berdasarkan `proposal_id`.
- Tambahkan constraint unik pada `proposal_id` saat schema Project dibuat.

### Risiko 3: Project Detail belum tersedia

Mitigasi:

- Jika Project Detail belum siap, arahkan ke Project placeholder yang jelas.

### Risiko 4: Data Proposal belum lengkap

Mitigasi:

- Setup Project tetap bisa berjalan dengan data minimum.
- Field operasional dilengkapi pada Project Setup sprint berikutnya.

### Risiko 5: Hak akses belum granular

Mitigasi:

- Gunakan rule MVP: Administrator dan Proposal Owner.
- Buat backlog permission granular.
