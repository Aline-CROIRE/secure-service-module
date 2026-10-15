"""User registration and authentication service."""

from secure_service.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
)
from secure_service.interfaces import PasswordHasher, UserRepository
from secure_service.models import User


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
        """Register a user after validating the password and username."""
        if len(password) < 8:
            raise InvalidPasswordError("Password must contain at least 8 characters.")

        existing_user = self.repository.get_by_username(username)
        if existing_user is not None:
            raise UserAlreadyExistsError(
                f"Username '{username}' is already registered."
            )

        user = User(
            username=username,
            password_hash=self.hasher.hash_password(password),
        )
        self.repository.save(user)
        return user
