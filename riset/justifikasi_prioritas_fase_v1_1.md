# Justifikasi Matriks Prioritas Fase NPK — Versi 1.1

## Ruang lingkup
Matriks dipakai untuk rekomendasi komputasional pada durian Montong produktif (umur minimal 10 tahun). Data monitoring adalah data simulasi, bukan pengukuran tanah kebun Monthong atau dosis lapangan. Matriks merupakan penjabaran kualitatif rujukan agronomi untuk basis aturan, bukan standar pemupukan universal.

## Definisi operasional lima fase
1. **Pascapanen**: setelah buah terakhir dipetik sampai muncul flush baru.
2. **Vegetatif**: pertumbuhan flush/tunas dan daun baru pada pohon produktif sampai daun berkembang dan matang.
3. **Prapembungaan**: setelah flush matang sampai sebelum bunga pertama mekar. Periode 1–2 bulan sebelum berbunga merupakan penanda literatur, bukan kalender tetap.
4. **Pembuahan**: kategori generatif operasional yang mencakup bunga mekar, pembentukan pentil setelah mahkota bunga luruh, dan pembesaran buah; berakhir ketika jendela prapanen dimulai.
5. **Prapanen**: kira-kira satu bulan sebelum perkiraan panen sampai pemetikan buah pertama.

**Panen aktif tidak menjadi fase tersendiri** dalam model lima fase. Ketika pemetikan berlangsung, kategori sistem tidak dimaksudkan menghasilkan rekomendasi pemupukan. Setelah pemetikan terakhir, pengguna berpindah ke Pascapanen. Ini merupakan penyederhanaan antarmuka dan batasan model.

## Matriks prioritas
| Fase | N | P₂O₅ | K₂O |
|---|---|---|---|
| Pascapanen | Rendah | Tinggi | Tinggi |
| Vegetatif | Tinggi | Sedang | Tinggi |
| Prapembungaan | Rendah | Tinggi | Tinggi |
| Pembuahan | Sedang | Sedang | Tinggi |
| Prapanen | Tinggi | Rendah | Tinggi |

## Dasar pemetaan
Buku Lapang Budidaya Durian Kementerian Pertanian (2021), Tabel 7, mengompilasi rekomendasi pemupukan durian produktif dari Haifa Thailand. Nilai per tanaman yang relevan:
- Satu minggu setelah panen: N 45–90 g, P₂O₅ 135–270 g, K₂O 135–270 g.
- Saat keluar pucuk daun: N 210–420 g, P₂O₅ 105–210 g, K₂O 420–840 g.
- Satu sampai dua bulan sebelum berbunga: N 45–90 g, P₂O₅ 135–270 g, K₂O 135–270 g.
- Saat bunga mekar: N 70–140 g, P₂O₅ 35–70 g, K₂O 140–280 g.
- Saat mahkota bunga luruh/pentil buah: N 18–36 g, P₂O₅ 54–108 g, K₂O 54–168 g.
- Enam minggu setelah bunga mekar: N 210–420 g, P₂O₅ 105–210 g, K₂O 420–840 g.
- Satu bulan sebelum panen: N 260–390 g, P₂O₅ 0 g, K₂O 920–1.400 g.

Prioritas Rendah/Sedang/Tinggi adalah penyederhanaan ordinal, bukan pembagian angka sumber menjadi persentase dosis per fase. Pascapanen dan Prapembungaan sama-sama diberi N rendah, P/K tinggi karena nilai pada stadia satu minggu setelah panen dan 1–2 bulan sebelum berbunga berada pada rentang sama. Vegetatif menempatkan N/K tinggi, P sedang mengikuti pola pucuk daun baru. Pembuahan menggabungkan tiga stadia generatif yang kebutuhan haranya bervariasi; prioritas N dan P sedang serta K tinggi adalah pendekatan agregat. Prapanen menempatkan N/K tinggi dan P rendah mengikuti tabel satu bulan sebelum panen.

Buku Kementerian Pertanian (2023), *Teknologi Produksi Melalui Pengaturan Fase Pembungaan dan Pembuahan Durian*, membedakan fase pembungaan dan pembuahan. Rujukan ini mendukung perlunya definisi operasional, tetapi tidak menyediakan matriks NPK universal yang dapat langsung dipindahkan ke penelitian ini.

## Kalibrasi D_ref v1.1
Target tahunan pembanding satu studi Monthong Thailand adalah 1.150 g N, 490 g P₂O₅, dan 1.710 g K₂O per pohon per tahun (Srisombat et al., 2019). Dalam skenario dasar saat semua status hara Rendah, FIS-1 menghasilkan Z=0 untuk prioritas Rendah, Z=50 untuk Sedang, dan Z=100 untuk Tinggi. Jumlah Z lima fase:
- N: 0 + 100 + 0 + 50 + 100 = 250%.
- P₂O₅: 100 + 50 + 100 + 50 + 0 = 300%.
- K₂O: 100 + 100 + 100 + 100 + 100 = 500%.

Maka D_ref: N = 1.150 / 2,5 = **460 g**; P₂O₅ = 490 / 3 = **163,33 g**; K₂O = 1.710 / 5 = **342 g**.

D_ref adalah konstanta skala pada rumus Tₓ = (Zₓ/100) × D_ref,ₓ. Ini bukan dosis pupuk per fase, bukan rekomendasi universal, dan bukan hasil validasi lapangan. Pembulatan produk dapat membuat akumulasi pada skenario dasar sedikit berbeda dari target.

## Batasan interpretasi
- Tabel 7 menyebut Haifa Thailand sebagai sumber; bukan uji lapangan khusus pada lokasi penelitian.
- Sumber menguraikan stadia lebih rinci daripada lima kategori sistem. Penggabungan bunga mekar, pentil, dan pembesaran buah ke Pembuahan mengurangi resolusi agronomi.
- Dataset masukan bukan analisis laboratorium tanah durian Monthong. Hasil dosis adalah estimasi komputasional.
- Dosis Dolomit/Belerang tidak dapat diputuskan hanya dari pH awal. Keluaran FIS-2 indikatif dan memerlukan analisis tanah serta kebutuhan kapur/belerang.
- Uji kesesuaian terhadap tabel acuan menilai konsistensi implementasi dengan aturan peneliti, bukan validasi agronomis independen.

## Referensi
Direktorat Buah dan Florikultura. (2021). *Buku Lapang Budidaya Durian*. Direktorat Jenderal Hortikultura, Kementerian Pertanian. Tabel 7; sumber tabel: Haifa Thailand.

Nuraini, F., Fajarsari, I. M., Rosita, D., & Cahyani, E. N. (2023). *Teknologi Produksi Melalui Pengaturan Fase Pembungaan dan Pembuahan Durian*. Pertanian Press.

Srisombat, et al. (2019). Entri bibliografi lengkap mengikuti daftar pustaka pada naskah utama; digunakan sebagai pembanding target hara tahunan Monthong pada satu lokasi penelitian di Thailand.
