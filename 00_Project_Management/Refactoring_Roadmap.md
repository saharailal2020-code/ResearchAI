# Refactoring Roadmap

Tanggal:
26 Juli 2026

Scope:
ResearchAI setelah Proposal, Project, dan Multiple Questionnaire

Tujuan:
Menjaga ResearchAI tetap scalable, maintainable, dan siap berkembang menjadi ERP/Operating System perusahaan riset.

## Guiding Principles

1. Refactor bertahap, tidak big bang.
2. Tidak memecah fitur yang sudah berjalan.
3. Refactor dilakukan setelah ada acceptance criteria dan regression test.
4. Modul bisnis tetap mengikuti Design Review sebelum implementation.
5. Technical foundation diprioritaskan jika modul berikutnya akan menambah kompleksitas besar.

## Roadmap Overview

```text
Phase R0 - Stabilize Baseline
Phase R1 - Database Migration Foundation
Phase R2 - API and Workflow Consistency
Phase R3 - Shared Activity/Event Service
Phase R4 - Frontend Modularization
Phase R5 - Security and Permission Foundation
Phase R6 - Testing Foundation
Phase R7 - Prepare Sample and Fieldwork Architecture
```

## Phase R0 - Stabilize Baseline

Timing:
Before Sprint 8

Goal:
Rapikan baseline dokumen dan repository agar sprint berikutnya tidak tercampur.

Tasks:

- Buat Architecture Baseline Index.
- Tentukan dokumen authoritative terbaru.
- Review file untracked lama.
- Putuskan dokumen mana yang perlu commit terpisah.
- Pastikan `.gitignore` menjaga temporary artifacts.

Deliverables:

- `Architecture_Baseline_Index.md`
- Clean documentation staging policy.

Risk:

- Tanpa baseline, tim bisa memakai dokumen lama.

Priority:
Medium

## Phase R1 - Database Migration Foundation

Timing:
Before adding Sample tables if possible

Goal:
Mengganti script upgrade manual menjadi migration formal.

Tasks:

- Install/configure Alembic.
- Buat baseline migration dari schema saat ini.
- Migrasikan script upgrade existing ke migration history.
- Tambahkan rollback pattern.
- Tambahkan seed data convention.
- Dokumentasikan migration workflow untuk local development.

Deliverables:

- Alembic configured.
- Baseline migration.
- Migration guide.

Risk:

- Harus hati-hati agar database lokal yang sudah ada tidak rusak.

Priority:
High

## Phase R2 - API and Workflow Consistency

Timing:
Before Fieldwork status/actions

Goal:
Membuat pola API dan workflow action yang konsisten.

Tasks:

- Buat `API_Convention_v1.md`.
- Tetapkan policy endpoint action.
- Tetapkan policy deprecated endpoint.
- Standarkan error response.
- Tambahkan pagination contract.
- Buat shared workflow transition helper.

Candidate Future Convention:

```text
POST /resources/{id}/actions/{action_name}
```

Examples:

```text
POST /proposals/{id}/actions/send-to-client
POST /proposals/{id}/actions/approve
POST /projects/{id}/actions/mark-ready
POST /questionnaires/{id}/actions/mark-ready
```

Deliverables:

- API convention.
- Workflow helper.
- Deprecated endpoint policy.

Risk:

- Perlu backward compatibility agar frontend lama tidak rusak.

Priority:
High

## Phase R3 - Shared Activity/Event Service

Timing:
Before Sample or Fieldwork produces many events

Goal:
Mencegah duplikasi activity logging dan menyiapkan timeline lintas domain.

Tasks:

- Buat shared activity service.
- Standarkan event naming.
- Standarkan event payload.
- Pisahkan konsep source module dan source id.
- Evaluasi apakah `ClientActivity` perlu diperluas menjadi `DomainActivity`.

Current Pattern:

```text
Proposal service -> ClientActivity
Project service -> ClientActivity
Questionnaire service -> ClientActivity
```

Target Pattern:

```text
Business Service -> Activity Service -> Timeline Views
```

Deliverables:

- Activity service.
- Activity naming convention.
- Timeline query policy.

Risk:

- Refactor activity harus menjaga data lama tetap terbaca.

Priority:
High

## Phase R4 - Frontend Modularization

Timing:
After Questionnaire, before UI grows too large

Goal:
Mengurangi page complexity dan menyiapkan frontend untuk modul Sample/Fieldwork.

Tasks:

- Buat module folders:

```text
src/modules/clients
src/modules/proposals
src/modules/projects
src/modules/questionnaires
```

- Extract section components dari page besar.
- Buat shared DataTable.
- Buat shared Breadcrumb.
- Buat shared PageHeader.
- Buat shared StatusActionPanel.
- Buat shared FormSection.
- Buat shared EmptyState/LoadingState variants.

Deliverables:

- Modular frontend structure.
- Reduced page file size.
- Reusable operational UI components.

Risk:

- Refactor frontend tanpa test bisa menyebabkan regression.

Priority:
Medium

## Phase R5 - Security and Permission Foundation

Timing:
Before multi-user operational usage

Goal:
Membuat ResearchAI aman untuk role berbeda.

Tasks:

- Definisikan permission matrix.
- Implement role-based authorization dependency.
- Implement object-level access rule.
- Review JWT storage strategy.
- Enforce production secret key from environment.
- Tambahkan CORS/security headers policy.

Candidate Permissions:

```text
proposal:create
proposal:update
proposal:approve
project:setup
project:update_status
questionnaire:create
questionnaire:update
questionnaire:mark_ready
```

Deliverables:

- Permission matrix.
- Authorization helper.
- Security configuration checklist.

Risk:

- Permission terlalu kompleks bisa menghambat MVP jika dibuat terlalu awal.

Priority:
High before production, Medium before local MVP demos.

## Phase R6 - Testing Foundation

Timing:
Before heavy refactoring

Goal:
Memberi safety net agar refactoring aman.

Tasks:

- Tambahkan backend integration tests.
- Tambahkan test database setup.
- Tambahkan API flow tests.
- Tambahkan frontend smoke tests.
- Tambahkan lint/build/test checklist ke sprint closing.

Minimum Backend Test Flow:

```text
Create Client
Create Proposal
Approve Proposal
Setup Project
Create two Questionnaires
Mark one Ready
Verify activity logs
```

Deliverables:

- Backend test suite.
- Frontend smoke test.
- Testing guide.

Risk:

- Test setup butuh waktu, tetapi akan menghemat waktu sprint berikutnya.

Priority:
High

## Phase R7 - Prepare Sample and Fieldwork Architecture

Timing:
Before Sample implementation

Goal:
Memastikan modul berikutnya tidak salah fondasi.

Tasks:

- Discovery Sample.
- Tentukan hubungan Sample dengan Questionnaire.
- Tentukan apakah Sample dibuat per Target Respondent.
- Tentukan readiness rule dari Questionnaire ke Sample/Fieldwork.
- Tentukan Fieldwork actor: Enumerator, Supervisor, QC.
- Tentukan apakah Resource Management harus dimulai sebelum Fieldwork.

Key Question:

```text
Apakah setiap Questionnaire memiliki Sample sendiri?
```

Likely Direction:

```text
Project
  -> Questionnaire
        -> Sample Group
              -> Fieldwork Assignment
```

Deliverables:

- Sample Discovery.
- ADR Questionnaire to Sample.
- Sprint Plan Sample Foundation.

Risk:

- Jika Sample langsung dibuat di level Project tanpa mempertimbangkan Questionnaire, project multi-target bisa sulit dikelola.

Priority:
High before Sprint Sample.

## Recommended Sequence

### Option A - Product-first but safe

1. R0 Baseline docs.
2. R7 Sample Discovery.
3. Sprint Sample Foundation.
4. R1 Migration Framework.
5. R3 Activity Service.

Suitable if:

- User ingin lanjut cepat ke fitur riset.

Risk:

- Technical debt migration tetap tertunda.

### Option B - Architecture-first

1. R0 Baseline docs.
2. R1 Migration Framework.
3. R6 Backend integration tests.
4. R3 Activity Service.
5. R7 Sample Discovery.

Suitable if:

- ResearchAI akan mulai dijalankan lebih serius dengan data yang perlu dipertahankan.

Recommendation:

Gunakan Option B ringan:

```text
R0 -> R1 minimal -> R6 minimal -> R7
```

Artinya:

- Tidak perlu refactor besar.
- Cukup migration baseline dan test flow utama sebelum Sample.

## Refactoring Guardrails

Jangan lakukan:

- Big bang folder restructure.
- Mengubah endpoint aktif tanpa compatibility.
- Mengubah workflow bisnis tanpa Product Owner Review.
- Menghapus deprecated endpoint sebelum frontend dan docs siap.
- Refactor UI besar tanpa screenshot regression.

Wajib lakukan:

- Product Owner approval.
- Regression testing.
- Commit per phase.
- Dokumentasi keputusan.

## Final Recommendation

Sebelum Sprint 8, lakukan satu mini-sprint:

Nama:
Technical Foundation Planning

Output:

- Architecture Baseline Index.
- Migration Framework Plan.
- Testing Baseline Plan.
- Sample Discovery Questions.

Setelah itu, Product Owner dapat memilih:

1. Langsung Sample Discovery.
2. Atau implement Alembic baseline terlebih dahulu.
