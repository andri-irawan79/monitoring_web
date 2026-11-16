"""
Simulator data monitoring durian melalui HTTP REST API.

Program ini membaca 365 record dari Crop_recommendationV2.csv dan
mengirimkannya ke FastAPI. Tanpa --session-id, skrip membuat sesi Git Bash
sendiri; website meneruskan ID sesi yang sudah dibuat oleh backend.
MQTT tidak digunakan dalam alur simulasi ini.
"""

import argparse
import json
import os
import time
from datetime import date, timedelta
from getpass import getpass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / "backend" / ".env")
configured_dataset = os.getenv("SIMULATOR_DATASET_PATH")
if configured_dataset:
    DATASET_PATH = Path(configured_dataset).expanduser()
    if not DATASET_PATH.is_absolute():
        DATASET_PATH = BASE_DIR / DATASET_PATH
else:
    preferred_dataset = BASE_DIR / "Crop_recommendationV2.csv"
    fallback_dataset = BASE_DIR / "Crop_recommendation.csv"
    DATASET_PATH = (
        preferred_dataset
        if preferred_dataset.exists()
        else fallback_dataset
    )

API_URL = os.getenv(
    "MONITORING_API_URL",
    "http://127.0.0.1:8000/monitoring/"
)
API_URL = API_URL.rstrip("/") + "/"
MONITORING_BASE_URL = API_URL.rstrip("/")
API_ROOT = MONITORING_BASE_URL.rsplit("/monitoring", 1)[0]
SIMULATOR_API_KEY = os.getenv(
    "SIMULATOR_API_KEY",
    "local-simulator-key-change-before-deployment"
)

RECORD_LIMIT = 365
SAMPLE_SEED = 42
INTERVAL_SECONDS = float(os.getenv("SIMULATOR_INTERVAL_SECONDS", "2"))
START_DATE = date.fromisoformat(
    os.getenv("SIMULATOR_START_DATE", "2026-01-01")
)
REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

REQUIRED_COLUMNS = {
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "label",
}


def stratified_sample(
    dataframe: pd.DataFrame,
    sample_size: int,
    label_column: str = "label",
    random_seed: int = SAMPLE_SEED,
) -> pd.DataFrame:
    """
    Memilih sampel proporsional berdasarkan label tanaman.

    Kolom label hanya digunakan sebagai strata agar urutan data yang
    berkelompok menurut tanaman tidak menyebabkan sampel hanya memuat
    sebagian label. Label tidak dikirim ke backend dan tidak menjadi
    variabel monitoring atau input Fuzzy Tsukamoto.
    """
    if label_column not in dataframe.columns:
        raise ValueError(
            f"Kolom strata '{label_column}' tidak ditemukan."
        )
    if sample_size <= 0 or sample_size > len(dataframe):
        raise ValueError("Ukuran sampel harus antara 1 dan jumlah record.")

    grouped = [
        (str(label), group)
        for label, group in dataframe.groupby(label_column, sort=True)
    ]
    if not grouped:
        raise ValueError("Tidak ditemukan kelompok label untuk sampling.")

    exact_quotas = {
        label: sample_size * len(group) / len(dataframe)
        for label, group in grouped
    }
    quotas = {
        label: int(value)
        for label, value in exact_quotas.items()
    }

    remainder = sample_size - sum(quotas.values())
    order = sorted(
        exact_quotas,
        key=lambda label: (-(exact_quotas[label] - quotas[label]), label)
    )
    for label in order[:remainder]:
        quotas[label] += 1

    sampled_groups = []
    for index, (label, group) in enumerate(grouped):
        quota = quotas[label]
        if quota > len(group):
            raise ValueError(
                f"Kuota sampel untuk label '{label}' melebihi jumlah record."
            )
        sampled_groups.append(
            group.sample(
                n=quota,
                replace=False,
                random_state=random_seed + index,
            )
        )

    sampled = pd.concat(sampled_groups, ignore_index=True)
    return (
        sampled.sample(frac=1, random_state=random_seed)
        .reset_index(drop=True)
    )


def _request_json(
    url: str,
    payload: dict,
    access_token: str = None,
    include_simulator_key: bool = True,
) -> dict:
    """Send one JSON control request with optional account authentication."""
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if include_simulator_key:
        headers["X-Simulator-Key"] = SIMULATOR_API_KEY
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    request = Request(
        url,
        data=body,
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else {}
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {error_body}") from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"Gagal menghubungi API: {error}") from error


def authenticate_terminal_user() -> str:
    """Sign in as the account that owns records sent by this Git Bash session."""
    configured_token = os.getenv("SIMULATOR_ACCESS_TOKEN", "").strip()
    if configured_token:
        return configured_token

    print("\\nMasuk untuk mengaitkan data simulasi dengan akun Anda.")
    email = input("Email akun: ").strip()
    if not email:
        raise ValueError("Email akun wajib diisi untuk menjalankan simulasi Git Bash.")

    password = getpass("Kata sandi: ")
    if not password:
        raise ValueError("Kata sandi wajib diisi untuk menjalankan simulasi Git Bash.")

    result = _request_json(
        f"{API_ROOT}/auth/login",
        {"email": email, "password": password},
        include_simulator_key=False,
    )
    access_token = result.get("access_token")
    if not access_token:
        raise RuntimeError("Login berhasil dipanggil, tetapi token akun tidak diterima.")
    return access_token


def create_terminal_session(access_token: str) -> str:
    """Create a new user-owned session when the script is launched manually."""
    result = _request_json(
        f"{MONITORING_BASE_URL}/sessions/terminal/start",
        {},
        access_token=access_token,
        include_simulator_key=False,
    )
    session_id = (result.get("session") or {}).get("id")
    if not session_id:
        raise RuntimeError("API tidak mengembalikan ID sesi simulasi.")
    return session_id


def finish_session(session_id: str, final_status: str, error_message=None) -> None:
    """Report completion, Ctrl+C, or failure to the backend."""
    try:
        _request_json(
            f"{MONITORING_BASE_URL}/sessions/{session_id}/finish",
            {
                "status": final_status,
                "error_message": str(error_message)[:1000] if error_message else None,
            },
        )
    except Exception as error:
        print(f"Peringatan: status akhir sesi tidak berhasil dikirim: {error}")


def send_record(payload: dict) -> dict:
    """Kirim satu record ke FastAPI dan kembalikan respons JSON."""

    body = json.dumps(payload).encode("utf-8")
    request = Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Simulator-Key": SIMULATOR_API_KEY,
        },
        method="POST",
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(
                request,
                timeout=REQUEST_TIMEOUT_SECONDS
            ) as response:
                response_body = response.read().decode("utf-8")
                result = (
                    json.loads(response_body)
                    if response_body
                    else {}
                )
                return {
                    "status_code": response.status,
                    "body": result,
                }

        except HTTPError as error:
            error_body = error.read().decode(
                "utf-8",
                errors="replace"
            )

            # Kesalahan validasi/request tidak akan membaik dengan retry.
            if 400 <= error.code < 500 and error.code != 429:
                raise RuntimeError(
                    f"HTTP {error.code}: {error_body}"
                ) from error

            last_error = f"HTTP {error.code}: {error_body}"

        except (URLError, TimeoutError) as error:
            last_error = str(error)

        if attempt < MAX_RETRIES:
            delay = RETRY_DELAY_SECONDS * attempt
            print(
                f"Peringatan: pengiriman gagal "
                f"(percobaan {attempt}/{MAX_RETRIES}). "
                f"Mencoba kembali dalam {delay} detik. "
                f"Detail: {last_error}"
            )
            time.sleep(delay)

    raise RuntimeError(
        f"Data gagal dikirim setelah {MAX_RETRIES} percobaan: "
        f"{last_error}"
    )


def load_sample() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATASET_PATH}"
        )

    dataframe = pd.read_csv(DATASET_PATH)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(
            "Kolom dataset tidak lengkap: "
            + ", ".join(sorted(missing_columns))
        )

    if len(dataframe) < RECORD_LIMIT:
        raise ValueError(
            f"Dataset hanya memiliki {len(dataframe)} record; "
            f"minimal {RECORD_LIMIT} record diperlukan."
        )

    return stratified_sample(
        dataframe,
        sample_size=RECORD_LIMIT,
        label_column="label",
        random_seed=SAMPLE_SEED,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulator monitoring tanah berbasis data CSV."
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="ID sesi yang dibuat backend saat simulator dimulai dari website.",
    )
    args = parser.parse_args()

    if INTERVAL_SECONDS < 0:
        raise ValueError("SIMULATOR_INTERVAL_SECONDS tidak boleh negatif.")

    dataframe = load_sample()
    access_token = None
    if args.session_id:
        # Website-started sessions already carry their authenticated owner.
        session_id = args.session_id
    else:
        # Git Bash sessions must explicitly authenticate the account owner.
        access_token = authenticate_terminal_user()
        session_id = create_terminal_session(access_token)

    print("=" * 72)
    print("SIMULATOR MONITORING DURIAN - HTTP REST API")
    print("=" * 72)
    print(f"Dataset       : {DATASET_PATH}")
    print(f"Endpoint      : {API_URL}")
    print(f"ID sesi       : {session_id}")
    print(f"Jumlah record : {len(dataframe)}")
    print("Metode sampel : Stratified sampling berdasarkan label")
    print(f"Random seed   : {SAMPLE_SEED}")
    print("Distribusi sampel:")
    print(dataframe["label"].value_counts().sort_index().to_string())
    print(f"Interval      : {INTERVAL_SECONDS} detik")
    print(f"Tanggal awal  : {START_DATE.isoformat()}")
    print("Metode        : HTTP POST dengan payload JSON")
    print("Label hanya untuk stratifikasi; tidak dikirim ke API.")
    print("=" * 72)

    success_count = 0
    final_status = "failed"
    final_error = None

    try:
        for record_number, (_, row) in enumerate(
            dataframe.iterrows(),
            start=1,
        ):
            simulation_date = (
                START_DATE + timedelta(days=record_number - 1)
            ).isoformat()

            payload = {
                "nitrogen": int(row["N"]),
                "phosphorus": int(row["P"]),
                "potassium": int(row["K"]),
                "temperature": round(float(row["temperature"]), 2),
                "humidity": round(float(row["humidity"]), 2),
                "ph": round(float(row["ph"]), 2),
                "rainfall": round(float(row["rainfall"]), 2),
                "simulation_date": simulation_date,
                "simulation_session_id": session_id,
                "session_record_number": record_number,
            }

            print("\n" + "=" * 72)
            print(
                f"Mengirim record sesi {record_number}/{len(dataframe)} "
                f"untuk tanggal simulasi {simulation_date}"
            )
            print("Data yang dikirim:")
            print(json.dumps(payload, indent=2, ensure_ascii=False))

            response = send_record(payload)
            response_body = response["body"]
            success_count = max(
                success_count,
                int(response_body.get("session_received_count") or record_number),
            )

            print("\nRespons FastAPI:")
            print(json.dumps(response_body, indent=2, ensure_ascii=False))
            print(f"Status HTTP   : {response['status_code']}")
            print(f"ID database   : {response_body.get('id', '-')}")
            print(f"Status        : {response_body.get('message', 'Data diterima')}")
            print(
                f"Progres sesi  : "
                f"{success_count}/{response_body.get('session_target_count', RECORD_LIMIT)}"
            )
            print("=" * 72)

            if record_number < len(dataframe):
                time.sleep(INTERVAL_SECONDS)

        final_status = "completed"

    except KeyboardInterrupt:
        final_status = "stopped"
        print("\nSimulasi dihentikan melalui Ctrl+C.")

    except Exception as error:
        final_status = "failed"
        final_error = error
        print(f"\nPENGIRIMAN DIHENTIKAN: {error}")
        raise

    finally:
        finish_session(session_id, final_status, final_error)

    if final_status == "completed":
        print("\nSIMULASI SELESAI")
    print(
        f"Total record berhasil dikirim dalam sesi ini: "
        f"{success_count}/{RECORD_LIMIT}"
    )


if __name__ == "__main__":
    main()
