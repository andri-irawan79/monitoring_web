"""Basis aturan FIS-1/FIS-2 dan prioritas fase versi 1.2."""

# Urutan siklus operasional.
PHASES = ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")

# Konsekuen FIS-1 dibedakan menjadi:
# - tidak_perlu: keluaran deterministik Z=0;
# - rendah: kebutuhan kecil tetapi tetap positif;
# - sedang dan tinggi: kebutuhan meningkat.
FIS1_RULES = {
    ("rendah", "tinggi"): "tinggi",
    ("rendah", "sedang"): "sedang",
    ("rendah", "rendah"): "rendah",
    ("sedang", "tinggi"): "sedang",
    ("sedang", "sedang"): "sedang",
    ("sedang", "rendah"): "rendah",
    ("tinggi", "tinggi"): "tidak_perlu",
    ("tinggi", "sedang"): "tidak_perlu",
    ("tinggi", "rendah"): "tidak_perlu",
    # Prapanen: P2O5 tidak diberikan pada basis Tabel 7 (satu bulan sebelum panen).
    ("rendah", "tidak_diperlukan"): "tidak_perlu",
    ("sedang", "tidak_diperlukan"): "tidak_perlu",
    ("tinggi", "tidak_diperlukan"): "tidak_perlu",
}

# Prioritas bersifat kualitatif, bukan persentase dosis. "tidak_diperlukan"
# adalah pengecualian operasional untuk P2O5 pada fase Prapanen.
PHASE_PRIORITY = {
    "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
    "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
    "Prapanen": {"N": "tinggi", "P": "tidak_diperlukan", "K": "tinggi"},
}

# FIS-2 tetap menggunakan tiga kategori keluaran lama, hanya berdasarkan pH.
FIS2_RULES = {
    "masam": ("tinggi", "rendah"),
    "normal": ("rendah", "rendah"),
    "basa": ("rendah", "tinggi"),
}
