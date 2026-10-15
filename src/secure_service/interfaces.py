"""Abstractions for storage and password hashing."""

from typing import Protocol

from secure_service.models import User


class UserRepository(Protocol):
    """Define the storage operations required by the service."""

    def get_by_username(self, username: str) -> User | None:
        """Return a user by username, or None if absent."""
        ...

    def save(self, user: User) -> None:
        """Persist a user."""
        ...


class PasswordHasher(Protocol):
    """Define the password hashing operations required by the service."""

    def hash_password(self, password: str) -> str:
        """Return a secure hash of a plaintext password."""
        ...

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Check a plaintext password against its stored hash."""
        ...
