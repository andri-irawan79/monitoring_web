"""Manage simulator subprocesses started from the website."""

import subprocess
import sys
import threading
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SIMULATOR_SCRIPT = REPOSITORY_ROOT / "backend" / "simulator" / "simulator.py"
LOG_DIRECTORY = REPOSITORY_ROOT / "backend" / "logs"

_processes = {}
_log_handles = {}
_process_lock = threading.Lock()


def start_simulator_process(session_id: str) -> subprocess.Popen:
    """Start one simulator process and write its output to a per-session log."""
    if not SIMULATOR_SCRIPT.is_file():
        raise FileNotFoundError(
            f"File simulator tidak ditemukan: {SIMULATOR_SCRIPT}"
        )

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIRECTORY / f"simulator-{session_id}.log"
    log_handle = log_path.open("a", encoding="utf-8", buffering=1)

    try:
        process = subprocess.Popen(
            [
                sys.executable,
                str(SIMULATOR_SCRIPT),
                "--session-id",
                session_id,
            ],
            cwd=str(REPOSITORY_ROOT),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
        )
    except Exception:
        log_handle.close()
        raise

    with _process_lock:
        _processes[session_id] = process
        _log_handles[session_id] = log_handle

    return process


def stop_simulator_process(session_id: str, timeout_seconds: float = 5.0) -> bool:
    """Stop a process started by this running API instance."""
    with _process_lock:
        process = _processes.get(session_id)
        log_handle = _log_handles.get(session_id)

    if process is None:
        return False

    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=timeout_seconds)

    with _process_lock:
        _processes.pop(session_id, None)
        _log_handles.pop(session_id, None)

    if log_handle and not log_handle.closed:
        log_handle.close()

    return True
