# ADR-001 Proposal to Project

Status:
Proposed for Product Owner Review

Tanggal:
26 Juli 2026

## Context

ResearchAI dibangun sebagai Operating System untuk perusahaan riset, bukan CRM biasa.

Dalam alur bisnis ResearchAI, Proposal adalah bagian dari Business Development, sedangkan Project adalah pusat delivery riset.

Alur strategis yang sudah disetujui:

```text
Client -> Proposal -> Project -> Questionnaire -> Sampling -> Fieldwork -> QC -> Dataset -> Dashboard -> Report -> Invoice
```

Pada Proposal Workflow MVP v0.1, Proposal yang berstatus `Approved` menjadi kandidat untuk Project Setup, tetapi Project belum dibuat otomatis pada sprint Proposal.

Keputusan ini perlu diperjelas sebelum masuk Project Management Module agar hubungan Client, Proposal, dan Project tidak menjadi rancu.

## Decision

Project dibuat setelah Proposal berstatus `Approved`.

Untuk MVP, satu Proposal menghasilkan maksimal satu Project.

Project harus selalu terhubung ke Client.

Project sebaiknya berasal dari Proposal Approved, tetapi untuk kebutuhan operasional tertentu pada versi berikutnya, Project dapat dibuat tanpa Proposal dengan alasan bisnis yang jelas dan permission khusus.

Pada MVP awal Project Management, rekomendasi utama adalah:

- Project dibuat dari Proposal Approved.
- Proposal tidak otomatis berubah menjadi Project.
- User melakukan action eksplisit `Setup Project` atau sejenisnya pada Proposal Approved.
- Project mewarisi sebagian data dari Proposal sebagai data awal.
- Proposal tetap menjadi record business development dan tidak hilang setelah Project dibuat.

## Rationale

Project bukan sekadar status lanjutan dari Proposal.

Proposal menjawab:

- Apa kebutuhan client?
- Apa jenis riset yang ditawarkan?
- Berapa estimasi budget?
- Apa metodologi dan timeline awal?
- Apakah client menyetujui?

Project menjawab:

- Bagaimana pekerjaan riset dijalankan?
- Siapa Project Manager?
- Apa jadwal kerja detail?
- Apa questionnaire, sampling, fieldwork, monitoring, QC, dataset, dashboard, report, dan invoice?

Karena tanggung jawab domainnya berbeda, Proposal dan Project harus menjadi entity terpisah tetapi saling terhubung.

## Business Rules

1. Project hanya dapat dibuat dari Proposal dengan status `Approved` pada MVP.
2. Proposal `Rejected` tidak dapat menjadi Project.
3. Proposal `Draft`, `Sent`, dan `Revised` belum dapat menjadi Project.
4. Satu Proposal menghasilkan maksimal satu Project pada MVP.
5. Project wajib memiliki Client.
6. Jika Project dibuat dari Proposal, Client Project harus sama dengan Client Proposal.
7. Project menyimpan referensi ke Proposal asal.
8. Proposal tetap dapat dibaca setelah menjadi Project.
9. Proposal sebaiknya dikunci dari perubahan status setelah Project dibuat.
10. Edit konten Proposal setelah Project dibuat perlu dibatasi atau dibuat sebagai change note pada phase berikutnya.

## Data Inheritance

Data yang diwariskan dari Proposal ke Project sebagai default awal:

- client_id
- proposal_id
- project_name dari proposal_title
- research_type
- project_objective dari research_objective
- methodology_summary sebagai initial methodology note
- estimated_budget sebagai initial project value atau estimated contract value
- estimated_timeline sebagai initial timeline note
- proposal_owner sebagai business development reference

Data yang tidak otomatis dibawa:

- proposal_number sebagai project_number
- proposal status
- proposal activity history sebagai project activity history
- approved_at sebagai project start date
- estimated budget sebagai invoice amount final
- methodology summary sebagai final research design
- proposal documents sebagai project documents tanpa aturan attachment yang jelas
- quotation dan contract karena belum tersedia pada MVP

## Consequences

### Positive

- Boundary Proposal dan Project menjadi jelas.
- Client 360 dapat menampilkan history proposal dan project secara terpisah.
- Project dapat berkembang menjadi delivery center tanpa membebani Proposal.
- Proposal Approved tetap menjadi bukti business decision.
- Alur Project dapat dibangun bertahap tanpa merombak Proposal.

### Negative

- Perlu desain Project Setup agar user memahami bahwa Project dibuat secara eksplisit.
- Perlu validasi agar satu Proposal tidak membuat banyak Project tanpa aturan.
- Perlu aturan apakah Proposal bisa diedit setelah Project dibuat.
- Perlu field relasi `proposal_id` pada Project.

### Neutral

- Quotation dan Contract dapat ditambahkan di phase berikutnya tanpa mengubah keputusan dasar Proposal -> Project.
- Document Management dapat menempel ke Proposal dan Project secara terpisah setelah desain attachment lintas domain selesai.

## Candidate Project Initial Status

Status awal Project yang direkomendasikan:

```text
Setup
```

Alasan:

Project yang baru dibuat dari Proposal Approved belum langsung berjalan. Biasanya masih perlu setup internal:

- assign Project Manager,
- finalisasi timeline,
- finalisasi questionnaire,
- sampling,
- resource planning,
- kickoff internal,
- kickoff client.

## Alternatives Considered

### Alternative 1: Proposal otomatis menjadi Project saat Approved

Ditolak untuk MVP.

Alasan:

- Terlalu otomatis dan berisiko membuat project sebelum tim siap.
- Project membutuhkan data operasional tambahan.
- Tidak semua proposal approved langsung dapat dijalankan tanpa setup.

### Alternative 2: Project selalu wajib memiliki Contract

Ditunda.

Alasan:

- Contract belum menjadi scope MVP saat ini.
- Jika dipaksakan, Project Management tertahan oleh Contract Module.

### Alternative 3: Satu Proposal dapat menghasilkan banyak Project sejak awal

Ditunda.

Alasan:

- Ada kemungkinan bisnis nyata seperti multi-wave atau multi-country project.
- Namun untuk MVP, aturan ini menambah kompleksitas.
- MVP lebih aman memakai satu Proposal satu Project.

## Open Questions

1. Apakah Beerka pernah menjalankan satu proposal yang dipecah menjadi beberapa project?
2. Apakah project internal tanpa proposal perlu didukung sejak MVP?
3. Apakah setelah Project dibuat, Proposal boleh diedit atau harus read-only?
4. Apakah Project Number perlu otomatis seperti Proposal Number?
5. Apakah status awal `Setup` sudah sesuai istilah operasional Beerka?
6. Apakah Project Setup perlu menampilkan checklist awal?
7. Apakah estimated budget dari Proposal menjadi project value sementara atau hanya referensi?

## Decision Owner

Product Owner dan Architecture Review.

## Next Step

Review dokumen `Project_Discovery_v1.md` sebelum membuat design sprint Project Management.
