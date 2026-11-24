"""
Simulator data monitoring durian melalui HTTP REST API.

Program ini memilih 365 record secara terstratifikasi dari enam label
tanaman buah pada Crop_recommendationV2.csv, kemudian mengirimkannya ke FastAPI.
Tanpa --session-id, skrip membuat sesi Git Bash
sendiri; website meneruskan ID sesi yang sudah dibuat oleh backend.
MQTT tidak digunakan dalam alur simulasi ini.
"""

import argparse
import json
import os
import sys
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
FRUIT_LABELS = (
    "banana",
    "coconut",
    "mango",
    "orange",
    "papaya",
    "pomegranate",
)
SAMPLE_QUOTAS = {
    "banana": 61,
    "coconut": 61,
    "mango": 61,
    "orange": 61,
    "papaya": 61,
    "pomegranate": 60,
}
EXPECTED_FRUIT_ROWS = 600
INTERVAL_SECONDS = float(os.getenv("SIMULATOR_INTERVAL_SECONDS", "5"))
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
    "soil_moisture",
    "label",
}

SCENARIO_CSV_PATH = BASE_DIR / "riset" / "skenario_uji.csv"
SCENARIO_EXPECTED_COUNT = 55
SCENARIO_RECORD_TARGET = 51
SCENARIO_INVALID_FIELDS = {
    "SK-52": "nitrogen",
    "SK-53": "ph",
    "SK-54": "soil_moisture",
    "SK-55": "phosphorus",
}
SCENARIO_REQUIRED_COLUMNS = {
    "id", "kelompok", "tujuan", "jenis", "N", "P", "K", "ph",
    "soil_moisture", "temperature", "humidity", "rainfall",
}


def stratified_sample(
    dataframe: pd.DataFrame,
    sample_size: int = RECORD_LIMIT,
    label_column: str = "label",
    random_seed: int = SAMPLE_SEED,
) -> pd.DataFrame:
    """
    Ambil sampel terstratifikasi mengikuti proyek ZIP acuan.

    Dataset yang diterima fungsi ini sudah difilter menjadi enam label buah.
    Kuota tetap: banana/coconut/mango/orange/papaya masing-masing 61 dan
    pomegranate 60. Setiap kelompok di-sample dengan seed yang sama,
    lalu seluruh sampel diacak sekali lagi dengan seed yang sama.
    """
    if label_column not in dataframe.columns:
        raise ValueError(
            f"Kolom strata '{label_column}' tidak ditemukan."
        )
    if sample_size != RECORD_LIMIT:
        raise ValueError(
            f"Ukuran sampel mengikuti proyek acuan dan harus {RECORD_LIMIT}."
        )

    actual_labels = set(dataframe[label_column].dropna().astype(str).unique())
    expected_labels = set(FRUIT_LABELS)
    if actual_labels != expected_labels:
        missing = sorted(expected_labels - actual_labels)
        unexpected = sorted(actual_labels - expected_labels)
        raise ValueError(
            "Data sampling harus berisi tepat enam label buah. "
            f"Label kurang: {missing or '-'}; label tidak sesuai: {unexpected or '-'}."
        )

    if len(dataframe) != EXPECTED_FRUIT_ROWS:
        raise ValueError(
            f"Enam label buah harus berjumlah {EXPECTED_FRUIT_ROWS} baris; "
            f"ditemukan {len(dataframe)}."
        )

    sampled_groups = []
    for label, group in dataframe.groupby(label_column):
        quota = SAMPLE_QUOTAS[str(label)]
        if len(group) < quota:
            raise ValueError(
                f"Label '{label}' memiliki {len(group)} baris; "
                f"minimal {quota} diperlukan."
            )
        # Sama dengan siapkan_data.py pada proyek ZIP: seed yang sama
        # digunakan untuk setiap kelompok, bukan seed berbeda per kelompok.
        sampled_groups.append(
            group.sample(n=quota, random_state=random_seed)
        )

    sampled = (
        pd.concat(sampled_groups)
        .sample(frac=1.0, random_state=random_seed)
        .reset_index(drop=True)
    )

    if len(sampled) != RECORD_LIMIT:
        raise RuntimeError(
            f"Hasil stratified sampling harus {RECORD_LIMIT} baris, "
            f"ditemukan {len(sampled)}."
        )
    return sampled


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

    print("\nMasuk untuk mengaitkan data simulasi dengan akun Anda.")
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


def send_record(payload: dict, accept_validation_error: bool = False) -> dict:
    """Send one record; scenario mode may inspect an expected HTTP 422 response."""

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

            # Mode uji perlu membaca respons validasi 422 sebagai hasil kasus,
            # bukan sebagai kegagalan transport. Respons 4xx lainnya tetap gagal.
            if accept_validation_error and error.code == 422:
                try:
                    parsed_body = json.loads(error_body)
                except json.JSONDecodeError:
                    parsed_body = {"raw": error_body}
                return {"status_code": error.code, "body": parsed_body}

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

    # Samakan ruang sampel dengan proyek acuan: enam kategori buah.
    fruit_dataframe = dataframe[
        dataframe["label"].isin(FRUIT_LABELS)
    ].copy()

    if len(fruit_dataframe) != EXPECTED_FRUIT_ROWS:
        distribution = (
            fruit_dataframe["label"].value_counts().sort_index().to_dict()
        )
        raise ValueError(
            "Dataset hasil filter enam tanaman buah harus berisi "
            f"{EXPECTED_FRUIT_ROWS} baris; ditemukan {len(fruit_dataframe)}. "
            f"Distribusi aktual: {distribution}"
        )

    return stratified_sample(
        fruit_dataframe,
        sample_size=RECORD_LIMIT,
        label_column="label",
        random_seed=SAMPLE_SEED,
    )


def load_scenarios(csv_path: Path = SCENARIO_CSV_PATH) -> pd.DataFrame:
    """Load and structurally validate the 55 reference API-validation scenarios."""
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Berkas skenario tidak ditemukan: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    missing_columns = SCENARIO_REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(
            "Kolom skenario tidak lengkap: " + ", ".join(sorted(missing_columns))
        )

    if len(dataframe) != SCENARIO_EXPECTED_COUNT:
        raise ValueError(
            f"Skenario harus berisi {SCENARIO_EXPECTED_COUNT} baris; "
            f"ditemukan {len(dataframe)}."
        )
    if dataframe["id"].astype(str).duplicated().any():
        raise ValueError("ID skenario harus unik.")

    types = dataframe["jenis"].astype(str).str.strip()
    valid_count = int((types == "valid").sum())
    invalid_count = int((types == "tidak_valid").sum())
    if valid_count != SCENARIO_RECORD_TARGET or invalid_count != 4:
        raise ValueError(
            "Komposisi skenario harus 51 valid dan 4 tidak_valid; "
            f"ditemukan {valid_count} valid dan {invalid_count} tidak_valid."
        )

    invalid_ids = set(dataframe.loc[types == "tidak_valid", "id"].astype(str))
    if invalid_ids != set(SCENARIO_INVALID_FIELDS):
        raise ValueError(
            "Daftar skenario tidak valid tidak sesuai dengan acuan: "
            f"{sorted(invalid_ids)}"
        )

    valid_rows = dataframe.loc[types == "valid"]
    numeric_columns = [
        "N", "P", "K", "ph", "soil_moisture",
        "temperature", "humidity", "rainfall",
    ]
    if valid_rows[numeric_columns].isna().any().any():
        raise ValueError("Skenario berstatus valid tidak boleh memiliki nilai kosong.")

    return dataframe


def _scenario_number(value, integer: bool = False):
    """Convert pandas values to JSON-safe numbers, preserving blank cells as null."""
    if pd.isna(value):
        return None
    if integer:
        return int(value)
    return round(float(value), 2)


def build_scenario_payload(
    row,
    session_id: str = None,
    session_record_number: int = None,
    scenario_index: int = 0,
) -> dict:
    """Translate a CSV row to the PATCH monitoring schema.

    Only valid cases receive session metadata. Invalid cases are rejected by
    Pydantic before the monitoring route can persist or count them.
    """
    payload = {
        "nitrogen": _scenario_number(row["N"], integer=True),
        "phosphorus": _scenario_number(row["P"], integer=True),
        "potassium": _scenario_number(row["K"], integer=True),
        "temperature": _scenario_number(row["temperature"]),
        "humidity": _scenario_number(row["humidity"]),
        "ph": _scenario_number(row["ph"]),
        "soil_moisture": _scenario_number(row["soil_moisture"]),
        "rainfall": _scenario_number(row["rainfall"]),
        "simulation_date": (
            START_DATE + timedelta(days=scenario_index)
        ).isoformat(),
    }

    if str(row["jenis"]).strip() == "valid":
        if not session_id or session_record_number is None:
            raise ValueError("Skenario valid wajib memiliki ID sesi dan nomor record.")
        payload["simulation_session_id"] = session_id
        payload["session_record_number"] = session_record_number

    return payload


def _validation_error_fields(response_body: dict) -> set[str]:
    """Extract rejected request fields from a FastAPI/Pydantic 422 response."""
    detail = response_body.get("detail", [])
    fields = set()
    if isinstance(detail, list):
        for issue in detail:
            if isinstance(issue, dict):
                location = issue.get("loc") or []
                if location:
                    fields.add(str(location[-1]))
    elif isinstance(detail, dict):
        location = detail.get("loc") or []
        if location:
            fields.add(str(location[-1]))
        if detail.get("field"):
            fields.add(str(detail["field"]))
    return fields


def create_scenario_session(access_token: str) -> str:
    """Create an authenticated, 51-record session reserved for scenario testing."""
    result = _request_json(
        f"{MONITORING_BASE_URL}/sessions/scenario/start",
        {},
        access_token=access_token,
        include_simulator_key=False,
    )
    session = result.get("session") or {}
    session_id = session.get("id")
    target_count = session.get("target_count")
    if not session_id:
        raise RuntimeError("API tidak mengembalikan ID sesi skenario.")
    if target_count != SCENARIO_RECORD_TARGET:
        raise RuntimeError(
            "Target sesi skenario tidak sesuai: "
            f"diharapkan {SCENARIO_RECORD_TARGET}, diterima {target_count}."
        )
    return session_id


def run_scenario_mode(csv_path: Path = SCENARIO_CSV_PATH, interval_seconds: float = 0.0) -> bool:
    """Execute 55 API validation cases: 51 stored records and 4 expected rejections."""
    if interval_seconds < 0:
        raise ValueError("Interval skenario tidak boleh negatif.")

    dataframe = load_scenarios(csv_path)
    access_token = authenticate_terminal_user()
    session_id = create_scenario_session(access_token)

    valid_record_number = 0
    valid_passed = 0
    invalid_passed = 0
    all_passed = True
    final_status = "failed"
    final_error = None

    print("=" * 72)
    print("MODE UJI API - 55 SKENARIO")
    print("=" * 72)
    print(f"Berkas skenario : {Path(csv_path)}")
    print(f"Endpoint        : {API_URL}")
    print(f"ID sesi         : {session_id}")
    print(f"Target tersimpan: {SCENARIO_RECORD_TARGET}")
    print("Ekspektasi      : 51 HTTP 200 dan 4 HTTP 422 dengan field yang tepat")
    print("=" * 72)

    try:
        for scenario_index, (_, row) in enumerate(dataframe.iterrows()):
            scenario_id = str(row["id"])
            is_valid = str(row["jenis"]).strip() == "valid"

            if is_valid:
                valid_record_number += 1

            payload = build_scenario_payload(
                row,
                session_id=session_id if is_valid else None,
                session_record_number=valid_record_number if is_valid else None,
                scenario_index=scenario_index,
            )

            print(f"\n[{scenario_id}] {row['tujuan']}")
            print("Data yang dikirim:")
            print(json.dumps(payload, indent=2, ensure_ascii=False))

            try:
                response = send_record(
                    payload,
                    accept_validation_error=not is_valid,
                )
            except Exception as error:
                all_passed = False
                print(f"HASIL: GAGAL mengirim skenario: {error}")
                if interval_seconds:
                    time.sleep(interval_seconds)
                continue

            status_code = response["status_code"]
            response_body = response.get("body") or {}

            if is_valid:
                case_passed = status_code == 200 and response_body.get("id") is not None
                if case_passed:
                    valid_passed += 1
                    print(
                        f"HASIL: LULUS (HTTP {status_code}), "
                        f"ID monitoring={response_body.get('id')}, "
                        f"record sesi={valid_record_number}/{SCENARIO_RECORD_TARGET}"
                    )
                else:
                    all_passed = False
                    print(
                        f"HASIL: GAGAL; ekspektasi HTTP 200 dan ID monitoring, "
                        f"diterima HTTP {status_code}: "
                        f"{json.dumps(response_body, ensure_ascii=False)}"
                    )
            else:
                expected_field = SCENARIO_INVALID_FIELDS[scenario_id]
                rejected_fields = _validation_error_fields(response_body)
                case_passed = status_code == 422 and expected_field in rejected_fields
                if case_passed:
                    invalid_passed += 1
                    print(
                        f"HASIL: LULUS (HTTP 422), field '{expected_field}' ditolak."
                    )
                else:
                    all_passed = False
                    print(
                        f"HASIL: GAGAL; ekspektasi HTTP 422 pada field "
                        f"'{expected_field}', diterima HTTP {status_code} "
                        f"dengan field {sorted(rejected_fields)}."
                    )

            if interval_seconds and scenario_index < len(dataframe) - 1:
                time.sleep(interval_seconds)

        if valid_passed != SCENARIO_RECORD_TARGET or invalid_passed != 4:
            all_passed = False

        final_status = "completed" if all_passed else "failed"
        if not all_passed:
            final_error = (
                f"Hasil skenario tidak sesuai: {valid_passed}/51 valid dan "
                f"{invalid_passed}/4 tidak valid."
            )

    except KeyboardInterrupt:
        final_status = "stopped"
        final_error = "Pengujian dihentikan melalui Ctrl+C."
        all_passed = False
        print("\nPengujian dihentikan melalui Ctrl+C.")

    except Exception as error:
        final_status = "failed"
        final_error = error
        all_passed = False
        print(f"\nPENGUJIAN DIHENTIKAN: {error}")

    finally:
        finish_session(session_id, final_status, final_error)

    print("\n" + "=" * 72)
    print("RINGKASAN MODE UJI")
    print(f"Skenario valid   : {valid_passed}/{SCENARIO_RECORD_TARGET}")
    print(f"Skenario ditolak : {invalid_passed}/4")
    print(f"Status sesi      : {final_status}")
    print(
        "HASIL AKHIR      : "
        + ("SESUAI HARAPAN (55/55)" if all_passed else "TIDAK SESUAI HARAPAN")
    )
    print("=" * 72)
    return all_passed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulator monitoring tanah melalui HTTP REST API."
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="ID sesi 365 data yang dibuat backend saat simulator dimulai dari website.",
    )
    parser.add_argument(
        "--uji",
        nargs="?",
        const=str(SCENARIO_CSV_PATH),
        default=None,
        metavar="CSV",
        help="Jalankan mode uji 55 skenario; default menggunakan riset/skenario_uji.csv.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=None,
        help="Jeda antar pengiriman dalam detik (mode uji default 0 detik).",
    )
    args = parser.parse_args()

    if args.uji is not None:
        if args.session_id:
            parser.error("--session-id tidak dapat digabungkan dengan --uji.")
        interval_seconds = 0.0 if args.interval is None else args.interval
        if interval_seconds < 0:
            parser.error("--interval tidak boleh negatif.")
        if not run_scenario_mode(Path(args.uji), interval_seconds):
            sys.exit(1)
        return

    interval_seconds = INTERVAL_SECONDS if args.interval is None else args.interval
    if interval_seconds < 0:
        raise ValueError("Interval simulasi tidak boleh negatif.")

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
    print("Filter label  : " + ", ".join(FRUIT_LABELS))
    print("Baris buah    : " + str(EXPECTED_FRUIT_ROWS))
    print("Metode sampel : Stratified random sampling (kuota tetap)")
    print(f"Random seed   : {SAMPLE_SEED}")
    print("Distribusi sampel:")
    print(dataframe["label"].value_counts().sort_index().to_string())
    print(f"Interval      : {interval_seconds} detik")
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
                "soil_moisture": round(float(row["soil_moisture"]), 2),
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
                time.sleep(interval_seconds)

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
