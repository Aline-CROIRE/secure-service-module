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
        """Initialize the service with injected dependencies."""
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a user after validating the password."""
        if len(password) < 8:
            logger.warning("Registration rejected: password policy failed.")
            raise InvalidPasswordError("Password must contain at least 8 characters.")

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
        """Authenticate a user using the injected repository and hasher."""
        user = self.repository.get_by_username(username)

        if user is None:
            logger.warning("Login failed: user not found.")
            raise UserNotFoundError("Invalid username or password.")

        if not self.hasher.verify_password(password, user.password_hash):
            logger.warning("Login failed: password verification failed.")
            raise InvalidPasswordError("Invalid username or password.")

        logger.info("User login successful.")
        return user
