"""Custom exceptions for the secure service module."""


class UserAlreadyExistsError(Exception):
    """Raised when a username is already registered."""