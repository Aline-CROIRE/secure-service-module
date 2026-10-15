"""Tests for the in-memory user repository."""

from secure_service.models import User
from secure_service.repository import InMemoryUserRepository


def test_get_by_username_returns_none_for_missing_user() -> None:
    repository = InMemoryUserRepository()

    assert repository.get_by_username("missing") is None


def test_save_and_retrieve_user() -> None:
    repository = InMemoryUserRepository()
    user = User(username="aline", password_hash="stored-hash")

    repository.save(user)

    assert repository.get_by_username("aline") == user


def test_saving_same_username_replaces_existing_user() -> None:
    repository = InMemoryUserRepository()
    original = User(username="aline", password_hash="old-hash")
    updated = User(username="aline", password_hash="new-hash")

    repository.save(original)
    repository.save(updated)

    assert repository.get_by_username("aline") == updated
