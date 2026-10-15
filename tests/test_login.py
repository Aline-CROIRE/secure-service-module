
"""Tests for user authentication."""

from unittest.mock import Mock

import pytest

from secure_service.exceptions import InvalidPasswordError, UserNotFoundError
from secure_service.models import User
from secure_service.service import UserService


def test_login_returns_user_when_password_is_correct() -> None:
    repository = Mock()
    hasher = Mock()

    user = User(username="aline", password_hash="stored-hash")
    repository.get_by_username.return_value = user
    hasher.verify_password.return_value = True

    service = UserService(repository=repository, hasher=hasher)

    authenticated_user = service.login(
        username="aline",
        password="StrongPass123!",
    )

    assert authenticated_user == user
    repository.get_by_username.assert_called_once_with("aline")
    hasher.verify_password.assert_called_once_with(
        "StrongPass123!",
        "stored-hash",
    )


def test_login_rejects_unknown_username() -> None:
    repository = Mock()
    hasher = Mock()
    repository.get_by_username.return_value = None

    service = UserService(repository=repository, hasher=hasher)

    with pytest.raises(UserNotFoundError):
        service.login(username="unknown", password="StrongPass123!")

    hasher.verify_password.assert_not_called()


def test_login_rejects_incorrect_password() -> None:
    repository = Mock()
    hasher = Mock()

    user = User(username="aline", password_hash="stored-hash")
    repository.get_by_username.return_value = user
    hasher.verify_password.return_value = False

    service = UserService(repository=repository, hasher=hasher)

    with pytest.raises(InvalidPasswordError):
        service.login(username="aline", password="WrongPass123!")

    hasher.verify_password.assert_called_once_with(
        "WrongPass123!",
        "stored-hash",
    )
