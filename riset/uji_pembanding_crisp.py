"""Pembanding berbatas tegas (crisp) terhadap fuzzy Tsukamoto (subbab 3.8.3).

Pada matriks fase v1.1, beberapa kombinasi menunjukkan kenaikan lokal Z yang kecil
ketika kadar hara naik. Uji monotonik melaporkan jumlahnya; batas yang diterapkan
adalah maksimum kenaikan satu langkah, bukan klaim bahwa kurva selalu menurun.

Nilai satu hara digeser bertahap sebesar 1 unit pada seluruh rentang data; hara lain tidak ikut dihitung
karena Z tiap hara berdiri sendiri (FIS-1). Yang dibandingkan adalah tingkat kebutuhan Z (% dari D_ref),
sehingga loncatan Z sama dengan loncatan dosis sebagai persen D_ref.

Pembanding crisp:
  'kuartil' : kelas dari ambang kuartil (Rendah <= a, Tinggi >= b, selain itu Sedang), seperti rumusan 3.8.3
  'argmax'  : kelas dengan derajat keanggotaan tertinggi (versi crisp yang lebih kuat)
Dosis kategori: kebutuhan Rendah = 0, Sedang = 50, Tinggi = 100 (% D_ref).

Pemakaian: python uji_pembanding_crisp.py   ->  hasil_pembanding_crisp.csv dan ringkasan di layar
"""
import csv
from fuzzy_tsukamoto import ATURAN1, FASE, PRIORITAS, PROFIL_A, status_hara, z_fis1

RENTANG = {"N": (0, 140), "P": (5, 145), "K": (5, 205)}     # min-maks seluruh data (subbab 3.3.4)
SKOR = {"rendah": 0.0, "sedang": 50.0, "tinggi": 100.0}
BATAS_LONCATAN = 25.0                                         # % D_ref (subbab 3.8.3)

def z_crisp(x, hara, fase, varian, profil=PROFIL_A):
    a, c, b = profil[hara]
    if varian == "kuartil":
        s = "rendah" if x <= a else "tinggi" if x >= b else "sedang"
    else:
        mu = status_hara(x, profil[hara])
        s = max(mu, key=mu.get)
    return SKOR[ATURAN1[(s, PRIORITAS[fase][hara])]]

def jalankan(profil=PROFIL_A):
    baris = []
    for hara, (lo, hi) in RENTANG.items():
        xs = list(range(lo, hi + 1))
        for fase in FASE:
            deret = {
                "fuzzy": [z_fis1(x, hara, fase, profil) for x in xs],
                "crisp_kuartil": [z_crisp(x, hara, fase, "kuartil", profil) for x in xs],
                "crisp_argmax": [z_crisp(x, hara, fase, "argmax", profil) for x in xs],
            }
            for nama, z in deret.items():
                lonc = [abs(z[i + 1] - z[i]) for i in range(len(z) - 1)]
                baris.append({"hara": hara, "fase": fase, "metode": nama,
                              "langkah": len(lonc),
                              "loncatan_gt_25": sum(1 for v in lonc if v > BATAS_LONCATAN),
                              "loncatan_maks": round(max(lonc), 2),
                              "rata2_loncatan": round(sum(lonc) / len(lonc), 3)})
    return baris

def ringkas(baris):
    print(f"{'metode':<15}{'langkah':>9}{'loncatan>25':>13}{'loncatan maks':>15}")
    for m in ("fuzzy", "crisp_kuartil", "crisp_argmax"):
        sub = [b for b in baris if b["metode"] == m]
        print(f"{m:<15}{sum(b['langkah'] for b in sub):>9}{sum(b['loncatan_gt_25'] for b in sub):>13}"
              f"{max(b['loncatan_maks'] for b in sub):>15}")

def uji_monotonik():
    """Uji perilaku (3.8.3 butir 1): naiknya kadar hara tidak boleh menaikkan Z. Mengembalikan jumlah pelanggaran."""
    import fuzzy_tsukamoto as ft
    contoh = {}
    for mode in ("per_aturan", "jumlah"):
        ft.AGREGASI = mode
        total, kasus = 0, []
        for hara, (lo, hi) in RENTANG.items():
            for fase in FASE:
                z = [z_fis1(x, hara, fase) for x in range(lo, hi + 1)]
                nai = [(lo + i, round(z[i], 1), round(z[i + 1], 1)) for i in range(len(z) - 1)
                       if z[i + 1] > z[i] + 1e-9]
                maks_naik = max([b - a for _, a, b in nai], default=0)
                total += len(nai)
                if nai:
                    kasus.append((hara, fase, len(nai), nai[0]))
        contoh[mode] = (total, kasus)
    ft.AGREGASI = "jumlah"
    return contoh

if __name__ == "__main__":
    hasil = jalankan()
    with open("hasil_pembanding_crisp.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hasil[0]))
        w.writeheader(); w.writerows(hasil)
    ringkas(hasil)
    print("\nUji monotonik (kenaikan hara tidak boleh menaikkan Z):")
    for mode, (total, kasus) in uji_monotonik().items():
        print(f"  agregasi={mode:<11} pelanggaran={total:>4}  kombinasi hara-fase terdampak={len(kasus)}")
        for k in kasus[:4]:
            print("     ", k)
