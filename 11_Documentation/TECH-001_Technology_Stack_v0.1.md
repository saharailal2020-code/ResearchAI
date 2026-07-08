# Technology Stack

## ResearchAI Platform

**Version:** 0.1

**Status:** Draft

**Document Owner:** Beerka Research

**Date:** 8 Juli 2026

---

# 1. Tujuan Dokumen

Dokumen ini menjelaskan teknologi utama yang akan digunakan untuk membangun ResearchAI.

Technology Stack menjadi dasar untuk menyusun System Architecture, Database Schema, API Requirement, Development Setup, dan Deployment Plan.

---

# 2. Ringkasan Stack

Stack awal ResearchAI:

- Backend: Python + FastAPI
- Database: PostgreSQL
- Frontend: React
- Styling: Tailwind CSS
- AI: OpenAI API
- File Storage: Local storage pada tahap awal
- Deployment: Docker
- Version Control: Git + GitHub
- Documentation: Markdown

---

# 3. Backend

## Pilihan

Python + FastAPI

## Alasan

Python dipilih karena sangat kuat untuk aplikasi berbasis data, otomasi dokumen, integrasi AI, dan data processing.

FastAPI dipilih karena ringan, cepat, modern, dan cocok untuk membangun API ResearchAI.

## Digunakan Untuk

- Authentication
- User and role management
- Client management
- Proposal management
- Project management
- Survey management
- Quality control
- Data processing
- AI integration
- Report generator
- API service

## Prioritas

High

---

# 4. Database

## Pilihan

PostgreSQL

## Alasan

PostgreSQL dipilih karena stabil, kuat untuk data relasional, mendukung struktur data kompleks, dan cocok untuk sistem operasional seperti ResearchAI.

## Digunakan Untuk

- User data
- Client data
- Proposal data
- Project data
- Survey data
- Quality control data
- Dataset metadata
- AI output
- Report content
- Knowledge base

## Prioritas

High

---

# 5. Frontend

## Pilihan

React

## Alasan

React dipilih karena cocok untuk membangun aplikasi web interaktif, dashboard, form operasional, dan tampilan berbasis komponen.

## Digunakan Untuk

- Login page
- Dashboard
- Client pages
- Proposal pages
- Project pages
- Survey pages
- Data processing pages
- AI analysis pages
- Report editor
- User management pages

## Prioritas

High

---

# 6. Styling

## Pilihan

Tailwind CSS

## Alasan

Tailwind CSS dipilih karena mempercepat pembuatan UI yang konsisten dan mudah disesuaikan.

## Prinsip Tampilan

- Profesional
- Bersih
- Mudah dibaca
- Cocok untuk aplikasi operasional
- Fokus pada data, status, dan tindakan pengguna

## Prioritas

High

---

# 7. AI Integration

## Pilihan

OpenAI API

## Alasan

OpenAI API dipilih untuk membantu fitur AI ResearchAI seperti draft proposal, project summary, insight draft, executive summary, recommendation draft, dan report narrative.

## Digunakan Untuk

- AI proposal draft
- Project summary
- Insight generation
- Executive summary
- Recommendation draft
- Report narrative draft

## Prinsip Penggunaan

- AI bertindak sebagai assistant.
- Output AI disimpan sebagai draft.
- Output AI harus bisa direview dan diedit manusia.
- Output AI tidak otomatis menjadi final.
- Data sensitif harus diperhatikan sebelum dikirim ke layanan AI.

## Prioritas

High

---

# 8. File Storage

## Pilihan Awal

Local storage

## Alasan

Local storage cukup untuk tahap awal pengembangan dan MVP lokal.

## Digunakan Untuk

- File proposal
- Dataset upload
- File laporan
- Dokumen proyek

## Rencana Lanjutan

Pada tahap deployment yang lebih serius, file storage dapat dipindahkan ke S3-compatible storage atau layanan cloud storage lain.

## Prioritas

Medium

---

# 9. Deployment

## Pilihan

Docker

## Alasan

Docker membantu membuat environment ResearchAI lebih mudah dijalankan, dipindahkan, dan di-deploy.

## Digunakan Untuk

- Backend container
- Frontend container
- PostgreSQL container pada development
- Deployment preparation

## Prioritas

Medium

---

# 10. Version Control

## Pilihan

Git + GitHub

## Alasan

Git dan GitHub digunakan untuk menyimpan riwayat perubahan, backup online, dan kolaborasi pengembangan.

## Repository

ResearchAI sudah terhubung ke GitHub:

https://github.com/saharailal2020-code/ResearchAI

## Prioritas

High

---

# 11. Documentation

## Pilihan

Markdown

## Alasan

Markdown mudah dibaca, mudah diubah, dan cocok untuk dokumentasi yang disimpan bersama kode di Git.

## Digunakan Untuk

- Product documentation
- Business requirement
- Functional requirement
- Database documentation
- UI/UX documentation
- Technical documentation
- Decision log

## Prioritas

High

---

# 12. Stack Untuk MVP

Stack MVP yang digunakan:

| Area | Technology |
| --- | --- |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Frontend | React |
| Styling | Tailwind CSS |
| AI | OpenAI API |
| File Storage | Local storage |
| Deployment | Docker |
| Version Control | Git + GitHub |
| Documentation | Markdown |

---

# 13. Teknologi Yang Ditunda

Teknologi berikut belum menjadi prioritas awal:

- Mobile app framework
- Advanced BI tools
- Cloud object storage
- Kubernetes
- Public API gateway
- Advanced analytics engine
- Real-time websocket system

Teknologi tersebut dapat dipertimbangkan setelah MVP internal berjalan.

---

# 14. Dampak Ke Dokumen Berikutnya

Dokumen berikut harus mengacu pada technology stack ini:

- System Architecture v0.1
- Database Schema v0.1
- API Requirement v0.1
- Development Setup Guide v0.1
- Deployment Plan v0.1

---

# 15. Status

Dokumen ini masih berstatus draft dan dapat diperbarui jika ada kebutuhan teknis baru.
