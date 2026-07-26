# MVP Module Dependency

Status:
Proposed for Domain Architecture Freeze

Tanggal:
26 Juli 2026

## Tujuan

Menentukan urutan pembangunan modul MVP ResearchAI berdasarkan dependency domain agar sprint berikutnya tidak melompat terlalu jauh dan tidak membuat modul yang belum punya fondasi.

## Prinsip Urutan Pembangunan

1. Bangun modul upstream sebelum downstream.
2. Modul yang menjadi parent harus stabil sebelum child module dibangun.
3. Activity logging ikut dalam setiap modul bisnis.
4. Jangan membuat AI sebelum data, document, dan knowledge cukup tersedia.
5. Jangan membuat Invoice final sebelum Project dan nilai pekerjaan jelas.

## Dependency Map

```text
Authentication
   |
   v
Client Management
   |
   v
Proposal Management
   |
   v
Project Management
   |
   +-- Questionnaire
   |
   +-- Sample
   |
   +-- Fieldwork
   |
   +-- QC
   |
   v
Dataset
   |
   +-- Dashboard
   |
   v
Report
   |
   v
Invoice
```

## Modul Prerequisite

### Authentication

Prerequisite untuk:

- semua modul internal
- activity created_by
- ownership Proposal dan Project

Status:
Sudah selesai basic.

### Client Management

Prerequisite untuk:

- Proposal
- Project
- Invoice
- Activity Timeline

Status:
Sudah selesai untuk MVP awal.

### Proposal Management

Prerequisite untuk:

- Project Setup
- Project Management MVP

Status:
Sedang berjalan. List, Detail, dan Status Actions selesai. Create/Edit frontend belum selesai.

### Project Management

Prerequisite untuk:

- Questionnaire
- Sample
- Fieldwork
- QC
- Dataset
- Dashboard
- Report
- Invoice

Status:
Belum dimulai.

## Modul Dependent

### Questionnaire

Depends on:

- Project

Dependent modules:

- Fieldwork
- QC
- Dataset

### Sample

Depends on:

- Project

Dependent modules:

- Fieldwork
- Monitoring
- QC

### Fieldwork

Depends on:

- Project
- Questionnaire
- Sample

Dependent modules:

- QC
- Dataset
- Monitoring

### QC

Depends on:

- Project
- Fieldwork data

Dependent modules:

- Dataset
- Analysis

### Dataset

Depends on:

- Project
- QC output

Dependent modules:

- Dashboard
- Report
- AI Insight Generator

### Dashboard

Depends on:

- Dataset

Dependent modules:

- Report
- Client delivery

### Report

Depends on:

- Project
- Dataset
- Dashboard

Dependent modules:

- Invoice
- Knowledge Repository
- AI Report Generator

### Invoice

Depends on:

- Client
- Project or Contract

Dependent modules:

- Payment
- Finance summary

## Modul yang Bisa Paralel

### Bisa Paralel Setelah Client Management

- Proposal Frontend
- Client 360 refinement
- Activity UI refinement

### Bisa Paralel Setelah Proposal Management Stabil

- Project Design Review
- Document Management Discovery
- Template Library Discovery

### Bisa Paralel Setelah Project Basic

- Questionnaire basic
- Sample basic
- Project activity refinement
- Project document attachment design

### Bisa Paralel Setelah Fieldwork Basic

- QC basic
- Monitoring basic
- Resource Management basic

### Bisa Paralel Setelah Dataset Basic

- Dashboard basic
- Report basic
- AI Insight discovery

## Rekomendasi Urutan MVP

### Step 1

Selesaikan Proposal Management:

- Create Proposal
- Edit Proposal
- Proposal Timeline
- Activity refinement

### Step 2

Project Management Design:

- Project domain design
- Project lifecycle freeze
- Project schema planning
- Project UI wireframe

### Step 3

Project Management Basic:

- Project backend
- Project frontend
- Setup Project dari Proposal Approved
- Project status actions
- Project activity logging

### Step 4

Research Operation Foundation:

- Questionnaire basic
- Sample basic
- Fieldwork basic
- QC basic

### Step 5

Data and Delivery Foundation:

- Dataset basic
- Dashboard basic
- Report basic

### Step 6

Finance Foundation:

- Invoice basic
- Payment basic

### Step 7

Knowledge and AI Foundation:

- Template Library
- Methodology Library
- Research Repository
- AI Assistant
- Insight Generator

## Modules to Delay

Tunda sampai fondasi utama stabil:

- Lead
- Opportunity
- Quotation
- Contract
- Vendor Management
- Asset Management
- Advanced Role Permission
- Notification
- Calendar
- Task
- AI full automation

Alasan:

Modul-modul tersebut penting, tetapi belum menjadi blocker untuk membuktikan alur MVP:

```text
Client -> Proposal -> Project -> Fieldwork -> Dataset -> Report -> Invoice
```

## Architecture Gate Before Sprint 5

Sebelum Sprint 5, Product Owner perlu mengonfirmasi:

- Proposal Create tetap menjadi prioritas Sprint 5.
- Project Management belum dimulai sebelum Proposal Create/Edit selesai.
- Domain Freeze Proposal vs Project disetujui.
- Project lifecycle MVP disetujui atau perlu revisi.
