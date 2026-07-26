# Product Owner Questions A0

Status:
Open for Product Owner Review

Tanggal:
26 Juli 2026

## Tujuan

Mencatat keputusan bisnis yang masih perlu dikonfirmasi sebelum Sprint 5 dan sebelum Project Management dimulai.

## Pertanyaan Sebelum Sprint 5

### Proposal Management

1. Apakah Sprint 5 tetap difokuskan pada `Proposal Form - Create Proposal`?
2. Apakah form create proposal tetap hanya berisi:
   - Client
   - Proposal Title
   - Research Type
   - Estimated Budget
3. Apakah tombol `+ Proposal Baru` di Proposal List langsung membuka form create?
4. Apakah setelah proposal dibuat, user langsung diarahkan ke Proposal Detail?
5. Apakah label `Next Business Action` perlu diganti menjadi `Aksi Bisnis Berikutnya`?

### Proposal to Project

6. Apakah action untuk membuat Project dari Proposal Approved disebut `Setup Project`, `Buat Project`, atau `Mulai Project Setup`?
7. Apakah Approved Proposal yang sudah dibuat menjadi Project harus dikunci dari perubahan status?
8. Apakah Proposal masih boleh diedit setelah Project dibuat?
9. Apakah satu Proposal satu Project sudah cukup untuk MVP Beerka?
10. Apakah Project tanpa Proposal benar-benar ditunda sampai phase berikutnya?

### Project Lifecycle

11. Apakah lifecycle Project MVP berikut disetujui?

```text
Setup -> Ready -> Fieldwork -> QC -> Analysis -> Reporting -> Completed
```

12. Apakah status `Ready` sesuai istilah operasional Beerka?
13. Apakah perlu status `On Hold` sejak MVP?
14. Apakah Project bisa kembali dari `QC` ke `Fieldwork` jika data tidak lolos QC?
15. Apakah Project bisa kembali dari `Reporting` ke `Analysis` jika report perlu revisi analisis?

### Project Setup

16. Apakah Project Manager wajib dipilih saat Project dibuat?
17. Apakah start date wajib diisi saat Project dibuat?
18. Apakah end date wajib diisi saat Project dibuat?
19. Apakah estimated budget dari Proposal menjadi project value sementara?
20. Apakah Project Number harus otomatis sejak MVP?

### Client 360

21. Apakah Client 360 tab Projects harus aktif segera setelah Project Management dibuat?
22. Apakah Project activity wajib tampil di Client Activity Timeline sejak Project sprint pertama?

### Finance dan Contract

23. Apakah Project boleh dibuat langsung dari Proposal Approved tanpa Contract untuk MVP?
24. Apakah Invoice boleh dibuat dari Project tanpa Contract pada MVP, atau Contract harus dibuat lebih dulu?

## Rekomendasi Decision Order

Urutan keputusan yang sebaiknya dijawab:

1. Konfirmasi Sprint 5 tetap Proposal Create.
2. Konfirmasi domain Proposal vs Project.
3. Konfirmasi lifecycle Project.
4. Konfirmasi aturan Project Setup.
5. Konfirmasi kapan Contract dan Invoice masuk.
