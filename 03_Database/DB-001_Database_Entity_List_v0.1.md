# Database Entity List

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan daftar entitas database awal yang dibutuhkan ResearchAI pada tahap MVP.

Database Entity List menjadi dasar untuk menyusun Entity Relationship Diagram (ERD), database schema, migration, API design, dan backend model.

---

# 2. Prinsip Desain Database

Prinsip awal database ResearchAI:

1. Setiap data utama harus memiliki identifier unik.
2. Data antar modul harus saling terhubung.
3. Data penting harus memiliki informasi pembuat dan waktu perubahan.
4. Hak akses harus dapat dikembangkan berbasis role.
5. Output AI harus dibedakan dari hasil final yang sudah direview manusia.
6. Struktur database harus modular agar mudah dikembangkan bertahap.

---

# 3. Kategori Entitas

Entitas database ResearchAI dibagi menjadi beberapa kategori:

- User and Access
- Client and Contact
- Proposal
- Project
- Survey and Fieldwork
- Quality Control
- Data Processing
- AI Analysis
- Report Generator
- Knowledge Base
- Dashboard and Activity
- File and Document

---

# 4. Core Entities MVP

## 4.1 users

Fungsi:

Menyimpan data pengguna ResearchAI.

Contoh field:

- id
- full_name
- email
- password_hash
- status
- last_login_at
- created_at
- updated_at

Relasi:

- users memiliki banyak user_roles
- users dapat membuat proposal, project note, dataset, report, dan AI output

Prioritas:

High

---

## 4.2 roles

Fungsi:

Menyimpan daftar role pengguna.

Contoh field:

- id
- role_name
- description
- status
- created_at
- updated_at

Contoh role:

- System Administrator
- Research Director
- Research Manager
- Project Manager
- Marketing
- Data Processing
- Data Analyst
- Quality Control
- Supervisor
- Enumerator
- Finance
- Client

Relasi:

- roles memiliki banyak user_roles
- roles dapat dihubungkan dengan permissions pada tahap lanjutan

Prioritas:

High

---

## 4.3 user_roles

Fungsi:

Menghubungkan pengguna dengan role.

Contoh field:

- id
- user_id
- role_id
- created_at

Relasi:

- user_roles menghubungkan users dan roles

Prioritas:

High

---

## 4.4 clients

Fungsi:

Menyimpan data klien.

Contoh field:

- id
- client_name
- industry
- client_type
- status
- notes
- created_by
- created_at
- updated_at

Relasi:

- clients memiliki banyak client_contacts
- clients memiliki banyak proposals
- clients memiliki banyak projects

Prioritas:

High

---

## 4.5 client_contacts

Fungsi:

Menyimpan kontak klien.

Contoh field:

- id
- client_id
- contact_name
- position
- email
- phone
- is_primary
- notes
- created_at
- updated_at

Relasi:

- client_contacts milik clients

Prioritas:

High

---

## 4.6 proposals

Fungsi:

Menyimpan data proposal riset.

Contoh field:

- id
- client_id
- proposal_title
- research_type
- research_objective
- methodology_summary
- estimated_timeline
- estimated_budget
- status
- created_by
- approved_at
- created_at
- updated_at

Status awal:

- Draft
- Sent
- Revised
- Approved
- Rejected

Relasi:

- proposals milik clients
- proposals dapat memiliki proposal_files
- proposals dapat menjadi projects
- proposals dapat memiliki AI output

Prioritas:

High

---

## 4.7 proposal_files

Fungsi:

Menyimpan metadata file proposal.

Contoh field:

- id
- proposal_id
- file_id
- file_type
- uploaded_by
- created_at

Relasi:

- proposal_files milik proposals
- proposal_files mengarah ke files

Prioritas:

Medium

---

## 4.8 projects

Fungsi:

Menyimpan data proyek riset.

Contoh field:

- id
- client_id
- proposal_id
- project_name
- project_code
- research_type
- project_manager_id
- start_date
- end_date
- status
- created_by
- created_at
- updated_at

Status awal:

- Project Active
- Research Design
- Fieldwork
- Quality Control
- Data Processing
- Analysis
- Report Draft
- Report Final
- Delivered
- Closed

Relasi:

- projects milik clients
- projects dapat berasal dari proposals
- projects memiliki project_members
- projects memiliki survey_plans
- projects memiliki datasets
- projects memiliki reports
- projects memiliki knowledge_items

Prioritas:

High

---

## 4.9 project_members

Fungsi:

Menyimpan anggota tim proyek.

Contoh field:

- id
- project_id
- user_id
- project_role
- assigned_at
- assigned_by

Relasi:

- project_members menghubungkan projects dan users

Prioritas:

High

---

## 4.10 project_milestones

Fungsi:

Menyimpan milestone proyek.

Contoh field:

- id
- project_id
- milestone_name
- description
- due_date
- status
- completed_at
- created_at
- updated_at

Relasi:

- project_milestones milik projects

Prioritas:

Medium

---

## 4.11 project_notes

Fungsi:

Menyimpan catatan progress proyek.

Contoh field:

- id
- project_id
- note
- note_type
- created_by
- created_at

Relasi:

- project_notes milik projects
- project_notes dibuat oleh users

Prioritas:

Medium

---

# 5. Survey and Fieldwork Entities

## 5.1 survey_plans

Fungsi:

Menyimpan informasi rencana survei per proyek.

Contoh field:

- id
- project_id
- survey_method
- target_respondent
- sample_size
- area
- start_date
- end_date
- status
- created_at
- updated_at

Relasi:

- survey_plans milik projects
- survey_plans memiliki fieldwork_progress

Prioritas:

Medium

---

## 5.2 fieldwork_progress

Fungsi:

Menyimpan progress pelaksanaan fieldwork.

Contoh field:

- id
- survey_plan_id
- progress_date
- completed_sample
- target_sample
- issue_notes
- reported_by
- created_at

Relasi:

- fieldwork_progress milik survey_plans
- fieldwork_progress dibuat oleh users

Prioritas:

Medium

---

# 6. Quality Control Entities

## 6.1 quality_checks

Fungsi:

Menyimpan hasil quality control.

Contoh field:

- id
- project_id
- dataset_id
- checked_by
- total_checked
- valid_count
- invalid_count
- status
- notes
- checked_at
- created_at

Relasi:

- quality_checks milik projects
- quality_checks dapat terhubung ke datasets
- quality_checks dibuat oleh users

Prioritas:

High

---

## 6.2 quality_check_items

Fungsi:

Menyimpan detail item atau masalah QC.

Contoh field:

- id
- quality_check_id
- issue_type
- issue_description
- severity
- status
- created_at
- updated_at

Relasi:

- quality_check_items milik quality_checks

Prioritas:

Medium

---

# 7. Data Processing Entities

## 7.1 datasets

Fungsi:

Menyimpan metadata dataset proyek.

Contoh field:

- id
- project_id
- dataset_name
- file_id
- dataset_type
- status
- uploaded_by
- uploaded_at
- created_at
- updated_at

Status awal:

- Uploaded
- Cleaning
- Validated
- Ready for Analysis

Relasi:

- datasets milik projects
- datasets mengarah ke files
- datasets memiliki data_processing_notes
- datasets dapat digunakan oleh AI analysis dan reports

Prioritas:

High

---

## 7.2 data_processing_notes

Fungsi:

Menyimpan catatan proses data cleaning dan data processing.

Contoh field:

- id
- dataset_id
- note
- created_by
- created_at

Relasi:

- data_processing_notes milik datasets
- data_processing_notes dibuat oleh users

Prioritas:

Medium

---

# 8. AI Analysis Entities

## 8.1 ai_outputs

Fungsi:

Menyimpan output yang dibuat dengan bantuan AI.

Contoh field:

- id
- project_id
- source_type
- source_id
- output_type
- prompt_summary
- output_content
- status
- generated_by
- reviewed_by
- reviewed_at
- created_at
- updated_at

Output type:

- Proposal Draft
- Project Summary
- Insight Draft
- Executive Summary Draft
- Recommendation Draft
- Report Narrative Draft

Status:

- Draft
- Reviewed
- Approved
- Rejected

Relasi:

- ai_outputs milik projects
- ai_outputs dapat terhubung ke proposals, datasets, atau reports
- ai_outputs dibuat oleh users
- ai_outputs direview oleh users

Prioritas:

High

---

# 9. Report Generator Entities

## 9.1 reports

Fungsi:

Menyimpan data laporan proyek.

Contoh field:

- id
- project_id
- report_title
- report_type
- status
- created_by
- reviewed_by
- finalized_at
- created_at
- updated_at

Status:

- Draft
- Review
- Revised
- Final
- Delivered

Relasi:

- reports milik projects
- reports memiliki report_sections
- reports dapat memiliki report_files

Prioritas:

High

---

## 9.2 report_sections

Fungsi:

Menyimpan bagian atau konten laporan.

Contoh field:

- id
- report_id
- section_title
- section_order
- content
- ai_output_id
- created_at
- updated_at

Relasi:

- report_sections milik reports
- report_sections dapat dibuat dari ai_outputs

Prioritas:

High

---

## 9.3 report_files

Fungsi:

Menyimpan metadata file laporan.

Contoh field:

- id
- report_id
- file_id
- file_type
- uploaded_by
- created_at

Relasi:

- report_files milik reports
- report_files mengarah ke files

Prioritas:

Medium

---

# 10. Knowledge Base Entities

## 10.1 knowledge_items

Fungsi:

Menyimpan knowledge yang dihasilkan dari proyek.

Contoh field:

- id
- project_id
- client_id
- title
- category
- content
- tags
- source_type
- source_id
- created_by
- created_at
- updated_at

Kategori awal:

- Insight
- Recommendation
- Methodology
- Template
- Lesson Learned
- Benchmark

Relasi:

- knowledge_items dapat terhubung ke projects
- knowledge_items dapat terhubung ke clients
- knowledge_items dibuat oleh users

Prioritas:

Medium

---

# 11. File and Document Entities

## 11.1 files

Fungsi:

Menyimpan metadata file yang diunggah ke ResearchAI.

Contoh field:

- id
- file_name
- file_path
- file_type
- file_size
- module_name
- uploaded_by
- uploaded_at
- created_at

Relasi:

- files dapat digunakan oleh proposal_files
- files dapat digunakan oleh datasets
- files dapat digunakan oleh report_files

Prioritas:

High

---

# 12. Activity and Audit Entities

## 12.1 activity_logs

Fungsi:

Menyimpan aktivitas penting pengguna.

Contoh field:

- id
- user_id
- activity_type
- module_name
- entity_name
- entity_id
- description
- created_at

Relasi:

- activity_logs dibuat oleh users
- activity_logs dapat mengarah ke entitas tertentu

Prioritas:

Medium

---

# 13. Relasi Utama

Relasi utama database ResearchAI:

- clients -> client_contacts
- clients -> proposals
- clients -> projects
- proposals -> projects
- projects -> project_members
- projects -> project_milestones
- projects -> project_notes
- projects -> survey_plans
- survey_plans -> fieldwork_progress
- projects -> quality_checks
- projects -> datasets
- datasets -> data_processing_notes
- projects -> ai_outputs
- projects -> reports
- reports -> report_sections
- projects -> knowledge_items
- users -> user_roles
- roles -> user_roles
- files -> proposal_files
- files -> datasets
- files -> report_files

---

# 14. Entitas Prioritas MVP

Entitas yang wajib ada untuk MVP awal:

- users
- roles
- user_roles
- clients
- client_contacts
- proposals
- projects
- project_members
- survey_plans
- quality_checks
- datasets
- ai_outputs
- reports
- report_sections
- files

Entitas yang dapat dibuat setelah MVP awal:

- project_milestones
- project_notes
- fieldwork_progress
- quality_check_items
- data_processing_notes
- report_files
- knowledge_items
- activity_logs

---

# 15. Catatan Untuk ERD

Dokumen ini belum menjadi ERD final.

Langkah berikutnya:

1. Menentukan primary key dan foreign key.
2. Menentukan tipe data setiap field.
3. Menentukan constraint dan index.
4. Menentukan soft delete atau hard delete.
5. Membuat ERD v0.1.
6. Membuat database schema v0.1.

---

# 16. Status

Dokumen ini masih berstatus draft dan akan diperbarui setelah UI/UX User Flow dan API Requirement dibuat.
