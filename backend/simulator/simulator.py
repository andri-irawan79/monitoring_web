"""
Simulator data monitoring durian melalui HTTP REST API.

Program ini membaca 365 record pertama dari Crop_recommendationV2.csv,
kemudian mengirimkannya langsung ke endpoint POST FastAPI. MQTT tidak
digunakan dalam alur simulasi ini.
"""

import json
import os
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE_DIR / "Crop_recommendationV2.csv"

API_URL = os.getenv(
    "MONITORING_API_URL",
    "http://127.0.0.1:8000/monitoring/"
)
API_URL = API_URL.rstrip("/") + "/"

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


def send_record(payload: dict) -> dict:
    """Kirim satu record ke FastAPI dan kembalikan respons JSON."""

    body = json.dumps(payload).encode("utf-8")
    request = Request(
        API_URL,
        data=body,
        headers={"Content-Type": "application/json"},
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

            last_error = (
                f"HTTP {error.code}: {error_body}"
            )

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


def main() -> None:
    if INTERVAL_SECONDS < 0:
        raise ValueError(
            "SIMULATOR_INTERVAL_SECONDS tidak boleh negatif."
        )

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATASET_PATH}"
        )

    dataframe = pd.read_csv(DATASET_PATH)

    missing_columns = REQUIRED_COLUMNS.difference(
        dataframe.columns
    )
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

    dataframe = stratified_sample(
        dataframe,
        sample_size=RECORD_LIMIT,
        label_column="label",
        random_seed=SAMPLE_SEED,
    )

    print("=" * 72)
    print("SIMULATOR MONITORING DURIAN - HTTP REST API")
    print("=" * 72)
    print(f"Dataset       : {DATASET_PATH}")
    print(f"Endpoint      : {API_URL}")
    print(f"Jumlah record : {len(dataframe)}")
    print(f"Metode sampel : Stratified sampling berdasarkan label")
    print(f"Random seed   : {SAMPLE_SEED}")
    print("Distribusi sampel:")
    print(dataframe["label"].value_counts().sort_index().to_string())
    print(f"Interval      : {INTERVAL_SECONDS} detik")
    print(f"Tanggal awal  : {START_DATE.isoformat()}")
    print("Metode        : HTTP POST dengan payload JSON")
    print("Kolom label hanya untuk stratifikasi; tidak dikirim ke API.")
    print("=" * 72)

    success_count = 0

    for index, row in dataframe.iterrows():
        simulation_date = (
            START_DATE + timedelta(days=success_count)
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
        }

        print("\n" + "=" * 72)
        print(
            f"Mengirim record dataset ke-{index + 1} "
            f"untuk tanggal simulasi {simulation_date}"
        )
        print("Data yang dikirim:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        try:
            response = send_record(payload)
        except RuntimeError as error:
            print(f"\nPENGIRIMAN DIHENTIKAN: {error}")
            print(
                "Record berikutnya tidak dikirim agar "
                "kegagalan pengiriman tidak tersembunyi."
            )
            raise

        success_count += 1
        response_body = response["body"]

        print("\nRespons FastAPI:")
        print(
            json.dumps(
                response_body,
                indent=2,
                ensure_ascii=False
            )
        )
        print(
            f"Status HTTP   : {response['status_code']}"
        )
        print(
            f"ID database   : {response_body.get('id', '-')}"
        )
        print(
            f"Status        : "
            f"{response_body.get('message', 'Data diterima')}"
        )
        print(
            f"Total terkirim: {success_count}/{len(dataframe)}"
        )
        print("=" * 72)

        if success_count < len(dataframe):
            time.sleep(INTERVAL_SECONDS)

    print("\nSIMULASI SELESAI")
    print(
        f"Total record berhasil dikirim: "
        f"{success_count}/{len(dataframe)}"
    )


if __name__ == "__main__":
    main()
