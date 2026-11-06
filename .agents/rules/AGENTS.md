# Project Domain

It is a {provide small description of the project}

## 1. Project Setup and Management

- Python version: 3.12.14. Don't use newer syntax.
- Dependency management: `pip` with requirements for the app in `requirements.txt` file. Explicitly ask for permissions when requiring new libraries.
- Always ask for approval before implementing changes. Do not commit changes.
- Never change the database you are pointing to. Always go to the test database.
- Python environment is located at `/usr/app/venv/bin/python`
- For testing use: `python -m pytest` followed by any parameter you required for your purpose.

## 2. Core Architecture Rules:

 - **Architectural Philosophy**:  The repository strictly follows **Clean / Onion Architecture** and **Domain-Driven Design (DDD)** principles:
    ```
    [ Entrypoints: Flask WebApp / CLI / RESTful API ]
                    │ (DTOs)
                    ▼
          [ Application Services ]
            │                  │
            ▼                  ▼
    [ Domain Model / Aggregates ]   [ Repository Interface (DIP) ]
                                                ▲
                                                │
                                  [ Database Infrastructure Adapter ]
    ```
- **Zero-Dependency Domain**: The domain layer (`src/model.py`) must remain pure Python. It must have no dependencies on web frameworks (Flask/WTForms), databases, ORMs, or infrastructure adapters.
- **Dependency Inversion Principle (DIP)**: High-level modules must not depend on low-level database modules. Services interact exclusively with `AbstractRepository` (`src/repository.py`).
- **Entrypoints are Details**: Adding or modifying entrypoints must never require changes to domain business logic.
- **Decoupling via DTOs**: Transfer data across boundaries (Flask Forms ⇄ Services) exclusively using immutable Data Transfer Objects (`@dataclass(frozen=True)`) defined in `src/dto.py`.


## 3. Database & Persistence Layer

- **Repository Pattern**: All database interactions are encapsulated inside implementation of `AbstractRepository`.
- **Centralized SQL Queries**:
  - All SQL queries must be stored as named constants in `src/utils/sql_queries.py`.
  - Table and schema names are dynamically formatted using `SqlTable` abstractions.
  - Query parameters must **always** be safely parameterized with `%s` to prevent SQL injection.
- **Lightweight DB Client**: Use `PostgresGCPClient` (`psycopg2`) without heavy ORMs.


## 4. Web Layer & Flask Conventions

- **Modular Blueprints**: Route endpoints are split logically by feature under `src/entrypoints/webapp/blueprints/`.
- **Form Handling with WTForms**:
  - Web forms are located in `forms.py` within their respective blueprint.
  - Each form must implement a `.to_dto()` method to map validated form input into the corresponding DTO in `src/dto.py`.
- **Route Error Handling**:
  - Catch domain `ValueError` exceptions specifically and report them to the user via Flask `flash(..., "warning")`.
  - Catch unexpected generic `Exception` errors, log them using `logger.exception(...)`, and display user-friendly error messages.
- **Templates & UI**:
  - Extend `templates/base.html` using Bootstrap 5 components.
  - Use vanilla JavaScript and HTML5 `data-*` attributes for dynamic dependent dropdowns.
  - Include HTML test marker comments (e.g. `<!--transactions_list this comment is to check that it is reached on test-->`) to facilitate test verification.


## 5. Code Style & Typing Guidelines

- **Strict Type Hinting**: Type-hint public functions and methods, including their return types.
- **Language**: Code, docstrings, commit messages, and documentation must be written in **English**.
- **f-string**: Prefer f-strings over `str.format()` or `%` formatting.
- **idiomatic Python**: Embrace idiomatic Python like comprehensions, generators, and decorators.


## 6. Testing Standards & Conventions

- **Pytest**: use pytest library for testing.
- **Gherkin-Style Documentation**: Every test function must include a structured Gherkin docstring.
- **Fixture Reusability**: Use shared fixtures from `tests/conftest.py` (`db_conn`, `postgres_repo`, `repo_with_data`, `client`, `client_logged_in`). For repetitive tests, always use pytest.mark.parametrize instead of writing multiple similar test functions.
- **Test Isolation**: Database fixtures must clean up after themselves (using `TRUNCATE ... RESTART IDENTITY CASCADE`).
- **Mocking External Boundaries**: Use `unittest.mock.patch` to simulate service failures or edge-case exceptions in web route testing. Restrict to cases where direct testing is not possible. Use humble pattern.
- **High Test Coverage**: Maintain comprehensive coverage across domain models, DTOs, repositories, services, and web routes.


## 7. API Layer

- **RESTful API**
- **Modular Blueprints**: Route endpoints are split logically by feature under `src/entrypoints/api/blueprints/`.
- **Schema Handling with marshmallow**:
  - Each schema must implement a `.to_dto()` method to map validated schema input into the corresponding DTO in `src/dto.py`.