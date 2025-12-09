"""
Security utility functions for the Hospital Insight Hub.

This module centralises basic security-related helpers so that
password handling and other sensitive operations are not scattered
throughout the codebase.
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
    """
    Create a salted hash for the given plain-text password.

    This wraps Werkzeug's generate_password_hash so that the rest
    of the application does not depend directly on the library call.
    """
    if not isinstance(plain_password, str):
        raise TypeError("Password must be a string.")
    return generate_password_hash(plain_password)


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Safely compare a plain-text password against a stored hash.

    Returns True if the password matches, False otherwise.
    """
    if not plain_password or not stored_hash:
        return False
    return check_password_hash(stored_hash, plain_password)
