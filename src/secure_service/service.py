"""User registration and authentication service."""

import logging

from secure_service.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from secure_service.interfaces import PasswordHasher, UserRepository
from secure_service.models import User

logger = logging.getLogger(__name__)


class UserService:
    """Manage user registration and authentication."""

    def __init__(
        self,
        repository: UserRepository,
        hasher: PasswordHasher,
    ) -> None:
        """Initialize the service with injected dependencies.

        Args:
            repository: Storage implementation for user records.
            hasher: Implementation used to hash and verify passwords.
        """
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a user after validating the password.

        Passwords must contain at least eight characters, an uppercase
        letter, a lowercase letter, a digit, and a special character.
        Whitespace is not allowed.

        Args:
            username: Username for the new account.
            password: Plain-text password to validate and hash.

        Returns:
            The newly registered user.

        Raises:
            InvalidPasswordError: If the password violates the policy.
            UserAlreadyExistsError: If the username is already registered.
        """
        password_errors = []

        if len(password) < 8:
            password_errors.append("at least 8 characters")

        if not any(char.isupper() for char in password):
            password_errors.append("at least one uppercase letter")

        if not any(char.islower() for char in password):
            password_errors.append("at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            password_errors.append("at least one digit")

        if not any(not char.isalnum() and not char.isspace() for char in password):
            password_errors.append("at least one special character")

        if any(char.isspace() for char in password):
            password_errors.append("no whitespace")

        if password_errors:
            logger.warning("Registration rejected: password policy failed.")
            raise InvalidPasswordError(
                "Password must contain " + ", ".join(password_errors) + "."
            )

        existing_user = self.repository.get_by_username(username)
        if existing_user is not None:
            logger.warning("Registration rejected: username already exists.")
            raise UserAlreadyExistsError(
                f"Username '{username}' is already registered."
            )

        user = User(
            username=username,
            password_hash=self.hasher.hash_password(password),
        )
        self.repository.save(user)

        logger.info("User registration successful.")
        return user

    def login(self, username: str, password: str) -> User:
        """Authenticate a user using the injected repository and hasher.

        Args:
            username: Username of the account.
            password: Password to verify.

        Returns:
            The authenticated user.

        Raises:
            UserNotFoundError: If the username does not exist.
            InvalidPasswordError: If password verification fails.
        """
        user = self.repository.get_by_username(username)

        if user is None:
            logger.warning("Login failed: user not found.")
            raise UserNotFoundError("Invalid username or password.")

        if not self.hasher.verify_password(password, user.password_hash):
            logger.warning("Login failed: password verification failed.")
            raise InvalidPasswordError("Invalid username or password.")

        logger.info("User login successful.")
        return user
