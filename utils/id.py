import uuid
import secrets


def generate_uuid() -> str:
    """
    This function generates a random UUID.
    """
    return str(uuid.uuid4())


def generate_token() -> str:
    """
    This function generates a random token.
    """
    return secrets.token_urlsafe(32)
