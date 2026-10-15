"""In-memory implementation of user storage."""

from secure_service.models import User


class InMemoryUserRepository:
    """Store user records in memory, indexed by username."""

    def __init__(self) -> None:
        """Initialize an empty user store."""
        self._users: dict[str, User] = {}

    def get_by_username(self, username: str) -> User | None:
        """Return a user by username, or None if the user does not exist."""
        return self._users.get(username)

    def save(self, user: User) -> None:
        """Save a user record."""
        self._users[user.username] = user
