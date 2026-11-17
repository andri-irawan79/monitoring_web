import os
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import DateTime, func
from sqlalchemy.exc import IntegrityError

from auth import get_current_user, verify_simulator_key
from database.session import SessionLocal
from models.monitoring import Monitoring
from models.simulation_session import SimulationSession
from models.user import User
from schemas.monitoring import MonitoringCreate
from schemas.simulation_session import SimulationSessionFinish
from simulator_process import start_simulator_process, stop_simulator_process


router = APIRouter()

SIMULATOR_STATUS_TIMEOUT_SECONDS = float(
    os.getenv("SIMULATOR_STATUS_TIMEOUT_SECONDS", "8")
)
SIMULATOR_SESSION_TIMEOUT_SECONDS = float(
    os.getenv("SIMULATOR_SESSION_TIMEOUT_SECONDS", "45")
)
SIMULATOR_RECORD_TARGET = 365


def _session_payload(session):
    if session is None:
        return None

    target = max(1, int(session.target_count or SIMULATOR_RECORD_TARGET))
    received = int(session.received_count or 0)
    return {
        "id": session.id,
        "mode": session.mode,
        "status": session.status,
        "target_count": target,
        "received_count": received,
        "remaining_count": max(0, target - received),
        "progress_percent": round(min(100, received / target * 100), 1),
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "last_received_at": (
            session.last_received_at.isoformat()
            if session.last_received_at
            else None
        ),
        "finished_at": session.finished_at.isoformat() if session.finished_at else None,
        "error_message": session.error_message,
        "can_stop_from_website": (
            session.mode == "website"
            and session.status in ("starting", "running")
        ),
    }


def _create_session(db, mode, user_id):
    active = (
        db.query(SimulationSession)
        .filter(
            SimulationSession.user_id == user_id,
            SimulationSession.status.in_(("starting", "running"))
        )
        .with_for_update()
        .first()
    )
    if active is not None:
        activity_at = active.last_received_at or active.started_at
        age_seconds = (
            (datetime.utcnow() - activity_at).total_seconds()
            if activity_at
            else SIMULATOR_SESSION_TIMEOUT_SECONDS + 1
        )
        if age_seconds > SIMULATOR_SESSION_TIMEOUT_SECONDS:
            active.status = "failed"
            active.finished_at = datetime.utcnow()
            active.error_message = (
                "Sesi sebelumnya tidak menerima data baru dalam "
                f"{SIMULATOR_SESSION_TIMEOUT_SECONDS:g} detik."
            )
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Masih ada sesi simulasi yang berjalan. "
                    "Hentikan atau selesaikan sesi tersebut terlebih dahulu."
                ),
            )

    session = SimulationSession(
        id=str(uuid4()),
        user_id=user_id,
        mode=mode,
        status="running",
        target_count=SIMULATOR_RECORD_TARGET,
        received_count=0,
        started_at=datetime.utcnow(),
    )
    db.add(session)
    try:
        db.commit()
        db.refresh(session)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sesi simulasi lain baru saja dimulai. Hanya satu sesi yang dapat aktif.",
        ) from error
    return session


@router.get("/latest")
def latest_monitoring(current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    try:
        data = (
            db.query(Monitoring)
            .filter(Monitoring.user_id == current_user.id)
            .order_by(Monitoring.id.desc())
            .first()
        )

        if data is None:
            return None

        return {
            "id": data.id,
            "nitrogen": data.nitrogen,
            "phosphorus": data.phosphorus,
            "potassium": data.potassium,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall,
            "created_at": data.created_at,
            "simulation_date": data.simulation_date,
        }

    finally:
        db.close()


@router.get("/history")
def monitoring_history(current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    try:
        data = (
            db.query(Monitoring)
            .filter(Monitoring.user_id == current_user.id)
            .order_by(Monitoring.id.desc())
            .all()
        )

        return [
            {
                "id": row.id,
                "nitrogen": row.nitrogen,
                "phosphorus": row.phosphorus,
                "potassium": row.potassium,
                "temperature": row.temperature,
                "humidity": row.humidity,
                "ph": row.ph,
                "rainfall": row.rainfall,
                "created_at": row.created_at,
                "simulation_date": row.simulation_date,
            }
            for row in data
        ]

    finally:
        db.close()


@router.delete("/history")
def delete_monitoring_history(
    current_user: User = Depends(get_current_user),
):
    """Delete only the signed-in user's monitoring history."""
    db = SessionLocal()

    try:
        active_session = (
            db.query(SimulationSession.id)
            .filter(
                SimulationSession.user_id == current_user.id,
                SimulationSession.status.in_(("starting", "running")),
            )
            .first()
        )
        if active_session is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Riwayat belum dapat dihapus karena simulasi masih berjalan. "
                    "Hentikan atau selesaikan sesi simulasi terlebih dahulu."
                ),
            )

        monitoring_query = db.query(Monitoring).filter(
            Monitoring.user_id == current_user.id
        )
        deleted_count = monitoring_query.count()

        if deleted_count:
            monitoring_query.delete(synchronize_session=False)

        db.commit()
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": (
                f"{deleted_count} data riwayat monitoring berhasil dihapus."
                if deleted_count
                else "Tidak ada data riwayat monitoring untuk dihapus."
            ),
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/simulator-status")
def simulator_status(
    response: Response,
    current_user: User = Depends(get_current_user),
):
    """Legacy indicator: whether a monitoring record was recently received."""
    response.headers["Cache-Control"] = "no-store"
    db = SessionLocal()

    try:
        latest = (
            db.query(
                Monitoring.created_at,
                func.extract(
                    "epoch",
                    func.now().cast(DateTime(timezone=False)) - Monitoring.created_at
                ).label("age_seconds"),
            )
            .filter(Monitoring.user_id == current_user.id)
            .order_by(Monitoring.id.desc())
            .first()
        )

        last_received_at = latest[0] if latest else None
        age_seconds = (
            max(0.0, float(latest[1]))
            if latest and latest[1] is not None
            else None
        )
        active = (
            age_seconds is not None
            and age_seconds <= SIMULATOR_STATUS_TIMEOUT_SECONDS
        )

        return {
            "active": active,
            "last_received_at": (
                last_received_at.isoformat()
                if last_received_at
                else None
            ),
            "seconds_since_last_received": (
                round(age_seconds, 1)
                if age_seconds is not None
                else None
            ),
            "timeout_seconds": SIMULATOR_STATUS_TIMEOUT_SECONDS,
        }

    finally:
        db.close()


@router.get("/sessions/status")
def simulation_session_status(
    response: Response,
    current_user: User = Depends(get_current_user),
):
    """Return current/latest session and its per-session record progress."""
    response.headers["Cache-Control"] = "no-store"
    db = SessionLocal()

    try:
        session = (
            db.query(SimulationSession)
            .filter(SimulationSession.user_id == current_user.id)
            .order_by(SimulationSession.started_at.desc())
            .first()
        )

        if session and session.status in ("starting", "running"):
            activity_at = session.last_received_at or session.started_at
            age_seconds = (
                (datetime.utcnow() - activity_at).total_seconds()
                if activity_at
                else SIMULATOR_SESSION_TIMEOUT_SECONDS + 1
            )
            if age_seconds > SIMULATOR_SESSION_TIMEOUT_SECONDS:
                session.status = "failed"
                session.finished_at = datetime.utcnow()
                session.error_message = (
                    "Tidak ada data baru yang diterima dalam "
                    f"{SIMULATOR_SESSION_TIMEOUT_SECONDS:g} detik. "
                    "Periksa proses simulator dan koneksi API."
                )
                db.commit()

        is_active = bool(
            session and session.status in ("starting", "running")
        )
        return {
            "active": is_active,
            "timeout_seconds": SIMULATOR_SESSION_TIMEOUT_SECONDS,
            "session": _session_payload(session),
        }

    finally:
        db.close()


@router.post("/sessions/start")
def start_website_simulation(
    current_user: User = Depends(get_current_user),
):
    """Create a website-managed session and launch its Python child process."""
    db = SessionLocal()

    try:
        session = _create_session(db, "website", current_user.id)
        try:
            process = start_simulator_process(session.id)
            session.process_id = process.pid
            db.commit()
            db.refresh(session)
        except Exception as error:
            db.rollback()
            failed = (
                db.query(SimulationSession)
                .filter(SimulationSession.id == session.id)
                .first()
            )
            if failed:
                failed.status = "failed"
                failed.finished_at = datetime.utcnow()
                failed.error_message = str(error)[:1000]
                db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Simulator tidak dapat dijalankan: {error}",
            ) from error

        return {
            "message": "Simulator berhasil dijalankan dari website.",
            "session": _session_payload(session),
            "log_file": f"backend/logs/simulator-{session.id}.log",
        }

    finally:
        db.close()


@router.post("/sessions/terminal/start")
def start_terminal_simulation(
    current_user: User = Depends(get_current_user),
):
    """Create a session for a simulator launched manually from Git Bash."""
    db = SessionLocal()
    try:
        session = _create_session(db, "terminal", current_user.id)
        return {
            "message": "Sesi simulasi Git Bash berhasil dibuat.",
            "session": _session_payload(session),
        }
    finally:
        db.close()


@router.post("/sessions/{session_id}/stop")
def stop_website_simulation(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    db = SessionLocal()

    try:
        session = (
            db.query(SimulationSession)
            .filter(
                SimulationSession.id == session_id,
                SimulationSession.user_id == current_user.id,
            )
            .with_for_update()
            .first()
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Sesi simulasi tidak ditemukan.")
        if session.mode != "website":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Sesi ini dijalankan melalui Git Bash. "
                    "Hentikan dari terminal dengan menekan Ctrl+C."
                ),
            )
        if session.status not in ("starting", "running"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Sesi sudah berstatus {session.status}.",
            )

        process_stopped = stop_simulator_process(session_id)
        if not process_stopped:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Proses tidak tercatat pada instance server ini. "
                    "Jalankan ulang backend sebelum menggunakan kontrol stop."
                ),
            )

        session.status = "stopped"
        session.finished_at = datetime.utcnow()
        session.error_message = None
        db.commit()
        db.refresh(session)

        return {
            "message": "Simulasi website dihentikan.",
            "session": _session_payload(session),
        }

    finally:
        db.close()


@router.post("/sessions/{session_id}/finish")
def finish_simulation_session(
    session_id: str,
    payload: SimulationSessionFinish,
    simulator_authorized: bool = Depends(verify_simulator_key),
):
    """Finish a terminal- or website-managed session from the Python process."""
    db = SessionLocal()

    try:
        session = (
            db.query(SimulationSession)
            .filter(SimulationSession.id == session_id)
            .with_for_update()
            .first()
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Sesi simulasi tidak ditemukan.")

        if session.status in ("stopped", "failed"):
            return {
                "message": "Sesi sudah dihentikan atau gagal sebelumnya.",
                "session": _session_payload(session),
            }

        if payload.status == "completed" and session.received_count < session.target_count:
            session.status = "failed"
            session.error_message = (
                "Proses berakhir dengan status selesai sebelum seluruh "
                f"{session.target_count} record berhasil diterima."
            )
        else:
            session.status = payload.status
            session.error_message = payload.error_message

        session.finished_at = datetime.utcnow()
        db.commit()
        db.refresh(session)

        return {
            "message": "Status sesi simulasi berhasil diperbarui.",
            "session": _session_payload(session),
        }

    finally:
        db.close()


@router.post("/")
def create_monitoring(
    payload: MonitoringCreate,
    simulator_authorized: bool = Depends(verify_simulator_key)
):
    db = SessionLocal()

    try:
        if not payload.simulation_session_id:
            raise HTTPException(
                status_code=422,
                detail="Setiap data simulasi wajib menyertakan ID sesi milik akun.",
            )

        session = None
        if payload.simulation_session_id:
            if payload.session_record_number is None:
                raise HTTPException(
                    status_code=422,
                    detail="Nomor record wajib dikirim untuk data dalam sesi simulasi.",
                )

            session = (
                db.query(SimulationSession)
                .filter(SimulationSession.id == payload.simulation_session_id)
                .with_for_update()
                .first()
            )
            if session is None:
                raise HTTPException(status_code=404, detail="Sesi simulasi tidak ditemukan.")
            if session.user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Sesi simulasi belum terhubung dengan akun pengguna.",
                )

            if not 1 <= payload.session_record_number <= session.target_count:
                raise HTTPException(
                    status_code=422,
                    detail=f"Nomor record harus berada pada rentang 1 sampai {session.target_count}.",
                )

            # A repeated HTTP request after a lost response must not inflate
            # the session counter or create a second monitoring row.
            duplicate = (
                db.query(Monitoring)
                .filter(
                    Monitoring.simulation_session_id == session.id,
                    Monitoring.session_record_number == payload.session_record_number,
                )
                .first()
            )
            if duplicate is not None:
                db.commit()
                return {
                    "message": "Record sesi ini sudah pernah diterima.",
                    "id": duplicate.id,
                    "simulation_date": (
                        duplicate.simulation_date.isoformat()
                        if duplicate.simulation_date
                        else None
                    ),
                    "session_received_count": session.received_count,
                    "duplicate": True,
                }

            if session.status not in ("starting", "running"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Sesi simulasi tidak menerima data karena berstatus {session.status}.",
                )

        data = Monitoring(
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            temperature=payload.temperature,
            humidity=payload.humidity,
            ph=payload.ph,
            rainfall=payload.rainfall,
            simulation_date=payload.simulation_date,
            user_id=session.user_id,
            simulation_session_id=payload.simulation_session_id,
            session_record_number=payload.session_record_number,
        )

        db.add(data)

        if session is not None:
            session.received_count += 1
            session.last_received_at = datetime.utcnow()
            if session.received_count >= session.target_count:
                session.received_count = session.target_count
                session.status = "completed"
                session.finished_at = datetime.utcnow()

        db.commit()
        db.refresh(data)

        return {
            "message": "Data monitoring berhasil ditambahkan",
            "id": data.id,
            "simulation_date": (
                data.simulation_date.isoformat()
                if data.simulation_date
                else None
            ),
            "session_received_count": (
                session.received_count if session is not None else None
            ),
            "session_target_count": (
                session.target_count if session is not None else None
            ),
            "duplicate": False,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
