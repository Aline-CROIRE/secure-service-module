from unittest.mock import Mock

import pytest

from secure_service.exceptions import UserAlreadyExistsError
from secure_service.service import UserService


def test_register_creates_user_with_hashed_password() -> None:
    repository = Mock()
    hasher = Mock()

    repository.get_by_username.return_value = None
    hasher.hash_password.return_value = "hashed-password"

    service = UserService(repository=repository, hasher=hasher)

    user = service.register(username="aline", password="StrongPass123!")

    assert user.username == "aline"
    assert user.password_hash == "hashed-password"
    repository.save.assert_called_once_with(user)
    hasher.hash_password.assert_called_once_with("StrongPass123!")


def test_register_rejects_duplicate_username() -> None:
    repository = Mock()
    hasher = Mock()
    repository.get_by_username.return_value = Mock()

    service = UserService(repository=repository, hasher=hasher)

    with pytest.raises(UserAlreadyExistsError):
        service.register(username="aline", password="StrongPass123!")

    repository.save.assert_not_called()
    hasher.hash_password.assert_not_called()
