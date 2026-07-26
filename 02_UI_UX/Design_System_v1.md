# ResearchAI Design System v1

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- Client Management
- Client Detail / Client 360
- Proposal List
- Proposal Detail
- Proposal Create
- Proposal Status Actions
- WF-004 Project Setup Review
- WF-005 Project Detail
- Project UI Architecture v1

## 1. Tujuan

Design System v1 mendefinisikan standar UI ResearchAI agar seluruh modul memiliki tampilan, struktur, dan pengalaman pengguna yang konsisten.

ResearchAI adalah ERP/Operating System untuk perusahaan riset. Karena itu UI harus terasa:

- Profesional.
- Tenang.
- Mudah dipindai.
- Konsisten lintas modul.
- Fokus pada workflow bisnis.
- Tidak terasa seperti landing page atau dashboard dekoratif.

## 2. Prinsip Desain

1. Konten bisnis lebih penting daripada dekorasi.
2. Layout harus mudah dipindai oleh user operasional.
3. Action utama harus jelas dan kontekstual.
4. Status harus mudah dikenali dengan badge.
5. Form harus singkat untuk aksi cepat.
6. Empty state harus menjelaskan kondisi, bukan membuat user merasa error.
7. Error state harus memberi arah tindakan berikutnya.
8. Modul baru harus mengikuti pola Client dan Proposal yang sudah berjalan.

## 3. Komponen Reusable

Komponen standar ResearchAI:

- Page Header.
- Summary Card.
- Information Card.
- Status Badge.
- Next Business Action.
- Timeline Component.
- Placeholder Card.
- Loading State.
- Empty State.
- Error State.
- Currency Format.
- Date Format.
- Button Style.
- Form Layout.
- Validation Style.

## 4. Page Header

### Tujuan

Memberi konteks utama halaman.

### Struktur

Page Header minimal memiliki:

- Breadcrumb jika halaman berada di level detail atau create.
- Eyebrow atau label modul.
- Judul halaman.
- Deskripsi singkat jika dibutuhkan.
- Primary action jika halaman list.
- Badge status jika halaman detail.

### Contoh List Page

```text
Manajemen Proposal
Daftar Proposal                                      [+ Proposal Baru]
```

### Contoh Detail Page

```text
Proposal / Proposal Detail

PROP-20260726-0001                                  [Draft]
Customer Satisfaction Survey 2026
Client: PT Contoh Riset | Research Type: CSAT
```

### Standar UI

- Container maksimal mengikuti `max-w-7xl`.
- Header detail menggunakan card putih dengan border.
- Judul detail harus dominan.
- Nomor dokumen seperti Proposal Number atau Project Number harus mudah dikenali.
- Jangan membuat hero besar untuk halaman operasional.

## 5. Summary Card

### Tujuan

Menampilkan metrik atau ringkasan angka utama.

### Pola

```text
+-----------------------------+
| Total Proposal              |
| 12                          |
+-----------------------------+
```

### Standar UI

- Background putih.
- Border slate tipis.
- Radius kecil.
- Label kecil dengan warna slate.
- Angka besar, jelas, dan tebal.
- Gunakan grid responsif.

### Penggunaan

- Client Detail summary.
- Dashboard summary.
- Project summary.
- Relationship summary.

## 6. Information Card

### Tujuan

Menampilkan data terstruktur dalam satu konteks.

### Pola

```text
+----------------------------------+
| Informasi Client                 |
| Nama Client       PT Contoh      |
| Industry          Market Research|
| Kota              Jakarta        |
+----------------------------------+
```

### Standar UI

- Background putih.
- Border `slate-200`.
- Radius `rounded-lg`.
- Padding konsisten.
- Header card menggunakan font semibold.
- Label menggunakan ukuran kecil dan warna slate.
- Value menggunakan warna slate gelap.
- Value kosong menggunakan `-`.

### Penggunaan

- Informasi Client.
- Informasi Proposal.
- Informasi Project.
- Proposal Asal.
- Informasi Sistem.

## 7. Status Badge

### Tujuan

Membuat status bisnis mudah dikenali.

### Proposal Status

| Status | Label UI | Warna |
| --- | --- | --- |
| Draft | Draft | Slate |
| Sent | Dikirim | Sky |
| Revised | Revisi | Amber |
| Approved | Disetujui | Emerald |
| Rejected | Ditolak | Red |

### Client Status

| Status | Label UI | Warna |
| --- | --- | --- |
| Active | Active | Emerald |
| Prospect | Prospect | Amber |
| Negotiation | Negotiation | Sky |
| Dormant | Dormant | Orange |
| Inactive | Inactive | Red |

### Project Status

| Status | Label UI | Warna |
| --- | --- | --- |
| Setup | Setup | Slate |
| Ready | Ready | Sky |
| Fieldwork | Fieldwork | Indigo |
| QC | QC | Amber |
| Analysis | Analysis | Violet |
| Reporting | Reporting | Cyan |
| Completed | Completed | Emerald |
| Cancelled | Cancelled | Red |

### Standar UI

- Badge menggunakan background soft.
- Text warna lebih gelap dari background.
- Gunakan ring/border tipis.
- Ukuran compact.
- Jangan menggunakan warna status sebagai background seluruh card.

## 8. Next Business Action

### Tujuan

Menampilkan action bisnis berikutnya berdasarkan status saat ini.

### Prinsip

- Action harus kontekstual.
- Tidak menggunakan dropdown status bebas.
- Hanya action valid yang ditampilkan.
- Action utama menggunakan button primary.
- Action destructive menggunakan warna red.
- Action warning menggunakan warna amber.

### Contoh Proposal

```text
Status: Draft
Action: [Kirim ke Client]
```

```text
Status: Dikirim
Action: [Tandai Perlu Revisi] [Setujui Proposal] [Tolak Proposal]
```

### Contoh Project

```text
Status: Setup
Action: [Tandai Ready]
```

### Standar UI

- Letakkan pada card kanan atau area action yang mudah ditemukan.
- Tampilkan deskripsi singkat status saat ini.
- Disable tombol saat loading.
- Tampilkan error action dekat area tombol.

## 9. Timeline Component

### Tujuan

Menampilkan riwayat atau lifecycle.

### Jenis Timeline

1. Activity Timeline.
2. Status Lifecycle Timeline.

### Activity Timeline

Pola:

```text
Proposal dibuat
26 Jul 2026
Proposal Customer Satisfaction Survey 2026 telah dibuat.
```

Standar:

- Urut terbaru di atas.
- Title semibold.
- Date kecil dengan warna slate.
- Description satu sampai dua baris.
- Jika kosong tampilkan empty state.

### Status Lifecycle Timeline

Pola:

```text
[Setup] -> [Ready] -> [Fieldwork] -> [QC] -> [Analysis] -> [Reporting] -> [Completed]
```

Standar:

- Status aktif ditandai jelas.
- Status yang sudah lewat terlihat completed.
- Status berikutnya tetap terlihat.
- Untuk MVP dapat berupa stepper sederhana.

## 10. Placeholder Card

### Tujuan

Menandai modul yang akan dikembangkan tanpa membuat user mengira fitur rusak.

### Pola

```text
Questionnaire
Belum dimulai
Instrumen riset untuk project ini akan dikelola di sini.
```

### Standar UI

- Gunakan label `Belum dimulai`, `Coming Soon`, atau `Phase berikutnya`.
- Tidak menampilkan tombol aktif jika modul belum tersedia.
- Deskripsi singkat maksimal dua baris.
- Gunakan card konsisten dengan border.

## 11. Loading State

### Tujuan

Memberi tanda bahwa data sedang dimuat.

### Standar Pesan

```text
Memuat data...
Memuat detail proposal...
Memuat detail project...
Memuat data setup project...
```

### Standar UI

- Untuk halaman detail gunakan skeleton card.
- Untuk list gunakan text loading dalam area table/card.
- Untuk submit gunakan loading label pada tombol.
- Disable primary action saat submit berjalan.

### Contoh Button Loading

```text
Menyimpan...
Membuat Project...
Memperbarui Status...
```

## 12. Empty State

### Tujuan

Menjelaskan bahwa data memang belum ada.

### Standar UI

- Title semibold.
- Description singkat.
- Optional primary action jika user bisa membuat data.
- Jangan menggunakan warna merah.

### Contoh

```text
Belum ada proposal
Proposal yang dibuat akan tampil di sini.
```

```text
Belum ada aktivitas
Aktivitas client akan tercatat otomatis dari modul bisnis.
```

## 13. Error State

### Tujuan

Menjelaskan masalah dan memberi jalan keluar.

### Standar UI

- Gunakan warna red soft.
- Title jelas.
- Pesan menjelaskan kondisi.
- Sediakan action `Coba Lagi` jika bisa retry.
- Sediakan navigasi balik jika data tidak ditemukan.

### Contoh

```text
Detail proposal belum bisa ditampilkan
Tidak dapat mengambil detail proposal. Periksa koneksi server lalu coba lagi.
[Coba Lagi] [Kembali ke Proposal]
```

### Error umum

| Kondisi | Pesan |
| --- | --- |
| Data tidak ditemukan | Data tidak ditemukan. |
| Backend tidak aktif | Tidak dapat terhubung ke server. |
| Validasi gagal | Periksa kembali data yang wajib diisi. |
| Action gagal | Aksi belum bisa diproses. Silakan coba lagi. |

## 14. Currency Format

### Standar

Gunakan format Indonesia:

```text
Rp 25.000.000
```

Rules:

- Currency: IDR.
- Tidak perlu decimal untuk Rupiah.
- Jika kosong tampilkan `-`.
- Jangan tampilkan `Rp 0` untuk data yang belum diisi, kecuali nilai nol memang bermakna.

### Label yang disarankan

- `Estimasi Nilai Proposal (Rp)`.
- `Project Value`.
- `Total Contract Value`.
- `Total Revenue`.

## 15. Date Format

### Standar

Gunakan format Indonesia:

```text
26 Jul 2026
```

Rules:

- Tanggal detail menggunakan `day month year`.
- Jika kosong tampilkan `-`.
- Timestamp penuh hanya digunakan jika dibutuhkan untuk audit.

### Label umum

- `Tanggal Dibuat`.
- `Created Date`.
- `Updated Date`.
- `Last Activity`.
- `Customer Since`.
- `Approved Date`.

Catatan:

- Lokalisasi penuh dapat memutuskan apakah label Inggris seperti `Created Date` diterjemahkan menjadi `Tanggal Dibuat`.

## 16. Button Style

### Primary Button

Penggunaan:

- Action utama halaman.
- Submit form.
- Next Business Action utama.

Contoh:

```text
[+ Proposal Baru]
[Simpan Draft]
[Buat Project]
[Tandai Ready]
```

Style:

- Background slate gelap.
- Text putih.
- Height konsisten.
- Radius kecil.
- Font semibold.

### Secondary Button

Penggunaan:

- Batal.
- Kembali.
- Coba Lagi.

Style:

- Background putih.
- Border slate.
- Text slate.

### Destructive Button

Penggunaan:

- Tolak Proposal.
- Hapus data.
- Cancel Project jika disetujui.

Style:

- Background red.
- Text putih.
- Gunakan hanya untuk aksi berisiko.

### Warning Button

Penggunaan:

- Tandai Perlu Revisi.

Style:

- Background amber.
- Text putih.

## 17. Form Layout

### Prinsip

- Form dibuat ringkas.
- Field wajib jelas.
- Section dikelompokkan berdasarkan konteks.
- Informasi sistem read-only dipisahkan dari field input.
- Action buttons berada di bagian bawah form.

### Layout Proposal Create

```text
Informasi Proposal
- Client
- Proposal Title
- Research Type
- Estimasi Nilai Proposal

Informasi Sistem
- Proposal Number
- Proposal Owner
- Status
- Created Date
- Updated Date
```

### Layout Setup Project Review

```text
Ringkasan Proposal
Ringkasan Client
Project Information
Informasi Sistem
Checklist Data
```

### Standar Field

- Input height konsisten.
- Border slate.
- Focus border slate gelap.
- Label di atas input.
- Help text jika field perlu penjelasan.

## 18. Validation Style

### Prinsip

- Validasi ditampilkan dekat field.
- Pesan harus spesifik.
- Jangan hanya menggunakan warna tanpa teks.
- Validasi frontend membantu user, validasi backend tetap wajib.

### Style

- Text red.
- Ukuran kecil.
- Input error menggunakan border red.
- Summary error hanya jika error lintas form.

### Contoh Pesan

```text
Client wajib dipilih.
Judul proposal wajib diisi.
Nama project wajib diisi.
Estimasi nilai proposal tidak boleh negatif.
```

## 19. Standar Layout Halaman

### List Page

```text
Header + Primary Action
Toolbar Search / Filter / Sort
Table
Empty / Loading / Error
```

### Detail Page

```text
Breadcrumb
Header Detail
Main Grid
Information Cards
Timeline / Activity
Related Modules
```

### Create Page

```text
Breadcrumb
Header
Form Section
System Info
Action Buttons
```

## 20. Rekomendasi Implementasi

Saat mulai implementasi komponen reusable, buat helper atau component bertahap sesuai kebutuhan.

Prioritas reusable component:

1. `StatusBadge`.
2. `PageHeader`.
3. `InfoCard`.
4. `DetailItem`.
5. `SummaryCard`.
6. `EmptyState`.
7. `ErrorState`.
8. `LoadingSkeleton`.
9. `NextBusinessAction`.
10. `Timeline`.

Rekomendasi teknis:

- Jangan refactor semua halaman sekaligus.
- Mulai dari modul Project sebagai consumer pertama.
- Setelah stabil, adopsi bertahap ke Proposal dan Client.
- Simpan format currency dan date sebagai utility bersama.
- Simpan mapping status sebagai konfigurasi agar warna konsisten.

## 21. Komponen yang Perlu Distandarkan di Sprint Berikutnya

Candidate shared components:

- Status Badge lintas Client, Proposal, dan Project.
- Currency formatter.
- Date formatter.
- Form error message.
- Detail skeleton.
- Empty state.
- Page section header.

## 22. Acceptance Criteria Design System

1. Seluruh modul baru mengikuti Page Header standar.
2. Summary Card menggunakan pola visual yang sama.
3. Information Card menggunakan struktur label/value yang sama.
4. Status Badge konsisten lintas modul.
5. Next Business Action tidak menggunakan dropdown status bebas.
6. Timeline memiliki pola visual yang sama.
7. Placeholder Card jelas dan tidak terlihat seperti error.
8. Loading State konsisten.
9. Empty State konsisten.
10. Error State konsisten.
11. Currency menggunakan format Rupiah Indonesia.
12. Date menggunakan format Indonesia.
13. Button style konsisten.
14. Form layout konsisten.
15. Validation style konsisten.

## 23. Catatan Product Development

Design System v1 adalah baseline. Tujuannya bukan membuat design system besar sejak awal, tetapi mencegah setiap modul tampil berbeda.

Prinsip implementasi:

- Standarkan sambil membangun.
- Jangan memaksa refactor besar sebelum modul Project berjalan.
- Komponen reusable dibuat ketika pola sudah digunakan minimal dua sampai tiga kali.
