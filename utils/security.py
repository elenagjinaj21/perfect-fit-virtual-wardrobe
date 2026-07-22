import hashlib
import hmac
import secrets

SCRYPT_N = 16_384
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_LENGTH = 32


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_LENGTH,
    )
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    if stored_password.startswith("scrypt$"):
        try:
            algorithm, n_text, r_text, p_text, salt_hex, digest_hex = stored_password.split("$", 5)
            if algorithm != "scrypt":
                return False
            digest = hashlib.scrypt(
                password.encode("utf-8"),
                salt=bytes.fromhex(salt_hex),
                n=int(n_text),
                r=int(r_text),
                p=int(p_text),
                dklen=len(bytes.fromhex(digest_hex)),
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, TypeError):
            return False

    if not stored_password.startswith("pbkdf2_sha256$"):
        # Support accounts created by older versions so users are not locked
        # out. Successful legacy logins are upgraded by the login screen.
        return hmac.compare_digest(password, stored_password)

    try:
        algorithm, rounds_text, salt_hex, digest_hex = stored_password.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(rounds_text)
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def needs_rehash(stored_password: str) -> bool:
    return not stored_password.startswith(f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}$")
