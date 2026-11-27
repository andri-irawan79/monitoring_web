"""Uji kewajaran dosis tahunan versi FIS-1 v1.2 (subbab 3.8.2c).

Untuk tiap skenario, sistem dijalankan pada lima fase (satu siklus tahunan), dosis pupuk dikonversi ke
gram hara, lalu dijumlahkan dan dibandingkan dengan kisaran gabungan lima sumber (Tabel bukti dosis, 3.6.8).

Kriteria wajar:
  (1) skenario 'hara rendah' berada dalam kisaran rujukan (toleransi pembulatan 2%),
  (2) skenario 'hara tinggi' menghasilkan dosis tahunan lebih kecil daripada 'hara rendah' (tiap hara),
  (3) tidak ada skenario yang melampaui batas atas rujukan.

Pemakaian: python uji_kewajaran.py   ->  hasil_kewajaran.csv dan ringkasan di layar
"""
import csv
from fuzzy_tsukamoto import FASE, hara_dari_dosis, rekomendasi

KISARAN = {"N": (649, 1800), "P": (490, 1560), "K": (717, 4000)}     # g hara per pohon per tahun
SKENARIO = ["SK-19", "SK-20", "SK-21", "SK-22", "SK-23", "SK-24", "SK-05", "SK-07", "SK-11", "SK-17"]
RENDAH, TINGGI = "SK-19", "SK-21"
TOLERANSI = 0.02

def tahunan(r):
    total = {"N": 0.0, "P": 0.0, "K": 0.0}
    for fase in FASE:
        d = rekomendasi(float(r["N"]), float(r["P"]), float(r["K"]), float(r["ph"]),
                        float(r["soil_moisture"]), float(r["rainfall"]), fase)["dosis"]
        for h, v in hara_dari_dosis(d).items():
            total[h] += v
    return total

def jalankan(path="skenario_uji.csv"):
    with open(path) as f:
        data = {r["id"]: r for r in csv.DictReader(f)}
    hasil = {i: tahunan(data[i]) for i in SKENARIO}
    baris, wajar = [], 0
    for i, tot in hasil.items():
        diatas = [h for h in tot if tot[h] > KISARAN[h][1]]
        ok = not diatas
        if i == RENDAH:
            ok = ok and all(KISARAN[h][0] * (1 - TOLERANSI) <= tot[h] <= KISARAN[h][1] for h in tot)
        if i == TINGGI:
            ok = ok and all(tot[h] < hasil[RENDAH][h] for h in tot)
        wajar += ok
        baris.append({"id": i, "tujuan": data[i]["tujuan"], "N_g": round(tot["N"]), "P2O5_g": round(tot["P"]),
                      "K2O_g": round(tot["K"]), "melampaui_batas_atas": ",".join(diatas) or "-",
                      "wajar": "ya" if ok else "tidak"})
    return baris, wajar

if __name__ == "__main__":
    baris, wajar = jalankan()
    with open("hasil_kewajaran.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(baris[0]))
        w.writeheader(); w.writerows(baris)
    for b in baris:
        print(f"{b['id']}  N={b['N_g']:>5}  P2O5={b['P2O5_g']:>5}  K2O={b['K2O_g']:>5}  wajar={b['wajar']:<5} {b['tujuan'][:48]}")
    print(f"Skenario wajar: {wajar}/{len(baris)} = {100 * wajar / len(baris):.0f}% (ambang 80%)")
