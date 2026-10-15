"""Data models for the secure service module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Represent a registered user without exposing a plaintext password."""

    username: str
    password_hash: str
