import pytest

from secure_service.exceptions import InvalidPasswordError, UserAlreadyExistsError
from secure_service.service import UserService


def test_register_creates_user_with_hashed_password(mocker) -> None:
    repository = mocker.Mock()
    hasher = mocker.Mock()

    repository.get_by_username.return_value = None
    hasher.hash_password.return_value = "hashed-password"

    service = UserService(repository=repository, hasher=hasher)

    user = service.register(username="aline", password="StrongPass123!")

    assert user.username == "aline"
    assert user.password_hash == "hashed-password"
    repository.save.assert_called_once_with(user)
    hasher.hash_password.assert_called_once_with("StrongPass123!")


def test_register_rejects_duplicate_username(mocker) -> None:
    repository = mocker.Mock()
    hasher = mocker.Mock()
    repository.get_by_username.return_value = mocker.Mock()

    service = UserService(repository=repository, hasher=hasher)

    with pytest.raises(UserAlreadyExistsError):
        service.register(username="aline", password="StrongPass123!")

    repository.save.assert_not_called()
    hasher.hash_password.assert_not_called()


@pytest.mark.parametrize(
    "password",
    [
        "Short1!",  # Fewer than 8 characters
        "alllower123!",  # No uppercase letter
        "ALLUPPER123!",  # No lowercase letter
        "NoDigits!!",  # No digit
        "NoSpecial123",  # No special character
        "Space 123A!",  # Contains whitespace
    ],
)
def test_register_rejects_passwords_that_violate_policy(mocker, password: str) -> None:
    repository = mocker.Mock()
    hasher = mocker.Mock()
    repository.get_by_username.return_value = None

    service = UserService(repository=repository, hasher=hasher)

    with pytest.raises(InvalidPasswordError):
        service.register(username="aline", password=password)

    repository.save.assert_not_called()
    hasher.hash_password.assert_not_called()


def test_register_accepts_valid_password_with_eight_characters(mocker) -> None:
    repository = mocker.Mock()
    hasher = mocker.Mock()
    repository.get_by_username.return_value = None
    hasher.hash_password.return_value = "hashed-password"

    service = UserService(repository=repository, hasher=hasher)

    user = service.register(username="aline", password="Pass123!")

    assert user.password_hash == "hashed-password"
    repository.save.assert_called_once_with(user)
