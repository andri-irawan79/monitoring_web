"""Pengaturan pytest bersama: path backend dan riset/, serta env aman untuk impor modul tanpa basis data."""
import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BACKEND_ROOT.parent
for p in (BACKEND_ROOT, REPO_ROOT / "riset"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Nilai tiruan agar `database.connection` dapat diimpor pada uji yang tidak menyentuh basis data.
for kunci, nilai in {"DB_HOST": "localhost", "DB_PORT": "5432", "DB_NAME": "uji", "DB_USER": "uji", "DB_PASSWORD": "uji",
                     "JWT_SECRET_KEY": "kunci-uji-minimal-32-byte-untuk-pengujian-saja",
                     "SIMULATOR_API_KEY": "kunci-simulator-uji"}.items():
    os.environ.setdefault(kunci, nilai)
