"""Authentication helpers using Python standard-library cryptography."""
import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database.session import SessionLocal
from models.user import User

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "local-development-secret-change-before-deployment"
).encode("utf-8")
TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "28800"))
PASSWORD_ITERATIONS = 310_000
SIMULATOR_API_KEY = os.getenv(
    "SIMULATOR_API_KEY",
    "local-simulator-key-change-before-deployment"
)
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    salt_text = base64.urlsafe_b64encode(salt).decode("ascii")
    hash_text = base64.urlsafe_b64encode(derived).decode("ascii")
    return "pbkdf2_sha256$" + str(PASSWORD_ITERATIONS) + "$" + salt_text + "$" + hash_text


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_text, hash_text = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected = base64.urlsafe_b64decode(hash_text.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def create_access_token(user_id: int) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "iat": now, "exp": now + TOKEN_TTL_SECONDS}
    signing_input = (
        _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        + "."
        + _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    )
    signature = hmac.new(
        JWT_SECRET_KEY, signing_input.encode("ascii"), hashlib.sha256
    ).digest()
    return signing_input + "." + _b64url(signature)


def decode_access_token(token: str) -> int:
    try:
        header_text, payload_text, signature_text = token.split(".")
        signing_input = header_text + "." + payload_text
        expected_signature = hmac.new(
            JWT_SECRET_KEY, signing_input.encode("ascii"), hashlib.sha256
        ).digest()
        supplied_signature = _b64url_decode(signature_text)
        if not hmac.compare_digest(expected_signature, supplied_signature):
            raise ValueError("Signature tidak valid.")

        header = json.loads(_b64url_decode(header_text))
        payload = json.loads(_b64url_decode(payload_text))
        if header.get("alg") != "HS256":
            raise ValueError("Algoritma token tidak didukung.")
        if int(payload.get("exp", 0)) <= int(time.time()):
            raise ValueError("Token telah kedaluwarsa.")

        user_id = int(payload.get("sub"))
        if user_id <= 0:
            raise ValueError("Identitas pengguna tidak valid.")
        return user_id
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesi tidak valid atau telah berakhir. Silakan masuk kembali.",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Silakan masuk untuk mengakses halaman ini.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = decode_access_token(credentials.credentials)
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active.is_(True)
        ).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Akun tidak ditemukan atau tidak aktif."
            )
        return user
    finally:
        db.close()


def verify_simulator_key(
    x_simulator_key: str = Header(default="", alias="X-Simulator-Key")
) -> bool:
    if not hmac.compare_digest(
        x_simulator_key.encode("utf-8"),
        SIMULATOR_API_KEY.encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kunci akses simulator tidak valid."
        )
    return True
