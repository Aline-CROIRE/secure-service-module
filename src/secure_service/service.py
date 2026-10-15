"""User authentication service."""


class UserService:
    """Manage user registration and authentication."""

    def __init__(self, repository, hasher):
        """Initialize the service with injected dependencies."""
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str):
        """Register a new user."""
        raise NotImplementedError