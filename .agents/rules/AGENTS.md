# Project Domain

It is a {provide small description of the project}

> **Template Note**: When adapting this repository for a new project, fill in `{...}` placeholders and remove any entrypoint or persistence subsections below that do not apply to your solution.

## 1. Project Setup and Management

- **Python version**: 3.12.14. Do not use syntax from newer Python versions.
- **Python environment**: Located at `/usr/app/venv/bin/python`.
- **Dependency management**: `pip` using `requirements.txt` (core) and `.devcontainer/*-requirements.txt` (`dev-requirements.txt`, `webapp-requirements.txt`, `cli-requirements.txt`). Explicitly ask for permission before adding or installing new libraries.
- **Change & Git policy**: Always ask for approval before implementing changes. Do not commit changes.
- **Database / Environment safety**: Never change the target database or cloud environment to production. Always point to the test database/environment.
- **Testing command**: Run tests using `python -m pytest` followed by any required parameters.

## 2. Core Architecture Rules

- **Architectural Philosophy**: The repository strictly follows **Clean / Onion Architecture** and **Domain-Driven Design (DDD)** principles:
  ```
  [ Entrypoints: Flask REST API / WebApp / CLI / Cloud Function ]
                            │ (DTOs / Primitives)
                            ▼
                  [ Application Services ]
                    │                  │
                    ▼                  ▼
    [ Domain Model / Aggregates ]   [ Repository Interfaces (DIP) ]
                                                ▲
                                                │
                                  [ Infrastructure / DB Adapters ]
  ```
- **Zero-Dependency Domain**: The domain layer (`src/model.py`) must remain pure Python. It must have no dependencies on web frameworks (Flask/WTForms/marshmallow), CLI libraries (Click), cloud SDKs, databases, ORMs, or infrastructure adapters.
- **Dependency Inversion Principle (DIP)**: High-level modules (`src/services.py`) must not depend on low-level infrastructure modules. Services interact exclusively with abstract repository interfaces (`ABC`) defined in `src/*_repository.py` (e.g., `src/source_repository.py`, `src/destination_repository.py`, or `src/repository.py`).
- **Entrypoints are Details**: Adding or modifying entrypoints under `src/entrypoints/` must never require changes to domain business logic.
- **Decoupling via DTOs**: When transferring structured input across boundaries (REST Schemas / Web Forms / CLI ⇄ Services), use immutable Data Transfer Objects (`@dataclass(frozen=True)`) defined in `src/dto.py`.

## 3. Data & Persistence Layer

- **Repository Pattern**: All external data and database interactions must be encapsulated inside concrete implementations of the `Abstract*Repository` interfaces.
- **If using SQL / PostgreSQL**:
  - Store all SQL queries as named constants in `src/utils/sql_queries.py`.
  - Format table and schema names dynamically using `SqlTable` abstractions.
  - Parameterize query values safely with `%s` to prevent SQL injection.
  - Use lightweight DB clients (e.g., `PostgresGCPClient` / `psycopg2`) rather than heavy ORMs.
- **If using GCP Data Services (BigQuery / GCS / APIs)**:
  - Keep GCP SDK clients (`google-cloud-*`) strictly inside concrete repository adapter classes, injecting them via constructor.

## 4. Entrypoints Conventions

Keep only the subsections that apply to your project:

### 4.1 RESTful API (`src/entrypoints/flaskapp/`)
- **Modular Blueprints**: Split route endpoints logically by feature under `src/entrypoints/flaskapp/blueprints/` using `flask-smorest`.
- **Schema Validation (`marshmallow`)**: Define request/response schemas with `marshmallow.Schema`. When mapping complex payloads to services, implement a `.to_dto()` method on the schema to return the corresponding DTO from `src/dto.py`.
- **Authentication**: Protect endpoints with `@jwt_required()` from `Flask-JWT-Extended` where required.

### 4.2 Command Line Interface (`src/entrypoints/cli/`)
- **Click Commands**: Build CLI commands and subcommands using `click` under `src/entrypoints/cli/`.
- **Thin Entrypoints**: CLI functions should only parse arguments, instantiate concrete repositories, and delegate execution to `src/services.py`.

### 4.3 Cloud Function (`src/entrypoints/cloud_function/`)
- **Serverless Handler**: Keep `src/entrypoints/cloud_function/main.py` as a thin wrapper that parses the event/request, initializes adapters, and calls `src/services.py`.

### 4.4 Server-Side WebApp (Optional — if using Jinja2 + WTForms)
- **Modular Blueprints**: Organize web routes by feature under `src/entrypoints/webapp/blueprints/`.
- **Form Handling (`WTForms`)**: Place forms in `forms.py` within each blueprint and implement `.to_dto()` to map validated inputs into DTOs in `src/dto.py`.
- **Route Error Handling**:
  - Catch domain `ValueError` exceptions and report them via Flask `flash(..., "warning")`.
  - Catch unexpected generic `Exception` errors, log them using `logger.exception(...)`, and display user-friendly messages.
- **Templates & UI**: Extend `templates/base.html` using Bootstrap 5, vanilla JS with HTML5 `data-*` attributes for dynamic dropdowns, and HTML test marker comments (e.g., `<!--page_name this comment is to check that it is reached on test-->`).

## 5. Code Style & Typing Guidelines

- **Strict Type Hinting**: Type-hint all public functions and methods, including return types.
- **Language**: All code, docstrings, comments, commit messages, and documentation must be written in **English**.
- **String Formatting**: Prefer f-strings over `str.format()` or `%` formatting.
- **Idiomatic Python**: Embrace idiomatic Python constructs such as comprehensions, generators, dataclasses, and decorators.
- **Formatting**: Format code following `black` standards.

## 6. Testing Standards & Conventions

- **Pytest**: Use `pytest` for all testing (`tests/`).
- **Gherkin-Style Documentation**: Every test function must include a structured Gherkin docstring (`GIVEN ... WHEN ... THEN ...`).
- **Fixture Reusability & Parametrization**: Reuse shared fixtures from `tests/conftest.py`. For repetitive test cases, always use `@pytest.mark.parametrize` instead of duplicating test functions.
- **Test Isolation**: Tests and database fixtures must clean up after themselves (e.g., `TRUNCATE ... RESTART IDENTITY CASCADE` for SQL tests, or isolated test datasets/tables for GCP).
- **Mocking External Boundaries**: Use fake/in-memory repositories or `unittest.mock.patch` (humble object pattern) to simulate service failures or external edge cases when direct testing is not possible. It is a priority to enforce testing against external services when dev/testing isntances are available.
- **High Test Coverage**: Maintain comprehensive test coverage (`>= 95%` enforced in CI) across domain models, DTOs, repositories, services, and entrypoints.
