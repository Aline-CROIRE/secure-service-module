"""Tests for authentication service logging."""

import logging
from unittest.mock import Mock

import pytest

from secure_service.exceptions import (
    InvalidPasswordError,
    UserNotFoundError,
)
from secure_service.models import User
from secure_service.service import UserService


def test_successful_registration_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    repository = Mock()
    hasher = Mock()
    repository.get_by_username.return_value = None
    hasher.hash_password.return_value = "stored-hash"
    service = UserService(repository, hasher)

    with caplog.at_level(logging.INFO, logger="secure_service.service"):
        service.register("aline", "StrongPass123!")

    assert "User registration successful." in caplog.text
    assert "StrongPass123!" not in caplog.text
    assert "stored-hash" not in caplog.text


def test_failed_login_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    repository = Mock()
    hasher = Mock()
    repository.get_by_username.return_value = User(
        username="aline",
        password_hash="stored-hash",
    )
    hasher.verify_password.return_value = False
    service = UserService(repository, hasher)

    with caplog.at_level(logging.WARNING, logger="secure_service.service"):
        with pytest.raises(InvalidPasswordError):
            service.login("aline", "WrongPass123!")

    assert "Login failed" in caplog.text
    assert "WrongPass123!" not in caplog.text
    assert "stored-hash" not in caplog.text


def test_unknown_user_login_is_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    repository = Mock()
    hasher = Mock()
    repository.get_by_username.return_value = None
    service = UserService(repository, hasher)

    with caplog.at_level(logging.WARNING, logger="secure_service.service"):
        with pytest.raises(UserNotFoundError):
            service.login("missing", "StrongPass123!")

    assert "Login failed: user not found." in caplog.text
    hasher.verify_password.assert_not_called()
