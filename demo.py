"""Interactive demonstration of the secure authentication module."""

from getpass import getpass

from secure_service.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from secure_service.hasher import BcryptPasswordHasher
from secure_service.repository import InMemoryUserRepository
from secure_service.service import UserService

repository = InMemoryUserRepository()
hasher = BcryptPasswordHasher()
service = UserService(repository, hasher)


def register_user():
    """Register a user using interactive input."""
    print("\n--- Registration ---")
    username = input("Username: ").strip()
    password = getpass("Password (hidden): ")

    service.register(username, password)
    print(f"Registration successful for '{username}'.")


def login_user():
    """Authenticate a user using interactive input."""
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = getpass("Password (hidden): ")

    service.login(username, password)
    print(f"Login successful. Welcome, '{username}'!")


def main():
    """Display the menu until the user exits."""
    while True:
        print("\n====== SECURE SERVICE MODULE ======")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("===================================")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            try:
                register_user()
            except (InvalidPasswordError, UserAlreadyExistsError) as error:
                print(f"\nRegistration failed: {type(error).__name__}")
                print(f"Reason: {error}")

        elif choice == "2":
            try:
                login_user()
            except (InvalidPasswordError, UserNotFoundError) as error:
                print(f"\nLogin failed: {type(error).__name__}")
                print(f"Reason: {error}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
