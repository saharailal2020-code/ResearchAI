# Product Roadmap ResearchAI v1

Tanggal:
26 Juli 2026

Peran:
Senior Product Manager dan Solution Architect

Baseline Produk Saat Ini:

- Client Management
- Proposal Management
- Project Foundation
- Multiple Questionnaire

Tujuan Roadmap:

Menyusun arah pengembangan ResearchAI sampai MVP selesai sebagai Operating System untuk perusahaan riset.

## 1. Product Direction

ResearchAI bukan CRM biasa.

ResearchAI adalah ERP/Operating System untuk perusahaan riset yang menghubungkan:

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
  -> Dashboard
  -> Report
  -> Invoice
```

Saat ini ResearchAI sudah melewati titik penting:

```text
Proposal -> Project -> Multiple Questionnaire
```

Artinya fondasi business development sudah tersambung ke fondasi operasional riset.

Fokus MVP berikutnya adalah menyelesaikan alur operasional riset dari Questionnaire sampai Invoice dalam bentuk sederhana tetapi end-to-end.

## 2. Roadmap Principles

1. Project adalah pusat delivery.
2. Client adalah pusat relationship.
3. Questionnaire harus mendahului Sample dan Fieldwork.
4. Sample harus mendahului Fieldwork.
5. QC harus mendahului Dataset final.
6. Dataset harus mendahului Dashboard dan Report.
7. Report harus mendahului Invoice closure.
8. Activity Logging tetap menjadi cross-cutting behavior.
9. Setiap modul baru harus menambah activity otomatis yang relevan.
10. Technical foundation boleh masuk di antara sprint bisnis jika menjadi dependency penting.

## 3. Module Roadmap

### 3.1 Technical Foundation

Tujuan bisnis:

Menjaga ResearchAI tetap stabil sebelum data dan modul bertambah.

User utama:

- Engineering
- Product Owner
- System Administrator

Ketergantungan modul:

- Semua modul berikutnya bergantung pada migration, testing, API convention, dan activity consistency.

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Jika ditunda terlalu lama, schema drift dan regression makin sulit dikendalikan.
- Jika dibuat terlalu besar, bisa memperlambat product progress.

Sprint yang direkomendasikan:

- Sprint 8A: Technical Foundation Planning
- Sprint 8B: Alembic Migration Baseline
- Sprint 8C: Backend Integration Test Baseline

Catatan:

Technical Foundation sebaiknya dibuat minimal tetapi cukup kuat sebelum Sample.

### 3.2 Sample Management

Tujuan bisnis:

Mengelola target responden, kuota, segmentasi, wilayah, dan kebutuhan sampel untuk setiap Project.

User utama:

- Research Manager
- Project Manager
- Statistician
- Fieldwork Manager

Ketergantungan modul:

- Project
- Questionnaire
- Target Respondent

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Jika Sample tidak dikaitkan dengan Questionnaire/Target Respondent, project multi-questionnaire akan sulit dikelola.
- Terlalu cepat membuat sampling kompleks dapat memperbesar scope.

Sprint yang direkomendasikan:

- Sprint 8: Sample Discovery and Workflow
- Sprint 9: Sample Foundation Backend
- Sprint 10: Sample Foundation Frontend

MVP Scope:

- Sample Group.
- Target Respondent.
- Target sample size.
- Region.
- Segment.
- Quota notes.
- Status Draft/Ready.

### 3.3 Fieldwork Planning

Tujuan bisnis:

Menyiapkan rencana pelaksanaan pengumpulan data berdasarkan Project, Questionnaire, dan Sample.

User utama:

- Project Manager
- Fieldwork Manager
- Supervisor

Ketergantungan modul:

- Project
- Questionnaire Ready
- Sample Ready
- Resource basic

Prioritas:
High

Kompleksitas:
High

Risiko implementasi:

- Fieldwork adalah domain operasional yang kompleks.
- Jika Resource belum tersedia, assignment akan terlalu abstrak.
- Jika Monitoring belum siap, progress sulit dipantau.

Sprint yang direkomendasikan:

- Sprint 11: Fieldwork Discovery
- Sprint 12: Fieldwork Plan Backend
- Sprint 13: Fieldwork Plan Frontend

MVP Scope:

- Fieldwork Plan.
- Fieldwork status.
- Start/end date optional.
- Target sample summary.
- Channel atau method.
- Basic assignment placeholder.

### 3.4 Resource Management Basic

Tujuan bisnis:

Mencatat resource operasional yang menjalankan fieldwork dan QC.

User utama:

- Fieldwork Manager
- Project Manager
- Operations
- QC Coordinator

Ketergantungan modul:

- Fieldwork Planning
- User/Role basic

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Resource dapat berkembang menjadi modul besar jika mencakup payroll, availability, performance, dan assignment detail.

Sprint yang direkomendasikan:

- Sprint 14: Resource Basic

MVP Scope:

- Enumerator.
- Supervisor.
- QC Staff.
- Region.
- Skill.
- Status active/inactive.
- Assignment ke Project atau Fieldwork secara sederhana.

### 3.5 Fieldwork Monitoring

Tujuan bisnis:

Memantau progress pengumpulan data, capaian sampel, masalah lapangan, dan status pelaksanaan.

User utama:

- Project Manager
- Fieldwork Manager
- Supervisor
- Management

Ketergantungan modul:

- Fieldwork Plan
- Sample
- Resource Basic

Prioritas:
High

Kompleksitas:
High

Risiko implementasi:

- Jika data lapangan belum terintegrasi dari KoBo, monitoring awal harus manual.
- Progress metric harus sederhana dulu agar tidak menjadi BI dashboard terlalu cepat.

Sprint yang direkomendasikan:

- Sprint 15: Monitoring MVP

MVP Scope:

- Target sample.
- Completed sample.
- Completion rate.
- Issue log.
- Status per target respondent.
- Manual progress update.

### 3.6 QC Management

Tujuan bisnis:

Menjamin kualitas data sebelum masuk Dataset final.

User utama:

- QC Team
- Data Processing
- Project Manager
- Research Manager

Ketergantungan modul:

- Fieldwork
- Monitoring
- Resource QC

Prioritas:
High

Kompleksitas:
High

Risiko implementasi:

- QC bisa menjadi sangat kompleks jika mencakup backcheck, fraud detection, audio validation, GPS, dan logic validation.
- MVP harus tetap manual/basic.

Sprint yang direkomendasikan:

- Sprint 16: QC Foundation

MVP Scope:

- QC batch.
- QC status.
- Checked count.
- Valid count.
- Rejected count.
- QC notes.
- Dataset readiness flag.

### 3.7 Dataset Management

Tujuan bisnis:

Menyimpan dan mengelola data hasil fieldwork yang sudah melalui QC.

User utama:

- Data Processing
- Data Analyst
- Research Manager
- Project Manager

Ketergantungan modul:

- QC
- Fieldwork
- Questionnaire

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Dataset bisa menjadi berat jika langsung mengelola file besar, variable dictionary, dan data cleaning kompleks.
- MVP cukup metadata dan link/file reference.

Sprint yang direkomendasikan:

- Sprint 17: Dataset Foundation

MVP Scope:

- Dataset name.
- Source.
- File/link reference.
- Status Draft/Ready.
- Record count.
- Last updated.
- Notes.

### 3.8 Dashboard Basic

Tujuan bisnis:

Memberikan ringkasan hasil atau progress riset dalam bentuk visual sederhana.

User utama:

- Management
- Research Manager
- Data Analyst
- Project Manager
- Client-facing team

Ketergantungan modul:

- Dataset Ready
- Monitoring

Prioritas:
Medium

Kompleksitas:
Medium

Risiko implementasi:

- Dashboard dapat melebar menjadi BI platform.
- MVP harus fokus pada metadata/dashboard link atau embedded summary.

Sprint yang direkomendasikan:

- Sprint 18: Dashboard Basic

MVP Scope:

- Dashboard title.
- Dashboard link.
- Dataset reference.
- Status.
- Key metric summary.

### 3.9 Report Management

Tujuan bisnis:

Mengelola laporan hasil riset sebagai deliverable utama ke client.

User utama:

- Research Manager
- Report Writer
- Data Analyst
- Research Director
- Project Manager

Ketergantungan modul:

- Dataset
- Dashboard
- Project
- Client

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Report Generator AI dan template bisa memperbesar scope.
- MVP cukup report metadata, file/link, status, dan delivery tracking.

Sprint yang direkomendasikan:

- Sprint 19: Report Foundation

MVP Scope:

- Report title.
- Report type.
- Report file/link.
- Status Draft/Final/Sent.
- Delivery date.
- Notes.

### 3.10 Document Management Basic

Tujuan bisnis:

Menyediakan attachment lintas domain agar dokumen penting tidak tercecer.

User utama:

- Semua user operasional
- Administration
- Project Manager
- Finance

Ketergantungan modul:

- Client
- Proposal
- Project
- Questionnaire
- Report
- Invoice

Prioritas:
Medium

Kompleksitas:
Medium

Risiko implementasi:

- File storage dan permission bisa kompleks.
- MVP bisa dimulai dengan metadata/link reference.

Sprint yang direkomendasikan:

- Sprint 20: Document Basic

MVP Scope:

- Document title.
- Source domain.
- Source ID.
- File/link reference.
- Document type.
- Uploaded by.
- Created date.

### 3.11 Invoice Management

Tujuan bisnis:

Menghubungkan project delivery ke tagihan client.

User utama:

- Finance
- Business Development
- Project Manager
- Management

Ketergantungan modul:

- Client
- Project
- Proposal value
- Report or delivery status

Prioritas:
High

Kompleksitas:
Medium

Risiko implementasi:

- Invoice bisa kompleks jika mencakup tax, payment terms, multi-stage billing, dan contract.
- MVP cukup invoice sederhana.

Sprint yang direkomendasikan:

- Sprint 21: Invoice Foundation

MVP Scope:

- Invoice number.
- Client.
- Project.
- Invoice date.
- Due date.
- Amount.
- Status Draft/Sent/Paid/Overdue.
- Notes.

### 3.12 Payment Tracking

Tujuan bisnis:

Menutup siklus bisnis dari invoice ke pembayaran.

User utama:

- Finance
- Management
- Business Development

Ketergantungan modul:

- Invoice
- Client

Prioritas:
High

Kompleksitas:
Low to Medium

Risiko implementasi:

- Payment matching dan partial payment bisa kompleks.
- MVP cukup satu atau beberapa payment per invoice.

Sprint yang direkomendasikan:

- Sprint 22: Payment Tracking

MVP Scope:

- Payment date.
- Amount paid.
- Payment method.
- Reference number.
- Invoice status update.

### 3.13 Knowledge Management Basic

Tujuan bisnis:

Membuat pengetahuan project dapat digunakan ulang untuk proposal, questionnaire, metodologi, dan report.

User utama:

- Research Manager
- Business Development
- Report Writer
- Research Director

Ketergantungan modul:

- Proposal
- Questionnaire
- Report
- Project

Prioritas:
Medium

Kompleksitas:
Medium

Risiko implementasi:

- Knowledge Management bisa melebar ke AI Knowledge Base terlalu cepat.
- MVP cukup template/reference library sederhana.

Sprint yang direkomendasikan:

- Sprint 23: Knowledge Library Basic

MVP Scope:

- Template Library.
- Methodology Library.
- Questionnaire Library metadata.
- Report Library metadata.

### 3.14 MVP Dashboard / Operating Overview

Tujuan bisnis:

Memberikan tampilan manajemen untuk melihat kesehatan bisnis dan project.

User utama:

- Management
- Research Director
- Project Manager
- Business Development
- Finance

Ketergantungan modul:

- Proposal
- Project
- Questionnaire
- Sample
- Fieldwork
- Report
- Invoice

Prioritas:
Medium

Kompleksitas:
Medium

Risiko implementasi:

- Dashboard bisa menjadi terlalu luas.
- MVP cukup KPI ringkas.

Sprint yang direkomendasikan:

- Sprint 24: MVP Operating Dashboard

MVP Scope:

- Active projects.
- Proposal pipeline.
- Fieldwork progress.
- Reports due.
- Invoice unpaid.
- Revenue summary.

## 4. Priority Matrix

| Priority | Module |
| --- | --- |
| High | Technical Foundation |
| High | Sample Management |
| High | Fieldwork Planning |
| High | Resource Management Basic |
| High | Fieldwork Monitoring |
| High | QC Management |
| High | Dataset Management |
| High | Report Management |
| High | Invoice Management |
| High | Payment Tracking |
| Medium | Dashboard Basic |
| Medium | Document Management Basic |
| Medium | Knowledge Management Basic |
| Medium | MVP Operating Dashboard |

## 5. Complexity Matrix

| Complexity | Module |
| --- | --- |
| High | Fieldwork Planning |
| High | Fieldwork Monitoring |
| High | QC Management |
| Medium | Technical Foundation |
| Medium | Sample Management |
| Medium | Resource Management Basic |
| Medium | Dataset Management |
| Medium | Dashboard Basic |
| Medium | Report Management |
| Medium | Document Management Basic |
| Medium | Invoice Management |
| Medium | Knowledge Management Basic |
| Low-Medium | Payment Tracking |

## 6. Recommended Sprint Sequence

```text
Sprint 8A  - Technical Foundation Planning
Sprint 8B  - Migration Baseline
Sprint 8C  - Integration Test Baseline
Sprint 8   - Sample Discovery
Sprint 9   - Sample Backend
Sprint 10  - Sample Frontend
Sprint 11  - Fieldwork Discovery
Sprint 12  - Fieldwork Backend
Sprint 13  - Fieldwork Frontend
Sprint 14  - Resource Basic
Sprint 15  - Monitoring MVP
Sprint 16  - QC Foundation
Sprint 17  - Dataset Foundation
Sprint 18  - Dashboard Basic
Sprint 19  - Report Foundation
Sprint 20  - Document Basic
Sprint 21  - Invoice Foundation
Sprint 22  - Payment Tracking
Sprint 23  - Knowledge Library Basic
Sprint 24  - MVP Operating Dashboard
Sprint 25  - MVP Hardening and Release
```

## 7. MVP Completion Definition

ResearchAI MVP dianggap selesai jika user dapat menjalankan flow:

```text
Client
  -> Proposal
  -> Project
  -> Multiple Questionnaire
  -> Sample
  -> Fieldwork
  -> Monitoring
  -> QC
  -> Dataset
  -> Dashboard/Report
  -> Invoice
  -> Payment
```

Minimum success criteria:

- Setiap domain utama memiliki list/detail/create minimum.
- Setiap domain utama punya status lifecycle sederhana.
- Activity penting tercatat otomatis.
- Project Detail menjadi pusat operasional.
- Client Detail menjadi pusat relationship.
- Management dapat melihat overview MVP.
- Data dapat dilacak dari Client sampai Payment.

## 8. Product Recommendation

Rekomendasi Product Manager:

Jangan langsung masuk Fieldwork.

Langkah paling tepat setelah Sprint 7 adalah:

```text
Technical Foundation ringan
  -> Sample Discovery
  -> Sample Foundation
  -> Fieldwork Discovery
```

Alasannya:

- Multiple Questionnaire telah membuat Project lebih realistis.
- Sample adalah jembatan wajib antara Questionnaire dan Fieldwork.
- Tanpa Sample, Fieldwork akan kehilangan struktur target respondent, quota, dan progress.
