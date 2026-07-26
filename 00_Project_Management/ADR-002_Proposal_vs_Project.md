# ADR-002 Proposal vs Project

Status:
Proposed for Domain Architecture Freeze

Tanggal:
26 Juli 2026

## Tujuan

Membekukan batas arsitektur antara Proposal dan Project agar modul berikutnya tidak mencampur domain Business Development dengan domain Project Management.

Keputusan ini menjadi acuan sebelum ResearchAI membangun Project Management, Questionnaire, Sample, Fieldwork, QC, Dataset, Dashboard, Report, dan Invoice.

## Latar Belakang

ResearchAI adalah Operating System untuk perusahaan riset. Dalam workflow utama ResearchAI, Client dapat memiliki Proposal, Proposal yang disetujui dapat menjadi Project, dan Project menjadi pusat pekerjaan operasional riset.

Proposal dan Project sering terlihat berdekatan karena keduanya berada dalam alur bisnis yang sama:

```text
Client -> Proposal -> Project
```

Namun secara domain, keduanya memiliki tanggung jawab yang berbeda.

Proposal adalah dokumen penawaran bisnis. Proposal menjelaskan apa yang ditawarkan kepada client, termasuk kebutuhan riset, jenis riset, objective, pendekatan metodologi, timeline estimasi, budget estimasi, dan status keputusan client.

Project adalah pekerjaan operasional. Project menjelaskan bagaimana riset yang disetujui akan dijalankan, siapa yang bertanggung jawab, apa instrumen risetnya, bagaimana sample dan fieldwork dijalankan, bagaimana QC dilakukan, bagaimana dataset disiapkan, bagaimana dashboard/report dibuat, dan bagaimana pekerjaan ditutup.

Jika batas ini tidak dibekukan, risiko terbesar adalah Proposal berubah menjadi modul operasional yang terlalu berat, atau Project kehilangan konteks bisnis asalnya.

## Keputusan Arsitektur

1. Proposal dan Project adalah dua entity berbeda.
2. Proposal adalah dokumen penawaran bisnis.
3. Project adalah pekerjaan operasional atau delivery object.
4. Proposal tetap menjadi historical record setelah Project dibuat.
5. Project dibuat dari Proposal yang berstatus `Approved`.
6. Project dibuat melalui action eksplisit `Setup Project`.
7. Project tidak dibuat otomatis saat Proposal berubah menjadi `Approved`.
8. Untuk MVP, satu Proposal menghasilkan maksimal satu Project.
9. Project wajib memiliki Client.
10. Jika Project dibuat dari Proposal, Client pada Project harus sama dengan Client pada Proposal.
11. Project menyimpan referensi ke Proposal asal.
12. Proposal tidak berubah menjadi Project; Proposal hanya menjadi sumber bisnis untuk Project.

## Business Rules

### Proposal

1. Proposal wajib terkait dengan Client.
2. Proposal memiliki Proposal Number yang unik.
3. Proposal memiliki Proposal Owner.
4. Proposal lifecycle MVP:

```text
Draft -> Dikirim ke Client -> Perlu Revisi -> Disetujui / Ditolak
```

5. Proposal `Approved` dapat digunakan untuk `Setup Project`.
6. Proposal `Rejected` tidak dapat menjadi Project.
7. Proposal `Draft`, `Sent`, dan `Revised` belum dapat menjadi Project.
8. Proposal tetap dapat dibaca setelah Project dibuat.
9. Proposal menjadi historical record atas penawaran dan keputusan bisnis.

### Project

1. Project wajib memiliki Client.
2. Untuk MVP, Project wajib berasal dari Proposal Approved.
3. Project harus menyimpan `proposal_id` sebagai referensi asal.
4. Project status awal adalah status awal lifecycle Project yang disetujui dalam ADR-003.
5. Project menjadi parent untuk modul operasional:
   - Questionnaire
   - Sample
   - Fieldwork
   - QC
   - Dataset
   - Dashboard
   - Report
   - Invoice
6. Project activity harus masuk ke Client Activity Timeline.

### Proposal to Project

1. Project dibuat melalui action `Setup Project`.
2. Action `Setup Project` hanya muncul pada Proposal `Approved`.
3. Action `Setup Project` tidak boleh muncul pada Proposal `Draft`, `Sent`, `Revised`, atau `Rejected`.
4. Untuk MVP, satu Proposal hanya dapat memiliki satu Project.
5. Setelah Project dibuat, Proposal Detail harus dapat menampilkan link ke Project.
6. Client 360 harus dapat menampilkan Project yang dibuat dari Proposal milik Client tersebut.

## Data yang Diwariskan dari Proposal ke Project

Data yang dapat diwariskan sebagai nilai awal:

- `client_id`
- `proposal_id`
- `project_name` dari `proposal_title`
- `research_type`
- `project_objective` dari `research_objective`
- `methodology_summary`
- `estimated_timeline`
- `estimated_budget` sebagai project value sementara
- `proposal_owner_id` sebagai referensi Business Development
- `approved_at` sebagai tanggal referensi approval, bukan start date final

## Data yang Tidak Otomatis Diwariskan

Data yang tidak otomatis dibawa:

- Proposal Number sebagai Project Number
- Proposal Status sebagai Project Status
- Proposal Owner sebagai Project Manager
- Proposal Activity sebagai Project Activity
- Approved Date sebagai Start Date
- Estimated Budget sebagai Invoice Final
- Proposal Document sebagai Project Document tanpa Document Management
- Quotation
- Contract
- Invoice
- Payment Terms

## Konsekuensi

### Konsekuensi Positif

- Boundary antara Business Development dan Delivery menjadi jelas.
- Proposal dapat tetap sederhana dan fokus pada penawaran bisnis.
- Project dapat berkembang menjadi delivery center tanpa membebani Proposal.
- Client 360 dapat menampilkan Proposal dan Project sebagai history terpisah.
- Activity Timeline lebih rapi karena source module jelas.
- Future modules seperti Contract, Invoice, Fieldwork, dan Report dapat menempel ke Project dengan lebih natural.

### Konsekuensi Negatif

- Dibutuhkan mekanisme `Setup Project`.
- Dibutuhkan validasi agar satu Proposal tidak membuat lebih dari satu Project pada MVP.
- Dibutuhkan aturan perubahan Proposal setelah Project dibuat.
- Project membutuhkan schema dan lifecycle sendiri.

### Konsekuensi Netral

- Quotation dan Contract dapat ditambahkan setelah Proposal dan Project stabil.
- Document Management dapat menempel pada Proposal dan Project secara terpisah.
- Multi-project dari satu Proposal bisa dipertimbangkan pada phase berikutnya.

## Future Consideration

1. Mendukung satu Proposal menjadi banyak Project untuk multi-wave, multi-country, atau multi-phase research.
2. Mendukung Project tanpa Proposal untuk internal research, recurring tracking, atau migrasi data lama.
3. Mengunci Proposal menjadi read-only setelah Project dibuat.
4. Menambahkan Contract sebagai gate sebelum Project dibuat.
5. Menambahkan Project Change Note untuk perubahan scope setelah Project berjalan.
6. Menambahkan Document Management agar dokumen Proposal dan Project dapat dikelola lintas domain.
7. Menambahkan Quotation dan Contract agar project value tidak lagi bergantung pada estimated budget.

## Decision Owner

Product Owner, Product Architecture, dan Engineering.

## Status Review

Dokumen ini perlu disetujui sebagai bagian dari Sprint A0 Domain Architecture Freeze sebelum Sprint 5 dimulai.
