"""Basis aturan FIS-1 dan FIS-2 dari proyek ZIP acuan."""

PHASES = ("Pascapanen", "Vegetatif", "Pembungaan", "Pembuahan", "Panen")

# (status hara, prioritas fase) -> tingkat kebutuhan hara
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

PHASE_PRIORITY = {
    "Pascapanen": {"N": "sedang", "P": "sedang", "K": "sedang"},
    "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "rendah"},
    "Pembungaan": {"N": "rendah", "P": "sedang", "K": "sedang"},
    "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
    "Panen": {"N": "rendah", "P": "rendah", "K": "rendah"},
}

# status pH -> (kebutuhan Dolomit, kebutuhan Belerang)
FIS2_RULES = {
    "masam": ("tinggi", "rendah"),
    "normal": ("rendah", "rendah"),
    "basa": ("rendah", "tinggi"),
}
