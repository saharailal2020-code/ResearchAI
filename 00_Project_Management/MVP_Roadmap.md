# MVP Roadmap

Tanggal:
26 Juli 2026

Status:
Draft untuk Product Owner Review

## 1. MVP Goal

MVP ResearchAI harus membuktikan bahwa sistem dapat mengelola siklus utama perusahaan riset dari penawaran sampai pembayaran.

Flow MVP:

```text
Client
  -> Proposal
  -> Project
  -> Questionnaire
  -> Sample
  -> Fieldwork
  -> Monitoring
  -> QC
  -> Dataset
  -> Report
  -> Invoice
  -> Payment
```

## 2. MVP Scope Status

| Area | Status Saat Ini | MVP Target |
| --- | --- | --- |
| Client | Tersedia | Stabil sebagai Client 360 basic |
| Proposal | Tersedia | Stabil sebagai business document |
| Project | Tersedia | Stabil sebagai operational root |
| Questionnaire | Tersedia | Multiple Questionnaire basic |
| Sample | Belum dimulai | Sample Group dan quota basic |
| Fieldwork | Belum dimulai | Plan dan progress basic |
| Monitoring | Belum dimulai | Manual progress monitoring |
| QC | Belum dimulai | QC summary dan readiness |
| Dataset | Belum dimulai | Dataset metadata/link |
| Dashboard | Belum dimulai | Dashboard link/summary |
| Report | Belum dimulai | Report metadata/link |
| Invoice | Belum dimulai | Invoice basic |
| Payment | Belum dimulai | Payment tracking basic |
| Document | Placeholder | Document metadata/link basic |
| Knowledge | Belum dimulai | Library metadata basic |

## 3. MVP Release Phases

### MVP Phase 1 - Commercial to Project Foundation

Status:
Completed / mostly completed

Modules:

- Client.
- Proposal.
- Project.
- Multiple Questionnaire.

Business value:

- Business Development dapat mencatat proposal.
- Proposal Approved dapat menjadi Project.
- Project dapat memiliki beberapa Questionnaire sesuai target respondent.

Sprint coverage:

- Sprint 1 sampai Sprint 7.

### MVP Phase 2 - Research Preparation

Status:
Next

Modules:

- Technical Foundation minimal.
- Sample Management.
- Fieldwork Discovery.

Business value:

- Project mulai memiliki struktur operasional riset yang realistis.
- Questionnaire terhubung ke target sample.

Recommended sprints:

- Sprint 8A: Technical Foundation Planning.
- Sprint 8B: Migration Baseline.
- Sprint 8C: Integration Test Baseline.
- Sprint 8: Sample Discovery.
- Sprint 9: Sample Backend.
- Sprint 10: Sample Frontend.

Definition of Done:

- Setiap Questionnaire atau Target Respondent dapat memiliki Sample Group.
- Project Detail menampilkan Sample summary.
- Sample status dapat ditandai Ready.

### MVP Phase 3 - Research Execution

Status:
Planned

Modules:

- Fieldwork Planning.
- Resource Basic.
- Monitoring MVP.

Business value:

- Project Manager dapat melihat rencana dan progress fieldwork.
- Fieldwork Manager dapat mencatat resource dan progress dasar.

Recommended sprints:

- Sprint 11: Fieldwork Discovery.
- Sprint 12: Fieldwork Backend.
- Sprint 13: Fieldwork Frontend.
- Sprint 14: Resource Basic.
- Sprint 15: Monitoring MVP.

Definition of Done:

- Fieldwork Plan dibuat dari Project.
- Fieldwork terhubung ke Sample dan Questionnaire.
- Progress dapat dicatat manual.
- Issue lapangan dapat dicatat.

### MVP Phase 4 - Quality and Data

Status:
Planned

Modules:

- QC Foundation.
- Dataset Foundation.

Business value:

- Data tidak langsung dianggap final tanpa QC.
- Dataset dapat dilacak dari Fieldwork dan Project.

Recommended sprints:

- Sprint 16: QC Foundation.
- Sprint 17: Dataset Foundation.

Definition of Done:

- QC summary tersedia.
- Dataset dapat dibuat setelah QC.
- Dataset memiliki status Draft/Ready.

### MVP Phase 5 - Insight and Delivery

Status:
Planned

Modules:

- Dashboard Basic.
- Report Foundation.
- Document Basic.

Business value:

- Output riset mulai tercatat.
- Report dan dashboard dapat dilacak sebagai deliverable.
- Dokumen penting mulai dikelola lintas domain.

Recommended sprints:

- Sprint 18: Dashboard Basic.
- Sprint 19: Report Foundation.
- Sprint 20: Document Basic.

Definition of Done:

- Report dapat dibuat dari Project/Dataset.
- Dashboard link atau summary dapat dicatat.
- Document dapat melekat ke domain utama.

### MVP Phase 6 - Finance Closure

Status:
Planned

Modules:

- Invoice Foundation.
- Payment Tracking.

Business value:

- Siklus bisnis tertutup dari delivery ke revenue.
- Management dapat melihat invoice dan payment status.

Recommended sprints:

- Sprint 21: Invoice Foundation.
- Sprint 22: Payment Tracking.

Definition of Done:

- Invoice dapat dibuat dari Project.
- Payment dapat dicatat terhadap Invoice.
- Status invoice dapat berubah menjadi Paid.

### MVP Phase 7 - Knowledge and Operating Overview

Status:
Planned

Modules:

- Knowledge Library Basic.
- MVP Operating Dashboard.
- MVP Hardening.

Business value:

- Knowledge project mulai bisa digunakan ulang.
- Management melihat end-to-end operating dashboard.
- MVP siap dipakai untuk demo internal atau pilot.

Recommended sprints:

- Sprint 23: Knowledge Library Basic.
- Sprint 24: MVP Operating Dashboard.
- Sprint 25: MVP Hardening and Release.

Definition of Done:

- Template/metodologi/report reference dapat dicatat.
- Dashboard MVP menunjukkan pipeline dan delivery.
- Regression testing seluruh flow berhasil.

## 4. MVP Sprint Plan

| Sprint | Nama | Output Utama | Priority |
| --- | --- | --- | --- |
| 8A | Technical Foundation Planning | Plan migration/test/API baseline | High |
| 8B | Migration Baseline | Alembic baseline | High |
| 8C | Integration Test Baseline | Test flow Proposal -> Project -> Questionnaire | High |
| 8 | Sample Discovery | Workflow dan ADR Sample | High |
| 9 | Sample Backend | Entity/API Sample | High |
| 10 | Sample Frontend | Project Detail Sample section | High |
| 11 | Fieldwork Discovery | Workflow Fieldwork | High |
| 12 | Fieldwork Backend | Entity/API Fieldwork | High |
| 13 | Fieldwork Frontend | Fieldwork UI | High |
| 14 | Resource Basic | Enumerator/Supervisor/QC basic | High |
| 15 | Monitoring MVP | Progress and issue tracking | High |
| 16 | QC Foundation | QC summary/status | High |
| 17 | Dataset Foundation | Dataset metadata/link | High |
| 18 | Dashboard Basic | Dashboard reference | Medium |
| 19 | Report Foundation | Report metadata/link | High |
| 20 | Document Basic | Attachment metadata/link | Medium |
| 21 | Invoice Foundation | Invoice basic | High |
| 22 | Payment Tracking | Payment basic | High |
| 23 | Knowledge Library Basic | Template/methodology/report library | Medium |
| 24 | MVP Operating Dashboard | Executive overview | Medium |
| 25 | MVP Hardening | Regression, docs, release | High |

## 5. MVP Non-Goals

MVP tidak mencakup:

- Full KoBoToolbox API integration.
- XLSForm parser.
- Form builder.
- AI Report Generator penuh.
- Data warehouse.
- Advanced BI.
- Vendor performance.
- Asset lifecycle.
- Advanced finance/tax.
- Client portal.
- Mobile app enumerator.

## 6. MVP Risks

### Risk 1 - Fieldwork Scope Explosion

Mitigation:

- Buat Fieldwork MVP manual/basic.
- Integrasi KoBo ditunda.

### Risk 2 - Sample Model Salah Fondasi

Mitigation:

- Lakukan Sample Discovery sebelum coding.
- Pastikan relasi Sample dengan Questionnaire jelas.

### Risk 3 - Technical Debt Menghambat

Mitigation:

- Kerjakan migration baseline dan integration test sebelum Sample.

### Risk 4 - UI Complexity

Mitigation:

- Buat reusable table/form/detail components sebelum modul makin banyak.

### Risk 5 - Security Belum Siap Multi-user

Mitigation:

- RBAC minimal sebelum Fieldwork/Finance digunakan banyak role.

## 7. MVP Success Criteria

MVP selesai jika:

1. User dapat membuat Client.
2. User dapat membuat Proposal.
3. Proposal Approved dapat menjadi Project.
4. Project dapat memiliki banyak Questionnaire.
5. Project dapat memiliki Sample.
6. Project dapat memiliki Fieldwork Plan.
7. Progress Fieldwork dapat dipantau.
8. QC dapat dicatat.
9. Dataset dapat dicatat.
10. Report dapat dicatat.
11. Invoice dapat dibuat.
12. Payment dapat dicatat.
13. Activity penting otomatis tercatat.
14. Management dapat melihat operating overview.
15. Regression end-to-end berhasil.

## 8. Recommended Next Step

Langkah berikutnya:

```text
Sprint 8A - Technical Foundation Planning
```

Setelah itu Product Owner memilih:

1. Kerjakan Migration Baseline dulu.
2. Atau langsung Sample Discovery dengan risiko technical debt tetap terbuka.

Rekomendasi:

Kerjakan technical foundation minimal dulu, lalu lanjut Sample Discovery.
