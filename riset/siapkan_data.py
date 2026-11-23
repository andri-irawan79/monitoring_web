"""Menyiapkan data simulasi 365 hari dari Crop_recommendationV2.csv.

Langkah (sesuai subbab 3.3.3 dan 3.3.4):
1. Saring 6 tanaman buah tahunan: banana, coconut, mango, orange, papaya, pomegranate (600 baris).
2. Ambil 365 baris dengan sampel acak terstratifikasi per tanaman (61,61,61,61,61,60) memakai seed tetap.
3. Acak urutan dengan seed yang sama lalu beri nomor hari 1-365.
4. Hitung kuartil 25/50/75 dari 600 baris (bukan dari 365) untuk kalibrasi himpunan fuzzy.

Pemakaian:  python siapkan_data.py Crop_recommendationV2.csv
Keluaran :  data_simulasi_365.csv dan kuartil_600.csv
"""
import sys
import pandas as pd

SEED = 42
BUAH = ["banana", "coconut", "mango", "orange", "papaya", "pomegranate"]
JUMLAH = {"banana": 61, "coconut": 61, "mango": 61, "orange": 61, "papaya": 61, "pomegranate": 60}
KOLOM = ["N", "P", "K", "ph", "soil_moisture", "temperature", "humidity", "rainfall"]

def main(path):
    df = pd.read_csv(path)
    buah = df[df["label"].isin(BUAH)].copy()
    assert len(buah) == 600, len(buah)

    bagian = [g.sample(n=JUMLAH[k], random_state=SEED) for k, g in buah.groupby("label")]
    sampel = pd.concat(bagian).sample(frac=1.0, random_state=SEED).reset_index(drop=True)
    sampel.insert(0, "hari", range(1, len(sampel) + 1))
    sampel[["hari"] + KOLOM + ["label"]].to_csv("data_simulasi_365.csv", index=False)

    kuartil = buah[KOLOM].quantile([0.25, 0.5, 0.75]).T
    kuartil.columns = ["q25", "q50", "q75"]
    kuartil.round(2).to_csv("kuartil_600.csv")
    print(kuartil.round(2))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Crop_recommendationV2.csv")
