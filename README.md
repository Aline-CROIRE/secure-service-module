# Secure Service Module

A reusable Python authentication library demonstrating password hashing, user registration, login, dependency injection, testing, and clean architecture.

## Features

- User registration with duplicate-username protection.
- Minimum password length of eight characters.
- Password hashing and verification using bcrypt.
- In-memory user storage.
- Custom authentication exceptions.
- Logging for registration and authentication events.
- Automated tests with pytest and pytest-mock.
- Code-quality checks with Black, Ruff, and mypy.
- Pre-commit hooks.

## Architecture

- `models.py` — User data model.
- `interfaces.py` — Repository and password-hasher abstractions.
- `service.py` — Registration and authentication business logic.
- `repository.py` — In-memory user repository.
- `hasher.py` — Bcrypt password hashing implementation.
- `exceptions.py` — Custom exceptions.

The `UserService` receives a repository and password hasher through its constructor. This is dependency injection: business logic depends on abstractions rather than being tightly coupled to specific implementations.

## Requirements

Python 3.11 or later.

Install dependencies and the package in editable mode:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run tests

```powershell
python -m pytest tests
```

## Check statement and branch coverage

```powershell
python -m pytest --cov=secure_service --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The coverage requirement is satisfied only when the command passes.

## Run code-quality checks

```powershell
python -m black --check src tests
python -m ruff check src tests
python -m mypy src
python -m pre_commit run --all-files
```

## Example usage

```python
from secure_service.hasher import BcryptPasswordHasher
from secure_service.repository import InMemoryUserRepository
from secure_service.service import UserService

repository = InMemoryUserRepository()
hasher = BcryptPasswordHasher()
service = UserService(repository=repository, hasher=hasher)

user = service.register("aline", "StrongPass123!")
authenticated_user = service.login("aline", "StrongPass123!")

print(authenticated_user.username)
```

## Security limitations

The in-memory repository does not persist users between application runs and is not production storage. A production deployment should use persistent storage, secure configuration, appropriate rate limiting, and carefully designed authentication responses.

## Development workflow

Use feature branches, commit failing tests before their implementations, run the test and quality checks, review changes, and merge completed features into `main`.
