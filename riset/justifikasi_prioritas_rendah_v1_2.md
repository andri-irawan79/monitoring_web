# Perbaikan Konsekuen Prioritas Rendah — FIS-1 Versi 1.2

## 1. Masalah pada versi 1.1

Pada versi 1.1, konsekuen keluaran Rendah memiliki invers z = 10(1 - alpha), sehingga hasilnya berada pada rentang 0–10. Ambang minimum Z sebesar 10% kemudian memotong keluaran di bawah 10 menjadi nol. Selain itu, ketika semua aturan aktif memiliki konsekuen yang sama, implementasi menjumlahkan alpha dan membatasi jumlahnya pada 1. Pada prioritas Rendah, seluruh status hara dipetakan ke konsekuen Rendah; karena jumlah derajat keanggotaan status hara adalah 1, keluaran agregat selalu mencapai alpha=1 dan Z=0. Akibatnya, prioritas Rendah berarti Tidak perlu, padahal sumber agronomi mencatat kebutuhan N sebesar 45–90 g per pohon satu minggu setelah panen dan 1–2 bulan sebelum berbunga.

Masalahnya bukan sekadar ambang minimum, melainkan dua makna yang dicampur pada satu konsekuen: kebutuhan kecil dan tidak perlu pemupukan.

## 2. Prinsip perbaikan

Versi 1.2 memisahkan konsekuen FIS-1:

| Konsekuen | Invers z | Makna operasional |
|---|---|---|
| Tidak perlu | z = 0 | Tidak ada kebutuhan hara menurut rule |
| Rendah | z = 20,6 − 10α | Kebutuhan kecil tetapi positif |
| Sedang | z = 50α | Kebutuhan menengah |
| Tinggi | z = 50 + 50α | Kebutuhan tinggi |

Konsekuen Tidak perlu memakai fungsi monoton berbentuk langkah yang selalu menghasilkan Z=0. Konsekuen Rendah memakai fungsi turun monoton; pada kekuatan aturan penuh (alpha=1), Z=10,6%. Fungsi keluaran Sedang dan Tinggi dipertahankan seperti versi sebelumnya.

Ambang Z minimum 10% tidak lagi diterapkan pada FIS-1. Nol hanya dihasilkan oleh konsekuen Tidak perlu atau oleh hasil defuzzifikasi yang memang nol. Ambang 10% pada FIS-2 dipertahankan sehingga perilaku koreksi pH tidak berubah.

## 3. Perubahan aturan FIS-1

Sembilan aturan utama tetap menghubungkan status hara dengan prioritas fase. Perubahan konsekuen:

- Status hara Tinggi pada prioritas Rendah/Sedang/Tinggi sekarang menghasilkan Tidak perlu, bukan Rendah. Dengan demikian, kebutuhan hara yang sudah tinggi tidak otomatis menerima pupuk tambahan.
- Status Rendah atau Sedang pada prioritas Rendah menghasilkan Rendah positif, bukan nol.
- Untuk unsur P₂O₅ pada fase Prapanen ditambahkan pengecualian prioritas **Tidak diperlukan**. Ketiga status hara P pada fase tersebut menghasilkan Tidak perlu. Pengecualian ini didasarkan pada Tabel 7 yang mencantumkan P₂O₅ = 0 g per pohon satu bulan sebelum panen.

Matriks prioritas v1.2:
| Fase | N | P₂O₅ | K₂O |
|---|---|---|---|
| Pascapanen | Rendah | Tinggi | Tinggi |
| Vegetatif | Tinggi | Sedang | Tinggi |
| Prapembungaan | Rendah | Tinggi | Tinggi |
| Pembuahan | Sedang | Sedang | Tinggi |
| Prapanen | Tinggi | Tidak diperlukan | Tinggi |

## 4. Dasar angka keluaran Rendah

Tabel 7 Buku Lapang Budidaya Durian Kementerian Pertanian (2021) mencantumkan N 45–90 g per pohon satu minggu setelah panen serta 1–2 bulan sebelum berbunga. Nilai ini menjadi bukti bahwa kebutuhan N pada dua periode tersebut tidak nol. Target tahunan pembanding Monthong Thailand yang dipakai dalam penelitian adalah 1.150 g N, 490 g P₂O₅, dan 1.710 g K₂O per pohon per tahun (Srisombat et al., 2019).

Pada kekuatan aturan penuh, nilai Z lima fase saat semua status hara Rendah:
- N: 10,6 + 100 + 10,6 + 50 + 100 = 271,2%.
- P₂O₅: 100 + 50 + 100 + 50 + 0 = 300%.
- K₂O: 100 + 100 + 100 + 100 + 100 = 500%.

D_ref versi 1.2 dihitung:
- N = 1.150 / 2,712 = **424,04 g**.
- P₂O₅ = 490 / 3 = **163,33 g**.
- K₂O = 1.710 / 5 = **342 g**.

Untuk N pada fase berprioritas Rendah, Z=10,6% menghasilkan target teoritis sekitar 44,95 g N. Setelah dikonversi dengan kadar Urea 46%, jumlah produk sekitar 97,7 g dan dibulatkan menjadi 100 g per pohon. Hara N yang dipasok oleh produk setelah pembulatan sekitar 46 g, mendekati batas bawah 45 g pada Tabel 7. Angka ini hanya pemeriksaan kewajaran matematis terhadap satu rujukan Thailand, bukan bukti dosis aman atau efektif di lapangan.

## 5. Pemisahan FIS-1 dan FIS-2

FIS-1 menggunakan fungsi keluaran v1.2. FIS-2 tetap menggunakan fungsi keluaran lama dan ambang Z minimum 10%, karena aturan FIS-2 hanya mengatur koreksi pH dan tidak mempunyai konsekuen prioritas fase. Dengan demikian, perubahan konsekuen Rendah pada FIS-1 tidak membuat koreksi Dolomit atau Belerang muncul pada pH normal.

## 6. Batasan

- Nilai Tabel 7 bersumber dari Haifa Thailand dan bukan dosis lapangan Monthong Indonesia.
- D_ref dikalibrasi dari satu target tahunan dan lima kategori fase model; bukan rekomendasi jadwal pemupukan tahunan.
- Pembuahan tetap menggabungkan bunga mekar, pentil, dan pembesaran buah.
- Prioritas P₂O₅ Tidak diperlukan pada Prapanen hanya berlaku pada definisi operasional satu bulan sebelum panen sampai pemetikan pertama.
- Keluaran pupuk tetap memerlukan verifikasi analisis tanah, label pupuk, dan rekomendasi setempat.
- Uji 450 kombinasi menilai konsistensi internal aturan; tidak menjadi validasi agronomis independen.

## Referensi
Direktorat Buah dan Florikultura. (2021). *Buku Lapang Budidaya Durian*. Direktorat Jenderal Hortikultura, Kementerian Pertanian. Tabel 7; sumber tabel: Haifa Thailand.

Srisombat, et al. (2019). Entri bibliografi lengkap mengikuti daftar pustaka naskah utama; sumber target tahunan Monthong pada satu lokasi di Thailand.
