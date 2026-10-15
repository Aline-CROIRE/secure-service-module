"""Tests for bcrypt password hashing."""

from secure_service.hasher import BcryptPasswordHasher


def test_hash_password_does_not_return_plaintext() -> None:
    hasher = BcryptPasswordHasher()

    hashed = hasher.hash_password("StrongPass123!")

    assert hashed != "StrongPass123!"
    assert hasher.verify_password("StrongPass123!", hashed)


def test_same_password_produces_different_hashes() -> None:
    hasher = BcryptPasswordHasher()

    first_hash = hasher.hash_password("StrongPass123!")
    second_hash = hasher.hash_password("StrongPass123!")

    assert first_hash != second_hash
    assert hasher.verify_password("StrongPass123!", first_hash)
    assert hasher.verify_password("StrongPass123!", second_hash)


def test_verify_password_rejects_wrong_password() -> None:
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash_password("StrongPass123!")

    assert not hasher.verify_password("WrongPass123!", hashed)
