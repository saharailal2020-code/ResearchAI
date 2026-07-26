# Project UI Architecture v1

Status:
Draft for Product Owner Review

Tanggal:
26 Juli 2026

Basis:

- WF-005 Project Detail
- WF-004 Project Setup Review
- ADR-002 Proposal vs Project
- ADR-003 Project Lifecycle
- Domain Model v1

## 1. Tujuan

Dokumen ini mendefinisikan arsitektur UI modul Project agar Project Management ResearchAI berkembang secara konsisten.

Project adalah pusat operasional ResearchAI. Karena itu UI Project harus mampu menampung workflow delivery riset dari Setup sampai Completed tanpa membuat halaman awal terlalu kompleks.

## 2. Prinsip UI Project

1. Project Detail adalah home operasional untuk satu Project.
2. Header Project harus selalu menampilkan identitas Project.
3. Status Project harus selalu terlihat.
4. Client dan Proposal asal harus mudah diakses.
5. Next Business Action harus kontekstual, bukan dropdown bebas.
6. Modul operasional tampil sebagai area bertahap, bukan dipaksa lengkap sejak MVP.
7. Placeholder harus jelas agar user tahu fitur belum dimulai, bukan error.
8. UI harus konsisten dengan Client Management dan Proposal Management.

## 3. Navigasi Project

Navigasi utama:

```text
Sidebar
  -> Project
      -> Project List
      -> Project Detail
```

Navigasi dari Proposal:

```text
Proposal Detail
  -> Setup Project
  -> Review Setup Project
  -> Project Detail
```

Navigasi dari Client:

```text
Client Detail
  -> Projects Tab
  -> Project Detail
```

Navigasi balik:

```text
Project Detail
  -> Client Detail
  -> Proposal Detail
```

## 4. Sidebar

Sidebar MVP:

```text
Dasbor
Client
Proposal
Project
Data
Analisis AI
Laporan
```

Behavior:

- Menu `Project` mengarah ke Project List jika sudah tersedia.
- Jika Project List belum tersedia, menu dapat mengarah ke placeholder Project.
- Saat user berada di Project Detail, menu `Project` aktif.

Label disarankan:

```text
Project
```

Alasan:

- Istilah `Project` umum digunakan di bisnis riset dan sudah konsisten dengan dokumen ResearchAI.
- Terjemahan `Proyek` bisa dipertimbangkan pada lokalisasi penuh, tetapi saat ini istilah campuran sudah digunakan.

## 5. Struktur Halaman Project Detail

Struktur utama:

```text
Breadcrumb
Header Project
Primary Grid
Timeline Project
Operational Modules
Activity / Future Tabs
```

Wireframe:

```text
Project / Project Detail

+--------------------------------------------------------------------------+
| PRJ-20260726-0001                                      [Setup]           |
| Customer Satisfaction Survey 2026                                        |
| Client: PT Contoh Riset     Research Type: CSAT     Value: Rp 25.000.000 |
| Proposal: PROP-20260726-0001                 PM: Belum ditentukan        |
+--------------------------------------------------------------------------+

+----------------------------------------------+---------------------------+
| Card: Informasi Project                       | Card: Next Business Action|
| Project Number                                |                           |
| Project Name                                  | [Tandai Ready]            |
| Research Type                                 |                           |
| Project Value                                 | Status sekarang: Setup    |
| Project Manager                               |                           |
| Start Date / End Date                         |                           |
+----------------------------------------------+---------------------------+

+----------------------------------------------+---------------------------+
| Card: Client                                  | Card: Proposal Asal       |
| Nama Client                                   | Proposal Number           |
| Industry                                      | Proposal Title            |
| Kota                                          | Proposal Owner            |
| PIC / Email / HP                              | Approved Date             |
| [Buka Client]                                 | [Buka Proposal]           |
+----------------------------------------------+---------------------------+

Card: Timeline Project
[Setup] -> [Ready] -> [Fieldwork] -> [QC] -> [Analysis] -> [Reporting] -> [Completed]

Card: Modul Operasional
+----------------+----------------+----------------+----------------+
| Questionnaire  | Sample         | Fieldwork      | QC             |
| Belum dimulai  | Belum dimulai  | Belum dimulai  | Belum dimulai  |
+----------------+----------------+----------------+----------------+
| Dataset        | Dashboard      | Report         | Invoice        |
| Belum dimulai  | Coming Soon    | Coming Soon    | Phase berikut  |
+----------------+----------------+----------------+----------------+
```

## 6. Card Utama

### Header Card

Informasi yang selalu tampil:

- Project Number.
- Project Name.
- Project Status.
- Client Name.
- Research Type.
- Project Value.
- Proposal Reference.
- Project Manager.

Tujuan:

- Memberi konteks instan.
- Membedakan Project dari Proposal.

### Informasi Project Card

Informasi:

- Project Number.
- Project Name.
- Research Type.
- Project Value.
- Project Manager.
- Start Date.
- End Date.
- Created Date.
- Updated Date.

### Next Business Action Card

Informasi:

- Status saat ini.
- Tombol action berikutnya.
- Keterangan singkat apa arti action.

Contoh:

```text
Status sekarang: Setup
Action berikutnya: Tandai Ready
```

### Client Card

Informasi:

- Nama Client.
- Industry.
- Kota.
- Status.
- PIC.
- Email.
- Nomor HP.
- Link ke Client Detail.

### Proposal Asal Card

Informasi:

- Proposal Number.
- Proposal Title.
- Proposal Owner.
- Proposal Status.
- Approved Date.
- Estimasi Nilai Proposal.
- Link ke Proposal Detail.

### Timeline Card

Informasi:

- Status lifecycle Project.
- Status aktif.
- Tanggal perpindahan status jika tersedia.

### Operational Modules Card

Informasi:

- Questionnaire.
- Sample.
- Fieldwork.
- QC.
- Dataset.
- Dashboard.
- Report.
- Invoice future.

## 7. Informasi yang Harus Selalu Tampil

Informasi berikut harus selalu tersedia pada Project Detail:

- Project Number.
- Project Name.
- Project Status.
- Client Name.
- Proposal Number.
- Research Type.
- Project Value.
- Next Business Action atau status selesai.

Alasan:

- Ini adalah konteks minimum untuk membaca Project secara operasional.
- User tidak perlu berpindah halaman untuk mengetahui Project sedang berada di tahap apa.

## 8. Informasi yang Dapat Menjadi Tab di Masa Depan

Saat Project semakin kompleks, informasi dapat dipindahkan menjadi tab.

Candidate tabs:

- Overview.
- Activity.
- Questionnaire.
- Sample.
- Fieldwork.
- QC.
- Dataset.
- Dashboard.
- Report.
- Invoice.
- Documents.
- Team.
- Timeline.

Rekomendasi MVP:

- Jangan langsung membuat semua tab.
- Gunakan card placeholder dulu.
- Tab dapat dibuat ketika masing-masing modul sudah punya data dan workflow.

## 9. Responsive Desktop

Target awal Sprint Project adalah desktop.

Rules:

- Header full width.
- Grid 2 kolom pada desktop.
- Card utama tidak nested.
- Operational module menggunakan grid.
- Text tidak overlap.
- Action utama mudah ditemukan.

Responsive fallback:

```text
Desktop:
2 kolom

Tablet / narrow:
1 kolom
```

## 10. Business Rules UI

1. Project Detail tidak boleh mengubah Client.
2. Project Detail tidak boleh mengubah Proposal asal.
3. Status Project tidak diedit bebas.
4. Status Project berubah lewat Next Business Action.
5. Project Number menjadi identitas utama.
6. Proposal Number hanya referensi historical.
7. Modul operasional berada di bawah Project.
8. Activity Project adalah cross-cutting behavior.

## 11. Acceptance Criteria

1. Sidebar memiliki navigasi Project ketika modul Project mulai diimplementasikan.
2. Project Detail dapat diakses dari Setup Project success flow.
3. Header Project menampilkan identitas utama.
4. Project Status selalu terlihat.
5. Client Card tersedia.
6. Proposal Asal Card tersedia.
7. Timeline Project tersedia.
8. Next Business Action tersedia.
9. Placeholder modul operasional tersedia.
10. UI konsisten dengan Client dan Proposal.
11. Informasi wajib selalu tampil tanpa harus membuka tab tambahan.
12. Future tab structure terdokumentasi.

## 12. Risiko

### Risiko 1: Terlalu banyak card membuat halaman berat

Mitigasi:

- Prioritaskan header, informasi project, client, proposal, action, timeline.
- Modul lain dibuat ringkas sebagai placeholder.

### Risiko 2: User mengira placeholder sudah fitur aktif

Mitigasi:

- Gunakan status `Belum dimulai`, `Coming Soon`, atau `Phase berikutnya`.
- Hindari tombol aktif untuk modul yang belum tersedia.

### Risiko 3: Project dan Proposal tertukar

Mitigasi:

- Project Number paling dominan.
- Proposal Asal berada di card referensi, bukan header utama.

### Risiko 4: Workflow Project terlalu cepat dipaksa lengkap

Mitigasi:

- Project Detail MVP hanya pusat informasi dan pintu masuk modul.
- Modul operasional dikembangkan bertahap.

### Risiko 5: Sidebar terlalu penuh

Mitigasi:

- Hanya tampilkan domain utama di sidebar.
- Submodule seperti Questionnaire, Fieldwork, QC, Dataset, Report masuk di dalam Project Detail, bukan sidebar utama.

## 13. Rekomendasi Product Development

Urutan implementasi yang disarankan setelah design freeze:

1. Project backend foundation.
2. Setup Project API.
3. Project Detail read-only.
4. Review Setup Project frontend.
5. Project Detail placeholder modules.
6. Project Status Actions.
7. Questionnaire MVP.
8. Sample MVP.
9. Fieldwork MVP.
10. QC MVP.
