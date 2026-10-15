"""User registration and authentication service."""

from secure_service.exceptions import UserAlreadyExistsError
from secure_service.interfaces import PasswordHasher, UserRepository
from secure_service.models import User


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
            hasher: Implementation responsible for password hashing.
        """
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a user after checking for duplicate usernames.

        Args:
            username: Unique username for the new user.
            password: Plaintext password to hash before storage.

        Returns:
            The newly created user record.

        Raises:
            UserAlreadyExistsError: If the username is already registered.
        """
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
