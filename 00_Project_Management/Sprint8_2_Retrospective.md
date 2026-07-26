# Sprint 8.2 Retrospective

Nama Sprint:
Sampling Plan API Layer

Tanggal:
26 Juli 2026

## 1. What Went Well

1. Design Freeze membuat scope API sangat jelas.
2. Endpoint Sample Group dan Sampling Target berhasil dipisahkan dengan rapi.
3. Business rule penting berhasil diamankan melalui test:
   - Delete Sample Group hanya Draft.
   - Delete target terakhir ditolak.
   - Full replacement targets tidak membuat orphan record.
4. Swagger/OpenAPI langsung tersedia karena mengikuti pola FastAPI existing.
5. Activity Logging tetap diperlakukan sebagai cross-cutting behavior.

## 2. What Can Be Improved

1. Technical debt migration perlu segera ditangani agar perubahan database lebih aman.
2. Error response perlu distandarkan agar frontend lebih mudah menampilkan pesan.
3. Project-level permission perlu mulai dirancang sebelum modul operasional semakin luas.
4. Warning deprecated sebaiknya dirapikan sebelum menumpuk.
5. Dokumentasi API sebaiknya dilengkapi contoh payload yang siap dipakai QA/manual test.

## 3. Technical Debt

| ID | Technical Debt | Priority | Recommendation |
| --- | --- | --- | --- |
| TD-SAMPLING-API-001 | Error response belum standardized | Low | Buat standard error envelope |
| TD-SAMPLING-API-002 | Permission masih authenticated user | Medium | Rancang project-level permission |
| TD-SAMPLING-API-003 | Response list bisa berat jika target banyak | Low | Buat lightweight list response bila dibutuhkan |
| TD-SAMPLING-API-004 | Filter list belum masuk API MVP | Low | Tambahkan setelah kebutuhan frontend jelas |
| TD-SAMPLING-API-005 | Alembic migration framework belum tersedia | Medium | Prioritaskan technical foundation sprint |
| TD-SAMPLING-API-006 | `datetime.utcnow()` deprecated warning | Low | Ganti ke timezone-aware datetime |
| TD-SAMPLING-API-007 | HTTP 422 constant deprecated warning | Low | Update constant FastAPI |

## 4. Action Item untuk Sprint 8.3

1. Mulai Design Review Frontend Sampling Plan.
2. Gunakan endpoint Sprint 8.2 sebagai kontrak API final.
3. Rancang UI Project Detail section Sampling Plan.
4. Rancang form Sample Group dan Target Wilayah.
5. Pastikan frontend memahami bahwa PATCH `targets` berarti full replacement.
6. Siapkan browser testing untuk Project -> Sampling Plan.

## 5. Closing Note

Sprint 8.2 menutup fondasi API Sampling Plan dan siap menjadi dasar Sprint 8.3.
