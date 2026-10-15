"""Custom exceptions for the secure service module."""


class UserAlreadyExistsError(Exception):
    """Raised when a username is already registered."""


class InvalidPasswordError(Exception):
    """Raised when a password does not meet the password policy."""


class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""
