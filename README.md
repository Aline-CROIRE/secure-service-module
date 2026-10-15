# Secure Service Module

A reusable Python authentication module that supports secure user registration and login through password validation, bcrypt hashing, dependency injection, custom exceptions, and automated testing.

This project was developed as part of the **AmaliTech Clean Code, Testing & Git assessment**, with a focus on Test-Driven Development (TDD), SOLID principles, code quality, and reliable authentication logic.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Demo](#running-the-demo)
- [Password Policy](#password-policy)
- [Using the Module](#using-the-module)
- [Error Handling](#error-handling)
- [Architecture](#architecture)
- [Testing and Coverage](#testing-and-coverage)
- [Code Quality](#code-quality)
- [Development Workflow](#development-workflow)
- [Security Considerations](#security-considerations)
- [Future Improvements](#future-improvements)

## Features

- **User registration:** Registers users after validating their passwords and checking for duplicate usernames.
- **User authentication:** Verifies credentials during login.
- **Password validation:** Enforces multiple password-strength requirements.
- **Password hashing:** Uses bcrypt instead of storing plain-text passwords.
- **Dependency injection:** Supplies repository and password-hashing implementations to `UserService`.
- **Custom exceptions:** Provides meaningful exceptions for registration and authentication failures.
- **In-memory storage:** Includes a repository implementation for storing user records during the application's lifetime.
- **Logging:** Records successful operations and authentication failures without logging passwords or password hashes.
- **Interactive demo:** Allows users to register, log in, and exit through a simple terminal menu.
- **Automated testing:** Uses pytest and pytest-mock to test expected behavior and failure scenarios.
- **Code quality checks:** Uses Black, Ruff, mypy, and pre-commit hooks.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| pytest | Automated testing |
| pytest-mock | Mocking dependencies in tests |
| bcrypt | Password hashing and verification |
| pytest-cov / Coverage.py | Statement and branch coverage |
| Black | Code formatting |
| Ruff | Linting and formatting checks |
| mypy | Static type checking |
| pre-commit | Automated checks before commits |
| Git and GitHub | Version control and source hosting |

## Project Structure

```text
secure-service-module/
│
├── src/
│   └── secure_service/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── hasher.py
│       ├── interfaces.py
│       ├── models.py
│       ├── repository.py
│       └── service.py
│
├── tests/
│   ├── test_hasher.py
│   ├── test_logging.py
│   ├── test_login.py
│   ├── test_registration.py
│   └── test_repository.py
│
├── .coveragerc
├── .gitignore
├── .pre-commit-config.yaml
├── demo.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Main components

- **`models.py`** — Defines the `User` dataclass containing a username and hashed password.
- **`interfaces.py`** — Defines the `UserRepository` and `PasswordHasher` protocols that describe the required dependency behavior.
- **`exceptions.py`** — Defines `UserAlreadyExistsError`, `InvalidPasswordError`, and `UserNotFoundError`.
- **`repository.py`** — Implements `InMemoryUserRepository` for storing and retrieving users.
- **`hasher.py`** — Implements `BcryptPasswordHasher` for hashing and verifying passwords.
- **`service.py`** — Implements `UserService`, which handles registration, password-policy validation, login, and logging.
- **`demo.py`** — Provides an interactive terminal application for demonstrating registration and login.
- **`tests/`** — Contains automated tests for the module's behavior and dependencies.

## Requirements

- Python 3.11 or later
- Git
- PowerShell, Command Prompt, or another terminal

The commands below use PowerShell on Windows.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Aline-CROIRE/secure-service-module.git
cd secure-service-module
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the virtual environment's Python executable directly using `.venv\Scripts\python.exe`.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Install the package in editable mode

```powershell
python -m pip install -e .
```

Editable installation makes the package available to the demo and tests while allowing changes to the source code to take effect without reinstalling it.

## Running the Demo

Start the interactive application from the project root:

```powershell
python demo.py
```

The application provides three options:

```text
====== SECURE SERVICE MODULE ======
1. Register
2. Login
3. Exit
===================================
Choose an option (1-3):
```

### Registration

Choose option `1` and enter a username and password. Password input is hidden in the terminal.

The application validates the password and checks whether the username already exists. If registration succeeds, the password is hashed and the user is saved.

### Login

Choose option `2` and enter the username and password. The service retrieves the user and verifies the supplied password against the stored hash.

### Exit

Choose option `3` to close the application.

**Note:** The demo uses in-memory storage. Registered users are not retained after the application exits, so register a user again when starting a new demo session.

## Password Policy

A password must satisfy all of the following requirements:

1. Contain at least 8 characters.
2. Include at least one uppercase letter.
3. Include at least one lowercase letter.
4. Include at least one digit.
5. Include at least one special character.
6. Contain no whitespace.

Example of a password that satisfies the policy:

```text
StrongPass123!
```

Examples of invalid passwords include:

| Password | Reason |
|---|---|
| `Short1!` | Fewer than 8 characters |
| `alllower123!` | No uppercase letter |
| `ALLUPPER123!` | No lowercase letter |
| `NoDigits!!` | No digit |
| `NoSpecial123` | No special character |
| `Space 123A!` | Contains whitespace |

The password policy is enforced inside `UserService.register()`, so it applies regardless of which interface calls the service.

## Using the Module

The service can be used by other Python code without using the interactive demo.

```python
from secure_service.hasher import BcryptPasswordHasher
from secure_service.repository import InMemoryUserRepository
from secure_service.service import UserService

repository = InMemoryUserRepository()
hasher = BcryptPasswordHasher()

service = UserService(
    repository=repository,
    hasher=hasher,
)

user = service.register(
    username="aline",
    password="StrongPass123!",
)

print(f"Registered user: {user.username}")

authenticated_user = service.login(
    username="aline",
    password="StrongPass123!",
)

print(f"Authenticated user: {authenticated_user.username}")
```

The example assumes that the package has been installed and the script runs in the configured Python environment.

## Error Handling

The module defines custom exceptions to distinguish common failure scenarios.

| Exception | When it is raised |
|---|---|
| `InvalidPasswordError` | The password fails registration policy validation or login password verification |
| `UserAlreadyExistsError` | The username is already registered |
| `UserNotFoundError` | The username supplied during login does not exist |

Example:

```python
from secure_service.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

try:
    service.register("aline", "weak")
except InvalidPasswordError as error:
    print(f"Registration failed: {error}")

try:
    service.login("unknown-user", "StrongPass123!")
except UserNotFoundError as error:
    print(f"Login failed: {error}")
```

These exceptions allow applications that use the module to handle authentication failures explicitly.

## Architecture

The module separates business logic from storage and password-hashing implementations.

```text
             Application / Demo
                     |
                     v
                UserService
                 /       \
                v         v
       UserRepository   PasswordHasher
                |         |
                v         v
       In-Memory Store   Bcrypt
```

### Dependency injection

`UserService` receives its repository and password hasher through its constructor rather than creating concrete implementations internally.

This makes dependencies replaceable and allows tests to use mock objects instead of real storage or hashing implementations.

### SOLID principles

- **Single Responsibility Principle:** User data, storage, password hashing, exceptions, and authentication logic are separated into dedicated components.
- **Open/Closed Principle:** New implementations of the repository or hasher can be introduced without rewriting the service, provided they satisfy the expected interfaces.
- **Liskov Substitution Principle:** Alternative implementations should honor the behavior expected by the repository and hasher protocols.
- **Interface Segregation Principle:** The protocols describe the operations required by the service rather than exposing unrelated functionality.
- **Dependency Inversion Principle:** The service depends on abstractions instead of being tightly coupled to the concrete repository and hashing classes.

## Testing and Coverage

The project uses pytest for automated testing and pytest-mock to isolate dependencies where appropriate.

The test suite covers:

- Password hashing and verification.
- User registration and duplicate-username rejection.
- Password-policy validation.
- Successful login and failed authentication.
- Repository behavior.
- Logging of authentication events.

### Run all tests

```powershell
python -m pytest -v
```

### Run tests with statement and branch coverage

```powershell
python -m pytest --cov=secure_service --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The coverage configuration requires at least 100% coverage.

**Verified result for the strengthened password policy:** 21 tests passed, with 100% statement and branch coverage. The `service.py` file had 44 statements and 20 branches covered, with no missed statements or branches.

Coverage results describe the tested code paths; they do not guarantee the absence of every possible defect.

## Code Quality

The project uses automated tools to maintain consistent formatting, catch common issues, and check types.

### Run pre-commit checks

```powershell
python -m pre_commit run --all-files
```

This runs the configured checks, including:

- **Black:** Consistent Python formatting.
- **Ruff:** Linting and formatting checks.
- **mypy:** Static type checking of the source code.

If Black modifies files during its first run, run the command again to confirm the formatted files pass.

### Check Git whitespace errors

```powershell
git diff --check
```

## Development Workflow

The project follows a Test-Driven Development workflow:

1. **Red:** Write a test describing the expected behavior and verify that it fails for the intended reason.
2. **Green:** Implement the smallest change necessary to make the test pass.
3. **Refactor:** Improve the implementation while keeping the tests passing.

Feature branches are used to organize development work. Changes should be tested, reviewed, and merged after the required checks pass.

Before committing changes, run the tests, coverage checks, and pre-commit hooks.

Example Git workflow:

```powershell
git switch -c feature/your-change
```

After making changes and verifying them:

```powershell
git add .
git commit -m "feat: describe your change"
git push -u origin feature/your-change
```

The branch can then be reviewed and merged into `main`.

## Security Considerations

This project demonstrates authentication concepts; it is not a complete production identity system.

- **Password storage:** Passwords are hashed with bcrypt rather than stored as plain text.
- **Password validation:** Registration rejects passwords that do not satisfy the defined policy.
- **Logging:** Authentication logs avoid including passwords and password hashes.
- **Storage:** The in-memory repository is temporary and is not suitable for persistent user accounts.
- **Authentication responses:** The service uses the same error message for an unknown username and an incorrect password, although it raises different exception types internally.
- **Production deployment:** A production system would need persistent storage, appropriate secret and configuration management, rate limiting, monitoring, and additional security review.
- **Transport security:** Any web or network interface using this module should protect credentials in transit with HTTPS.

## Future Improvements

Potential extensions include:

- A persistent database-backed repository.
- Additional integration tests with a real storage implementation.
- Rate limiting and protections against repeated login attempts.
- More comprehensive authentication security reviews.
- Additional application interfaces that reuse the service without duplicating business logic.

## Author

**Aline NIYONIZERA**

GitHub: [Aline-CROIRE](https://github.com/Aline-CROIRE)

---

*Built as a Python authentication module with an emphasis on clean code, dependency injection, Test-Driven Development, and automated quality checks.*
