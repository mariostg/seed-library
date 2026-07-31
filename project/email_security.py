import base64
import hashlib
import hmac

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from cryptography.fernet import Fernet
except Exception:  # pragma: no cover
    Fernet = None


def normalize_email(email: str | None) -> str:
    return (email or "").strip().lower()


def _required_setting(name: str) -> str:
    """Retrieve a required setting from Django settings or environment variables."""
    value = getattr(settings, name, None)
    if value:
        return str(value)

    if settings.SECRET_KEY:
        return f"{settings.SECRET_KEY}:{name}"

    raise ImproperlyConfigured(
        f"Missing required setting: {name}. Set it to a long random secret."
    )


def _fernet() -> "Fernet":
    """Create a Fernet instance for email encryption/decryption."""
    if Fernet is None:
        raise ImproperlyConfigured(
            "cryptography is required for email encryption. Install the 'cryptography' package."
        )

    key_material = _required_setting("EMAIL_ENCRYPTION_KEY")
    digest = hashlib.sha256(key_material.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_email(email: str | None) -> str:
    """Encrypt the given email address using Fernet symmetric encryption."""

    normalized = normalize_email(email)
    if not normalized:
        return ""
    return _fernet().encrypt(normalized.encode("utf-8")).decode("utf-8")


def decrypt_email(token: str | None) -> str:
    """Decrypt the given token back to the original email address using Fernet symmetric encryption."""
    if not token:
        return ""
    return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")


def email_hash(email: str | None) -> str:
    """Generate a SHA-256 hash of the normalized email address using a secret key for HMAC.
    This ensures that the hash is unique and secure, preventing exposure of the original email address.
    """
    normalized = normalize_email(email)
    if not normalized:
        return ""

    hash_key = _required_setting("EMAIL_HASH_KEY")
    digest = hmac.new(
        hash_key.encode("utf-8"), normalized.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return digest
