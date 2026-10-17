RULES = [

    # =====================================================
    # FASE VEGETATIF (R1-R12)
    # =====================================================

    {
        "id": 1,
        "fase": "Vegetatif",
        "conditions": [("N", "rendah"), ("PH", "asam")],
        "pupuk": "Urea",
        "output": "tinggi"
    },

    {
        "id": 2,
        "fase": "Vegetatif",
        "conditions": [("N", "rendah"), ("PH", "normal")],
        "pupuk": "Urea",
        "output": "tinggi"
    },

    {
        "id": 3,
        "fase": "Vegetatif",
        "conditions": [("N", "rendah"), ("PH", "basa")],
        "pupuk": "Urea",
        "output": "sedang"
    },

    {
        "id": 4,
        "fase": "Vegetatif",
        "conditions": [("N", "sedang"), ("PH", "asam")],
        "pupuk": "Urea",
        "output": "sedang"
    },

    {
        "id": 5,
        "fase": "Vegetatif",
        "conditions": [("N", "sedang"), ("PH", "normal")],
        "pupuk": "Urea",
        "output": "sedang"
    },

    {
        "id": 6,
        "fase": "Vegetatif",
        "conditions": [("N", "sedang"), ("PH", "basa")],
        "pupuk": "Urea",
        "output": "rendah"
    },

    {
        "id": 7,
        "fase": "Vegetatif",
        "conditions": [("N", "tinggi"), ("PH", "asam")],
        "pupuk": "Urea",
        "output": "rendah"
    },

    {
        "id": 8,
        "fase": "Vegetatif",
        "conditions": [("N", "tinggi"), ("PH", "normal")],
        "pupuk": "Urea",
        "output": "rendah"
    },

    {
        "id": 9,
        "fase": "Vegetatif",
        "conditions": [("N", "tinggi"), ("PH", "basa")],
        "pupuk": "Urea",
        "output": "rendah"
    },

    {
        "id": 10,
        "fase": "Vegetatif",
        "conditions": [("N", "rendah"), ("P", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 11,
        "fase": "Vegetatif",
        "conditions": [("N", "rendah"), ("K", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 12,
        "fase": "Vegetatif",
        "conditions": [("N", "sedang"), ("P", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    # =====================================================
    # FASE PEMBUNGAAN (R13-R24)
    # =====================================================

    {
        "id": 13,
        "fase": "Pembungaan",
        "conditions": [("P", "rendah"), ("PH", "asam")],
        "pupuk": "SP36",
        "output": "tinggi"
    },

    {
        "id": 14,
        "fase": "Pembungaan",
        "conditions": [("P", "rendah"), ("PH", "normal")],
        "pupuk": "SP36",
        "output": "tinggi"
    },

    {
        "id": 15,
        "fase": "Pembungaan",
        "conditions": [("P", "rendah"), ("PH", "basa")],
        "pupuk": "SP36",
        "output": "sedang"
    },

    {
        "id": 16,
        "fase": "Pembungaan",
        "conditions": [("P", "sedang"), ("PH", "asam")],
        "pupuk": "SP36",
        "output": "sedang"
    },

    {
        "id": 17,
        "fase": "Pembungaan",
        "conditions": [("P", "sedang"), ("PH", "normal")],
        "pupuk": "SP36",
        "output": "sedang"
    },

    {
        "id": 18,
        "fase": "Pembungaan",
        "conditions": [("P", "sedang"), ("PH", "basa")],
        "pupuk": "SP36",
        "output": "rendah"
    },

    {
        "id": 19,
        "fase": "Pembungaan",
        "conditions": [("P", "tinggi"), ("PH", "asam")],
        "pupuk": "SP36",
        "output": "rendah"
    },

    {
        "id": 20,
        "fase": "Pembungaan",
        "conditions": [("P", "tinggi"), ("PH", "normal")],
        "pupuk": "SP36",
        "output": "rendah"
    },

    {
        "id": 21,
        "fase": "Pembungaan",
        "conditions": [("P", "tinggi"), ("PH", "basa")],
        "pupuk": "SP36",
        "output": "rendah"
    },

    {
        "id": 22,
        "fase": "Pembungaan",
        "conditions": [("P", "rendah"), ("N", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 23,
        "fase": "Pembungaan",
        "conditions": [("P", "rendah"), ("K", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 24,
        "fase": "Pembungaan",
        "conditions": [("N", "sedang"), ("P", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    # =====================================================
    # FASE PEMBUAHAN (R25-R36)
    # =====================================================

    {
        "id": 25,
        "fase": "Pembuahan",
        "conditions": [("K", "rendah"), ("PH", "asam")],
        "pupuk": "KCl",
        "output": "tinggi"
    },

    {
        "id": 26,
        "fase": "Pembuahan",
        "conditions": [("K", "rendah"), ("PH", "normal")],
        "pupuk": "KCl",
        "output": "tinggi"
    },

    {
        "id": 27,
        "fase": "Pembuahan",
        "conditions": [("K", "rendah"), ("PH", "basa")],
        "pupuk": "KCl",
        "output": "sedang"
    },

    {
        "id": 28,
        "fase": "Pembuahan",
        "conditions": [("K", "sedang"), ("PH", "asam")],
        "pupuk": "KCl",
        "output": "sedang"
    },

    {
        "id": 29,
        "fase": "Pembuahan",
        "conditions": [("K", "sedang"), ("PH", "normal")],
        "pupuk": "KCl",
        "output": "sedang"
    },

    {
        "id": 30,
        "fase": "Pembuahan",
        "conditions": [("K", "sedang"), ("PH", "basa")],
        "pupuk": "KCl",
        "output": "rendah"
    },

    {
        "id": 31,
        "fase": "Pembuahan",
        "conditions": [("K", "tinggi"), ("PH", "asam")],
        "pupuk": "KCl",
        "output": "rendah"
    },

    {
        "id": 32,
        "fase": "Pembuahan",
        "conditions": [("K", "tinggi"), ("PH", "normal")],
        "pupuk": "KCl",
        "output": "rendah"
    },

    {
        "id": 33,
        "fase": "Pembuahan",
        "conditions": [("K", "tinggi"), ("PH", "basa")],
        "pupuk": "KCl",
        "output": "rendah"
    },

    {
        "id": 34,
        "fase": "Pembuahan",
        "conditions": [("K", "rendah"), ("P", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 35,
        "fase": "Pembuahan",
        "conditions": [("K", "rendah"), ("N", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 36,
        "fase": "Pembuahan",
        "conditions": [("N", "sedang"), ("P", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    # =====================================================
    # FASE PANEN (R37-R45)
    # =====================================================

    {
        "id": 37,
        "fase": "Panen",
        "conditions": [("N", "rendah")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    {
        "id": 38,
        "fase": "Panen",
        "conditions": [("P", "rendah")],
        "pupuk": "SP36",
        "output": "sedang"
    },

    {
        "id": 39,
        "fase": "Panen",
        "conditions": [("K", "rendah")],
        "pupuk": "KCl",
        "output": "sedang"
    },

    {
        "id": 40,
        "fase": "Panen",
        "conditions": [("N", "sedang"), ("P", "sedang")],
        "pupuk": "NPK",
        "output": "rendah"
    },

    {
        "id": 41,
        "fase": "Panen",
        "conditions": [("N", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "rendah"
    },

    {
        "id": 42,
        "fase": "Panen",
        "conditions": [("P", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "rendah"
    },

    {
        "id": 43,
        "fase": "Panen",
        "conditions": [("PH", "asam")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    {
        "id": 44,
        "fase": "Panen",
        "conditions": [("PH", "basa")],
        "pupuk": "NPK",
        "output": "rendah"
    },

    {
        "id": 45,
        "fase": "Panen",
        "conditions": [("N", "tinggi"), ("P", "tinggi"), ("K", "tinggi")],
        "pupuk": "NPK",
        "output": "rendah"
    },

    # =====================================================
    # FASE PASCA PANEN (R46-R54)
    # =====================================================

    {
        "id": 46,
        "fase": "Pascapanen",
        "conditions": [("N", "rendah")],
        "pupuk": "Urea",
        "output": "tinggi"
    },

    {
        "id": 47,
        "fase": "Pascapanen",
        "conditions": [("P", "rendah")],
        "pupuk": "SP36",
        "output": "tinggi"
    },

    {
        "id": 48,
        "fase": "Pascapanen",
        "conditions": [("K", "rendah")],
        "pupuk": "KCl",
        "output": "tinggi"
    },

    {
        "id": 49,
        "fase": "Pascapanen",
        "conditions": [("N", "rendah"), ("P", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 50,
        "fase": "Pascapanen",
        "conditions": [("N", "rendah"), ("K", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 51,
        "fase": "Pascapanen",
        "conditions": [("P", "rendah"), ("K", "rendah")],
        "pupuk": "NPK",
        "output": "tinggi"
    },

    {
        "id": 52,
        "fase": "Pascapanen",
        "conditions": [("PH", "asam")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    {
        "id": 53,
        "fase": "Pascapanen",
        "conditions": [("PH", "normal")],
        "pupuk": "NPK",
        "output": "sedang"
    },

    {
        "id": 54,
        "fase": "Pascapanen",
        "conditions": [("N", "sedang"), ("P", "sedang"), ("K", "sedang")],
        "pupuk": "NPK",
        "output": "sedang"
    }
]