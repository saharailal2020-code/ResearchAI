# WF-002 Proposal Create

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- WF-001 Proposal Workflow MVP v0.1
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1
- Product Owner Decision Sprint A0

## 1. Tujuan Halaman

Proposal Create Page digunakan oleh Business Development untuk membuat Proposal baru secara cepat.

Tujuan utama:

- Membuat Draft Proposal dalam waktu kurang dari 3 menit.
- Menghubungkan Proposal ke Client yang benar.
- Mengisi data minimum yang diperlukan untuk proses Proposal.
- Menyiapkan data awal yang nantinya dapat menjadi dasar `Setup Project` jika Proposal disetujui.

Proposal Create bukan tempat untuk mengisi semua detail riset. Detail seperti objective, methodology, dan timeline dapat dilengkapi setelah Draft dibuat melalui Proposal Edit pada sprint berikutnya.

## 2. Prinsip Desain

1. Form harus singkat.
2. Field awal hanya yang benar-benar dibutuhkan untuk Draft.
3. Proposal Number dibuat otomatis oleh backend.
4. Proposal Owner otomatis dari user yang sedang login.
5. Status awal otomatis `Draft`.
6. Status tidak dipilih dari form.
7. Form tidak membuat Project.
8. Form tidak membuat Quotation.
9. Form tidak membuat Contract.
10. Proposal yang dibuat harus langsung dapat dibuka di Proposal Detail.

## 3. Informasi yang Harus Diisi

Field MVP:

| Field | Wajib | Tujuan |
| --- | --- | --- |
| Client | Ya | Menentukan pemilik Proposal |
| Proposal Title | Ya | Nama Proposal dan kandidat nama awal Project |
| Research Type | Tidak | Kategori riset dari dropdown master data MVP dan kandidat research type Project |
| Estimasi Nilai Proposal (Rp) | Tidak | Estimasi nilai Proposal kepada client dan kandidat project value sementara |

Field yang otomatis:

| Field | Sumber |
| --- | --- |
| Proposal Number | Backend |
| Proposal Owner | Current user |
| Status | Backend, default `Draft` |
| Created Date | Backend |
| Updated Date | Backend |

Field yang ditunda ke Proposal Edit:

- Research Objective
- Methodology Summary
- Estimated Timeline
- Internal Note
- Attachment

## 4. Pengelompokan Field

### Section 1: Informasi Utama

Field:

- Client
- Proposal Title

Tujuan:
Membuat Proposal memiliki identitas bisnis yang jelas.

### Section 2: Ringkasan Riset

Field:

- Research Type
- Estimasi Nilai Proposal (Rp)

Tujuan:
Memberikan konteks awal untuk Proposal List, Proposal Detail, dan future Setup Project.

### Section 3: Informasi Sistem

Read-only information:

- Proposal Number: otomatis setelah disimpan
- Proposal Owner: user saat ini
- Status: Draft

Tujuan:
Memberi pemahaman bahwa user tidak perlu mengisi nomor, owner, atau status.

## 5. Validasi Field

### Client

Rules:

- Wajib dipilih.
- Harus berasal dari daftar Client yang tersedia.
- Tidak boleh input teks bebas.

Error message:

```text
Client wajib dipilih.
```

### Proposal Title

Rules:

- Wajib diisi.
- Minimal 3 karakter.
- Maksimal 150 karakter.
- Tidak boleh hanya spasi.

Error message:

```text
Judul proposal wajib diisi.
```

### Research Type

Rules:

- Optional.
- Tidak menggunakan free text.
- Menggunakan dropdown yang bersumber dari master data.
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

Error message:

```text
Jenis riset belum valid.
```

### Estimasi Nilai Proposal (Rp)

Rules:

- Optional.
- Jika diisi, harus berupa angka.
- Tidak boleh negatif.
- Nilai 0 sebaiknya dianggap belum diisi.
- Ditampilkan dalam format Rupiah di list/detail setelah tersimpan.

Error message:

```text
Estimasi nilai proposal harus berupa angka dan tidak boleh negatif.
```

## 6. Alur Penyimpanan Draft

```text
User klik + Proposal Baru
  |
  v
Proposal Create Page terbuka
  |
  v
User memilih Client dan mengisi Proposal Title
  |
  v
User boleh mengisi Research Type dan Estimasi Nilai Proposal
  |
  v
User klik Simpan Draft
  |
  v
Frontend validasi field
  |
  v
Frontend mengirim request Create Proposal
  |
  v
Backend membuat Proposal Number, Owner, dan Status Draft
  |
  v
Backend mencatat Activity "Proposal dibuat"
  |
  v
User diarahkan ke Proposal Detail
```

Expected backend behavior:

- `proposal_number` otomatis.
- `proposal_owner_id` otomatis.
- `status = Draft`.
- Activity proposal created tercatat ke Client Activity Timeline.

## 7. Alur Submit Proposal

Pada Sprint 5, Submit Proposal ke Client tidak dilakukan dari Proposal Create Page.

Reasoning:

- Proposal harus dibuat sebagai Draft dulu.
- Status business action sudah tersedia di Proposal Detail.
- Mengirim Proposal ke Client adalah event bisnis terpisah dari create draft.

Flow submit yang benar:

```text
Create Proposal -> Draft
  |
  v
Proposal Detail
  |
  v
Next Business Action: Kirim ke Client
```

Dengan demikian, Proposal Create hanya memiliki primary action:

```text
Simpan Draft
```

Secondary action:

```text
Batal
```

## 8. Loading State

### Loading Client List

Tampil saat daftar Client sedang dimuat.

Copy:

```text
Memuat daftar client...
```

### Saving Draft

Tampil saat Proposal sedang dibuat.

Button state:

```text
Menyimpan...
```

Rules:

- Tombol submit disabled.
- Tombol batal sebaiknya disabled atau tetap aktif sesuai implementasi.
- Jangan mengirim request ganda.

## 9. Error State

### Client List Error

Jika daftar Client gagal dimuat:

```text
Daftar client belum bisa dimuat. Pastikan backend sedang berjalan.
```

Action:

- Coba Lagi
- Kembali ke Proposal

### Create Proposal Error

Jika request create gagal:

```text
Proposal belum bisa disimpan. Silakan coba lagi.
```

### Validation Error

Ditampilkan dekat field terkait dan/atau summary error di atas form.

## 10. Empty State

### Tidak Ada Client

Jika belum ada client:

```text
Belum ada client.
Buat client terlebih dahulu sebelum membuat proposal.
```

Action:

- Kembali ke Client

Reasoning:

Proposal tidak boleh dibuat tanpa Client.

## 11. Navigasi Setelah Berhasil

Setelah Draft Proposal berhasil dibuat:

```text
Navigate to /proposals/{proposal_id}
```

Di Proposal Detail:

- Proposal Number tampil dominan.
- Status tampil `Draft`.
- Next Business Action tampil `Kirim ke Client`.

## 12. Wireframe Sederhana

```text
Proposal / Proposal Baru

┌──────────────────────────────────────────────────────────────┐
│ Proposal Baru                                                │
│ Buat draft proposal baru untuk client.                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐ ┌─────────────────────┐
│ Informasi Utama                       │ │ Informasi Sistem    │
│                                      │ │                     │
│ Client *                             │ │ Proposal Number     │
│ [ Pilih Client              v ]      │ │ Dibuat otomatis     │
│                                      │ │                     │
│ Proposal Title *                     │ │ Proposal Owner      │
│ [ Masukkan judul proposal       ]    │ │ User saat ini       │
│                                      │ │                     │
│ Ringkasan Riset                      │ │ Status              │
│                                      │ │ Draft               │
│ Research Type                        │ │                     │
│ [ Customer Satisfaction        v ]   │ └─────────────────────┘
│                                      │
│ Estimasi Nilai Proposal (Rp)         │
│ [ Rp 0                         ]     │
│                                      │
│ [ Batal ]            [ Simpan Draft ] │
└──────────────────────────────────────┘
```

## 13. Hubungan dengan Setup Project

Proposal Create harus mulai menangkap data yang akan menjadi dasar Setup Project:

- Client -> menjadi Client Project
- Proposal Title -> kandidat Project Name
- Research Type -> kandidat Research Type Project
- Estimasi Nilai Proposal (Rp) -> kandidat Project Value sementara

Namun Proposal Create tidak membuat Project.

Project hanya dapat dibuat nanti setelah Proposal:

```text
Draft -> Dikirim ke Client -> Disetujui -> Setup Project
```

## 14. Acceptance Criteria

1. User dapat membuka Proposal Create dari tombol `+ Proposal Baru`.
2. Form menampilkan field Client, Proposal Title, Research Type, dan Estimasi Nilai Proposal (Rp).
3. Client wajib dipilih.
4. Proposal Title wajib diisi.
5. Estimasi Nilai Proposal (Rp) harus angka dan tidak boleh negatif jika diisi.
6. Proposal Number tidak diisi manual.
7. Proposal Owner tidak dipilih manual.
8. Status tidak dipilih manual.
9. Submit membuat Proposal berstatus Draft.
10. Submit berhasil mengarahkan user ke Proposal Detail.
11. Proposal Detail menampilkan Proposal Number hasil backend.
12. Activity `Proposal dibuat` tercatat ke Client Activity Timeline dari backend.
13. Empty state muncul jika belum ada Client.
14. Loading state muncul saat daftar Client dimuat dan saat draft disimpan.
15. Error state muncul jika daftar Client gagal dimuat atau create gagal.
16. Tidak membuat Project.
17. Tidak membuat Quotation.
18. Tidak membuat Contract.
19. Tidak mengubah workflow Proposal yang sudah disetujui.
20. Frontend lint, build, browser testing, dan regression testing berhasil pada sprint implementasi.

## 15. Risiko

- Form terlalu panjang sehingga tujuan create kurang dari 3 menit gagal.
- User mengira Simpan Draft sama dengan mengirim ke client.
- Client list gagal dimuat sehingga Proposal tidak bisa dibuat.
- Input estimasi nilai proposal dapat membingungkan jika tidak diformat Rupiah dengan baik.
- Jika setelah submit tidak diarahkan ke Proposal Detail, user tidak melihat Next Business Action.

## 16. Rekomendasi Desain

1. Gunakan label `Simpan Draft`, bukan `Submit`.
2. Tampilkan status sistem sebagai read-only agar user paham nomor, owner, dan status dibuat otomatis.
3. Setelah berhasil, arahkan langsung ke Proposal Detail.
4. Jangan tampilkan tombol `Kirim ke Client` di halaman create.
5. Pastikan empty state client jelas karena Proposal wajib memiliki Client.
