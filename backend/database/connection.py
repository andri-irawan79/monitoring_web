
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Membaca konfigurasi dari backend/.env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Memastikan seluruh konfigurasi wajib tersedia
required_config = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}

missing_config = [
    key for key, value in required_config.items()
    if not value
]

if missing_config:
    raise RuntimeError(
        "Konfigurasi database belum lengkap: "
        + ", ".join(missing_config)
        + ". Periksa file backend/.env."
    )

# URL.create menangani karakter khusus pada username/password
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

# Gunakan UTF-8 untuk komunikasi dengan PostgreSQL
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "client_encoding": "UTF8"
    },
    pool_pre_ping=True,
)
