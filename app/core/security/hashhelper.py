from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as exc:
        # Surface a clear error if hashing backend is misconfigured
        raise RuntimeError(
            "Password hashing backend error. Ensure 'argon2-cffi' is installed and up-to-date."
        ) from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
