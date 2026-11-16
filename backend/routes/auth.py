from fastapi import APIRouter, Depends, HTTPException, status

from auth import create_access_token, get_current_user, hash_password, verify_password
from database.session import SessionLocal
from models.user import User
from schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    LoginResponse,
    RegisterRequest
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email sudah terdaftar. Silakan masuk atau gunakan email lain."
            )

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "message": "Akun berhasil dibuat. Silakan masuk menggunakan email dan kata sandi.",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if (
            user is None
            or not user.is_active
            or not verify_password(payload.password, user.password_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau kata sandi tidak sesuai."
            )
        return {
            "access_token": create_access_token(user.id, user.auth_version),
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }
    finally:
        db.close()


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        user = (
            db.query(User)
            .filter(User.id == current_user.id, User.is_active.is_(True))
            .with_for_update()
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Akun tidak ditemukan atau tidak aktif."
            )

        if not verify_password(payload.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kata sandi saat ini tidak sesuai."
            )

        if verify_password(payload.new_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kata sandi baru harus berbeda dari kata sandi saat ini."
            )

        user.password_hash = hash_password(payload.new_password)
        user.auth_version = int(user.auth_version or 0) + 1
        db.commit()
        db.refresh(user)

        # Rotate this browser's token while invalidating tokens issued to
        # other sessions/devices using the previous auth_version.
        return {
            "message": "Kata sandi berhasil diperbarui.",
            "access_token": create_access_token(user.id, user.auth_version),
            "token_type": "bearer"
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/me")
def current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email
    }
