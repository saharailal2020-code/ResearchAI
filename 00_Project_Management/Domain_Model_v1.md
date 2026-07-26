# ResearchAI Domain Model v1

Status:
Proposed for Domain Architecture Freeze

Tanggal:
26 Juli 2026

## Tujuan

Membekukan hubungan domain inti ResearchAI untuk MVP agar pengembangan modul berikutnya memiliki fondasi yang konsisten.

Domain model ini berfokus pada alur utama:

```text
Client -> Proposal -> Project -> Questionnaire -> Sample -> Fieldwork -> QC -> Dataset -> Dashboard -> Report -> Invoice
```

## Prinsip Domain

1. Client adalah pusat relationship.
2. Proposal adalah dokumen penawaran bisnis.
3. Project adalah pusat pekerjaan operasional.
4. Questionnaire, Sample, Fieldwork, QC, Dataset, Dashboard, Report, dan Invoice berada di bawah konteks Project.
5. Activity adalah cross-cutting behavior.
6. Document Management akan menjadi cross-domain service pada phase berikutnya.
7. Modul dibangun bertahap, tetapi relasi domain harus konsisten sejak awal.

## Diagram ASCII

```text
Client
   |
   +-- Contact
   |
   +-- Activity Timeline
   |
   +-- Proposal
   |      |
   |      +-- Proposal Number
   |      +-- Proposal Owner
   |      +-- Proposal Status
   |      |
   |      v
   |   Setup Project
   |
   +-- Project
          |
          +-- Questionnaire
          |
          +-- Sample
          |
          +-- Fieldwork
          |
          +-- QC
          |
          +-- Dataset
          |
          +-- Dashboard
          |
          +-- Report
          |
          +-- Invoice
```

## Domain Entity

### Client

Tujuan:
Menjadi pusat informasi relationship dengan organisasi client.

Memiliki:

- Contact
- Activity
- Proposal
- Project
- Report
- Invoice

Dependency:

- User untuk owner atau creator
- Activity untuk riwayat

Dependent modules:

- Proposal
- Project
- Invoice
- Report

### Proposal

Tujuan:
Menjadi dokumen penawaran bisnis kepada client.

Memiliki:

- Proposal Number
- Proposal Owner
- Client
- Research Type
- Objective
- Methodology Summary
- Estimated Timeline
- Estimated Budget
- Status

Dependency:

- Client wajib ada.
- User sebagai Proposal Owner.

Dependent modules:

- Project dibuat dari Proposal Approved.

Business rule utama:

- Proposal Approved dapat masuk Setup Project.
- Proposal tetap historical record.
- Proposal tidak otomatis menjadi Project.

### Project

Tujuan:
Menjadi pekerjaan operasional setelah Proposal disetujui.

Memiliki:

- Client
- Proposal asal
- Project Number
- Project Name
- Project Manager
- Status
- Timeline
- Project Value sementara

Dependency:

- Client wajib ada.
- Proposal Approved wajib untuk MVP.
- User sebagai Project Manager jika sudah ditentukan.

Dependent modules:

- Questionnaire
- Sample
- Fieldwork
- QC
- Dataset
- Dashboard
- Report
- Invoice

Business rule utama:

- Status awal Project adalah `Setup`.
- Project tidak dibuat otomatis.
- Untuk MVP, satu Proposal maksimal satu Project.

### Questionnaire

Tujuan:
Menjadi instrumen riset yang digunakan dalam project.

Dependency:

- Project wajib ada.

Dependent modules:

- Fieldwork
- QC
- Dataset

Output:

- Draft questionnaire
- Final questionnaire
- Version history pada phase berikutnya

### Sample

Tujuan:
Menentukan target responden, jumlah sample, quota, segment, dan distribusi sample.

Dependency:

- Project wajib ada.
- Research Type dan methodology dari Project menjadi input.

Dependent modules:

- Fieldwork
- Monitoring
- QC

Output:

- Sample plan
- Quota structure
- Target sample size

### Fieldwork

Tujuan:
Mengelola pelaksanaan pengumpulan data.

Dependency:

- Project wajib ada.
- Questionnaire sebaiknya tersedia.
- Sample sebaiknya tersedia.

Dependent modules:

- QC
- Dataset
- Monitoring

Output:

- Raw data
- Submission progress
- Fieldwork issue log

### QC

Tujuan:
Memastikan data yang terkumpul memenuhi standar kualitas.

Dependency:

- Fieldwork wajib menghasilkan data.
- Project wajib ada.

Dependent modules:

- Dataset
- Analysis

Output:

- QC result
- Cleaned or approved data
- Rejected or flagged records

### Dataset

Tujuan:
Menjadi data yang siap dianalisis setelah QC.

Dependency:

- Project wajib ada.
- QC sebaiknya selesai.

Dependent modules:

- Dashboard
- Report
- AI Insight pada phase berikutnya

Output:

- Clean dataset
- Data dictionary
- Data readiness status

### Dashboard

Tujuan:
Menampilkan visualisasi dan monitoring hasil riset.

Dependency:

- Dataset wajib tersedia.

Dependent modules:

- Report
- Client delivery pada phase berikutnya

Output:

- Dashboard view
- Chart
- KPI

### Report

Tujuan:
Menjadi deliverable naratif dan analitik untuk client.

Dependency:

- Dataset
- Dashboard
- Project

Dependent modules:

- Invoice
- Knowledge Repository pada phase berikutnya

Output:

- Draft report
- Final report
- Recommendation

### Invoice

Tujuan:
Mengelola tagihan atas pekerjaan riset.

Dependency:

- Client wajib ada.
- Project sebaiknya ada.
- Contract akan menjadi dependency pada phase berikutnya.

Output:

- Invoice record
- Payment status pada phase berikutnya

## Dependency Summary

```text
Client
  required by Proposal
  required by Project
  required by Invoice

Proposal
  requires Client
  required by Project Setup in MVP

Project
  requires Client
  requires Approved Proposal in MVP
  required by Questionnaire, Sample, Fieldwork, QC, Dataset, Dashboard, Report, Invoice

Questionnaire
  requires Project
  supports Fieldwork

Sample
  requires Project
  supports Fieldwork

Fieldwork
  requires Project
  ideally requires Questionnaire and Sample
  produces raw data

QC
  requires Fieldwork data
  produces approved data

Dataset
  requires QC output
  supports Dashboard and Report

Dashboard
  requires Dataset
  supports Report

Report
  requires Project and Dataset
  supports Invoice and Knowledge Repository

Invoice
  requires Client
  ideally requires Project or Contract
```

## Domain Rules

1. Client can exist without Proposal.
2. Proposal cannot exist without Client.
3. Project cannot exist without Client.
4. For MVP, Project cannot exist without Approved Proposal.
5. Proposal can exist without Project.
6. Approved Proposal can create Project through Setup Project.
7. Rejected Proposal cannot create Project.
8. Project owns delivery modules.
9. Dataset should not exist without Project.
10. Report should not exist without Project.
11. Invoice should be connected to Client and preferably Project.
12. Every business event should create Activity when relevant.

## Notes for Implementation

This document is conceptual. It is not a database schema.

Database design, API design, and UI design must use this document as a domain reference but still require separate design review before implementation.
