# Architecture Review v1

Tanggal:
26 Juli 2026

Scope Review:

- Proposal
- Project
- Multiple Questionnaire
- Client Activity Timeline sebagai cross-cutting behavior

Status:
Architecture Review sebelum Sprint 8

## 1. Executive Summary

ResearchAI saat ini sudah memiliki fondasi MVP yang baik untuk bergerak dari Business Development menuju Research Preparation.

Alur utama sudah terbentuk:

```text
Client
  -> Proposal
  -> Project
  -> Questionnaire
```

Secara produk, arah arsitektur sudah sesuai visi ResearchAI sebagai Operating System perusahaan riset, bukan CRM biasa.

Namun, karena ResearchAI mulai berkembang dari modul sederhana menjadi ERP riset, beberapa area perlu distabilkan sebelum modul berikutnya seperti Sample, Fieldwork, QC, Dataset, Dashboard, Report, dan Invoice ditambahkan.

Prioritas utama:

1. Database migration framework.
2. Role-based access control.
3. Workflow/state transition consistency.
4. Shared activity logging service.
5. Frontend component modularization.
6. API documentation and deprecated endpoint policy.

## 2. Domain Model Review

### Kondisi Saat Ini

Domain utama yang sudah berjalan:

```text
Client
  |
  +-- Contact
  |
  +-- Activity
  |
  +-- Proposal
          |
          +-- Project
                  |
                  +-- Questionnaire
```

Kekuatan:

- Proposal dan Project sudah dipisahkan dengan benar.
- Proposal tetap menjadi business document.
- Project menjadi operational object.
- Project dibuat dari Proposal Approved melalui action Setup Project.
- Multiple Questionnaire sudah mendukung project riset dengan banyak target respondent.
- Activity Timeline mulai menjadi cross-cutting behavior.

Kekurangan:

- Domain Sample, Fieldwork, QC, Dataset, Report, dan Invoice belum memiliki kontrak konseptual di kode.
- Activity masih tersimpan sebagai `ClientActivity`, bukan domain event general.
- Questionnaire sudah one-to-many, tetapi belum terhubung ke Sample atau Fieldwork.
- Belum ada konsep Team, Assignment, atau Resource yang akan dibutuhkan Fieldwork.

Risiko Jangka Panjang:

- Jika semua aktivitas hanya disimpan sebagai Client Activity, timeline Project dan module-level audit akan sulit dibangun.
- Jika Sample dibangun tanpa hubungan jelas ke Questionnaire, proses multi-target respondent bisa menjadi kacau.
- Jika status setiap modul dibuat manual dan terpisah, workflow ERP akan sulit dikendalikan.

Rekomendasi:

- Tetapkan `Project` sebagai root operasional.
- Definisikan domain `Sample` sebelum Fieldwork.
- Buat konsep `Domain Activity/Event` yang bisa ditampilkan di Client Timeline, Project Timeline, dan module timeline.
- Gunakan ADR untuk setiap transisi domain besar.

## 3. Database Design Review

### Kondisi Saat Ini

Database menggunakan SQLAlchemy model dengan table:

- `clients`
- `client_contacts`
- `client_activities`
- `proposals`
- `projects`
- `questionnaires`
- `users`
- `roles`
- `user_roles`

Kekuatan:

- UUID sudah digunakan sebagai primary key.
- Foreign key antar domain inti sudah tersedia.
- Index dasar sudah tersedia pada field pencarian/status.
- `Project.proposal_id` memiliki unique constraint, sesuai rule MVP: satu Proposal maksimal satu Project.
- `Questionnaire.project_id` mendukung one-to-many.
- Field numeric budget/value menggunakan `Numeric`.

Kekurangan:

- Belum ada migration framework resmi seperti Alembic.
- Upgrade schema masih menggunakan script manual.
- Beberapa status masih berupa string bebas, belum enum/check constraint.
- Belum ada audit fields standar yang konsisten untuk semua action-level changes.
- Belum ada soft delete.
- Belum ada tenant/company boundary.
- Belum ada constraint uniqueness untuk kombinasi tertentu, misalnya `project_id + sort_order`.

Risiko Jangka Panjang:

- Schema drift antar environment.
- Sulit rollback jika migration gagal.
- Data status bisa inkonsisten jika validasi service terlewati.
- Sulit mendukung multi-company atau production setup.

Rekomendasi:

- Implement Alembic sebelum schema bertambah besar.
- Tambahkan DB-level constraint untuk status penting secara bertahap.
- Buat migration baseline dari schema saat ini.
- Buat seed data formal untuk admin, roles, dan master data research type.
- Pertimbangkan `organization_id` sebelum multi-user production.

## 4. API Design Review

### Kondisi Saat Ini

Endpoint utama:

```text
/api/v1/auth
/api/v1/clients
/api/v1/proposals
/api/v1/projects
/api/v1/questionnaires
```

Kekuatan:

- API sudah resource-oriented.
- Proposal dan Questionnaire menggunakan endpoint plural.
- Status action dipisahkan dari edit form melalui endpoint status.
- Setup Project dibuat sebagai business action dari Proposal.
- Response model menggunakan schema Pydantic.
- Authentication dependency sudah konsisten menggunakan bearer token.

Kekurangan:

- Beberapa endpoint action masih belum sepenuhnya konsisten secara naming.
- Deprecated endpoint Questionnaire singular belum diberi marker formal di Swagger.
- Belum ada pagination untuk list endpoint.
- Belum ada standardized error response.
- Belum ada API versioning policy selain prefix `/api/v1`.
- Belum ada authorization policy per role/action.

Risiko Jangka Panjang:

- List endpoint akan berat saat data bertambah.
- Developer bisa memakai endpoint deprecated karena belum ditandai.
- Frontend harus menangani banyak bentuk error manual.
- API action akan semakin sulit dirawat jika setiap modul membuat pola sendiri.

Rekomendasi:

- Buat API convention document.
- Tambahkan pagination, sorting, dan filtering standar.
- Tandai deprecated endpoint di OpenAPI.
- Gunakan action endpoint konsisten:

```text
POST /proposals/{id}/actions/setup-project
POST /projects/{id}/actions/mark-ready
POST /questionnaires/{id}/actions/mark-ready
```

Catatan:

- Perubahan action endpoint tidak harus sekarang karena dapat breaking change. Untuk MVP, cukup dokumentasikan convention baru dan migrasikan bertahap.

## 5. Frontend Structure Review

### Kondisi Saat Ini

Frontend menggunakan:

- React
- Vite
- Axios service layer
- Pages per module
- Shared UI component sederhana di `components/ui.jsx`
- Shared formatter dan status styles

Kekuatan:

- Struktur mudah dipahami.
- Service API dipisahkan dari page.
- Komponen reusable dasar sudah mulai terbentuk.
- Design System v1 mulai tercermin di UI.
- Routing sederhana dan cocok untuk MVP.

Kekurangan:

- Page components mulai panjang dan memuat banyak logic.
- Belum ada module folder per domain.
- Form handling masih manual di setiap page.
- Error/loading state belum sepenuhnya reusable.
- Tidak ada test frontend permanen.
- Terminologi UI masih campuran Indonesia-Inggris.

Risiko Jangka Panjang:

- Saat modul Sample/Fieldwork masuk, folder `pages` akan penuh dan sulit dirawat.
- Duplicate pattern untuk forms, status actions, detail cards, dan tables akan bertambah.
- Perubahan Design System harus dilakukan manual di banyak halaman.

Rekomendasi:

- Refactor bertahap ke module structure:

```text
src/modules/proposals
src/modules/projects
src/modules/questionnaires
src/modules/clients
```

- Buat reusable components:
  - `PageHeader`
  - `Breadcrumb`
  - `DataTable`
  - `StatusActionPanel`
  - `Timeline`
  - `FormSection`
  - `LinkField`

## 6. Folder Structure Review

### Kondisi Saat Ini

Folder root sudah memisahkan:

- Product Management
- UI/UX
- Database
- Backend
- Frontend
- API
- Testing
- Deployment
- Documentation
- Project Management

Kekuatan:

- Cocok untuk product-led development.
- Dokumen keputusan dan sprint tersimpan.
- Memudahkan user non-teknis memahami perkembangan.

Kekurangan:

- Banyak dokumen lama masih untracked di Git.
- Beberapa dokumen arsitektur berada di `00_Project_Management`, beberapa di `11_Documentation`.
- Belum ada aturan jelas dokumen mana yang authoritative.
- Backend memiliki `__pycache__` di filesystem, walaupun tidak terlihat masuk Git.

Risiko Jangka Panjang:

- Dokumen bisa saling tumpang tindih.
- Sprint berikutnya bisa memakai dokumen lama yang bukan baseline terbaru.

Rekomendasi:

- Tetapkan folder authoritative:
  - ADR: `00_Project_Management`
  - Workflow: `11_Documentation`
  - Design System: `02_UI_UX`
  - Sprint Summary: `00_Project_Management`
- Tambahkan index dokumen baseline aktif.
- Pastikan `.gitignore` menjaga artifact temporary seperti `__pycache__`, `dist`, dan screenshot testing.

## 7. Naming Convention Review

Kekuatan:

- Backend menggunakan pola `models`, `schemas`, `services`, `api`.
- Field database cukup deskriptif.
- Proposal Number dan Project Number konsisten.

Kekurangan:

- Status Proposal di workflow dokumen menggunakan istilah `Sent to Client`, sedangkan kode memakai `Sent`.
- Questionnaire docs sempat memakai `respondent_group`, sedangkan implementasi final memakai `target_respondent`.
- UI menggunakan campuran `Client`, `Project`, `Questionnaire`, `Target Respondent`.
- Endpoint action belum punya convention final.

Risiko Jangka Panjang:

- Inkonsistensi nama akan memperlambat onboarding developer.
- Mapping dokumen ke kode bisa membingungkan.

Rekomendasi:

- Buat `Naming_Convention_v1.md`.
- Tetapkan istilah canonical:
  - `Client`
  - `Proposal`
  - `Project`
  - `Questionnaire`
  - `Target Respondent`
  - `Instrument Type`
- Hindari sinonim untuk field yang sama.

## 8. Design System Review

Kekuatan:

- Card, badge, button, loading, error, dan placeholder sudah cukup konsisten.
- UI tenang dan cocok untuk operational tool.
- Project Detail dan Questionnaire sudah mengikuti pola Design System.

Kekurangan:

- Design System masih berupa dokumen dan komponen sederhana.
- Belum ada component-level enforcement.
- Tidak ada token warna/spacing formal.
- Status badge styles masih manual.

Risiko Jangka Panjang:

- Setiap modul baru bisa menciptakan variasi UI sendiri.
- UI akan kehilangan konsistensi saat jumlah page bertambah.

Rekomendasi:

- Ubah Design System menjadi reusable component library kecil di frontend.
- Tambahkan status style map terpusat per domain.
- Buat table/list component standar sebelum Sample.

## 9. Security Review

Kekuatan:

- Password hashing sudah menggunakan library hash modern.
- JWT bearer token sudah tersedia.
- Endpoint utama memerlukan user login.
- User active/status dicek saat request.

Kekurangan:

- Secret key default masih ada di config.
- Tidak ada refresh token atau session revocation.
- Token disimpan di localStorage.
- Belum ada role-based access control.
- Belum ada object-level authorization.
- CORS/security headers belum terlihat sebagai kebijakan lengkap.
- Validasi URL KoBo/XLSForm belum ketat.

Risiko Jangka Panjang:

- User dapat mengakses data lintas Project jika hanya mengandalkan login.
- LocalStorage rentan jika aplikasi terkena XSS.
- Production deployment berisiko jika secret tidak dikelola ketat.

Rekomendasi:

- Implement RBAC sebelum production.
- Tambahkan object-level access rule.
- Wajibkan `SECRET_KEY` dari environment untuk non-development.
- Pertimbangkan httpOnly cookie atau mitigasi XSS sebelum production.
- Tambahkan validation untuk external URL fields.

## 10. Scalability Review

Kekuatan:

- Modular backend sederhana mudah dikembangkan.
- Relationship dasar sudah benar untuk Proposal -> Project -> Questionnaire.
- Index dasar pada status dan foreign key sudah ada.

Kekurangan:

- Belum ada pagination.
- Belum ada background job.
- Belum ada file storage abstraction nyata.
- Belum ada caching.
- Activity logging masih synchronous di service utama.

Risiko Jangka Panjang:

- List Proposal/Project/Questionnaire bisa berat.
- Activity Timeline bisa menjadi lambat jika data besar.
- Integrasi KoBo, XLSForm parsing, dan report generation akan butuh job queue.

Rekomendasi:

- Tambahkan pagination sebelum data produksi.
- Siapkan background job untuk import/export dan AI tasks.
- Buat file/document storage service sebelum attachment.
- Optimalkan query timeline saat activity tumbuh.

## 11. Maintainability Review

Kekuatan:

- Kode masih mudah dibaca.
- Pemisahan API, service, schema, model sudah baik untuk MVP.
- Sprint documents membantu menjaga product reasoning.

Kekurangan:

- Business rules tersebar di service.
- Activity logging logic berulang di Proposal, Project, Questionnaire.
- Status transition logic manual di setiap service.
- Belum ada automated test suite yang menjadi safety net.

Risiko Jangka Panjang:

- Perubahan workflow bisa menyebabkan regression.
- Modul baru akan copy-paste pattern lama.
- Activity logging bisa tidak konsisten antar modul.

Rekomendasi:

- Buat shared `activity_service`.
- Buat shared `workflow/state_transition` helper.
- Tambahkan backend integration tests minimal untuk business-critical flow.
- Buat API contract testing untuk Proposal -> Project -> Questionnaire.

## 12. Overall Assessment

### Kelebihan Utama

- Domain direction benar.
- Proposal dan Project dipisahkan dengan baik.
- Multiple Questionnaire sudah sesuai proses bisnis riset.
- Activity Timeline mulai dibangun sebagai kebiasaan lintas modul.
- UI sudah stabil untuk MVP.

### Kekurangan Utama

- Migration belum production-grade.
- Authorization belum cukup untuk ERP.
- Workflow belum punya abstraction.
- Frontend mulai membutuhkan modularisasi.
- Dokumentasi baseline perlu dirapikan.

### Risiko Jangka Panjang

- Schema drift.
- Inconsistent workflow.
- Security gap saat multi-user.
- UI duplication.
- Activity/audit sulit diperluas.

## 13. Final Recommendation

Sebelum membangun modul besar berikutnya, ResearchAI sebaiknya melakukan satu sprint technical foundation ringan.

Rekomendasi urutan:

1. Migration framework baseline.
2. API convention and deprecated endpoint policy.
3. Shared Activity Service.
4. Workflow transition helper.
5. Frontend reusable table/form/action components.

Setelah itu, lanjut ke Product Discovery dan Design Review untuk Sample Foundation.
