"""Basis aturan FIS-1/FIS-2 dan prioritas fase versi 1.1."""

# Urutan siklus operasional yang ditampilkan kepada pengguna.
# Panen aktif tidak menjadi kategori tersendiri; prapanen berakhir pada
# pemetikan pertama, dan siklus berikutnya dimulai dengan Pascapanen.
PHASES = ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")

FIS1_RULES = {
    ("rendah", "tinggi"): "tinggi",
    ("rendah", "sedang"): "sedang",
    ("rendah", "rendah"): "rendah",
    ("sedang", "tinggi"): "sedang",
    ("sedang", "sedang"): "sedang",
    ("sedang", "rendah"): "rendah",
    ("tinggi", "tinggi"): "rendah",
    ("tinggi", "sedang"): "rendah",
    ("tinggi", "rendah"): "rendah",
}

# Prioritas kualitatif; bukan persentase pembagian dosis tahunan.
PHASE_PRIORITY = {
    "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
    "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
    "Prapanen": {"N": "tinggi", "P": "rendah", "K": "tinggi"},
}

FIS2_RULES = {
    "masam": ("tinggi", "rendah"),
    "normal": ("rendah", "rendah"),
    "basa": ("rendah", "tinggi"),
}
