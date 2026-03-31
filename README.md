# Aura — Task Management API

## Overview

Aura is a production-structured REST API backend built with FastAPI and SQLite, designed to serve as the intelligent task management core of the Momentum productivity ecosystem. It exposes a clean CRUD interface for managing tasks with priority, energy cost, and deadline tracking — engineered from the ground up with a strict layered architecture that separates concerns across routes, domain models, repositories, and API schemas.

## Key Features

- Full CRUD API for task management via RESTful endpoints
- Dual-layer validation: Pydantic schema enforcement at the API boundary and domain-level business rule validation inside the Task model
- Parameterized SQL queries throughout the data access layer, eliminating SQL injection risk by design
- Automatic database initialization — the tasks table is created on first connection with no manual setup required
- Built-in interactive API documentation via FastAPI's auto-generated Swagger UI and ReDoc
- Task lifecycle tracking with enforced status transitions: `PENDING`, `COMPLETED`, `SKIPPED`
- Energy cost and priority fields designed to support future context-aware scheduling logic

## Tech Stack

**Backend**
- Python 3.x
- FastAPI — async-capable web framework with automatic OpenAPI spec generation
- Pydantic v2 — request/response validation and serialization

**Database**
- SQLite 3 — file-based relational database via Python's built-in `sqlite3` driver

**Development**
- Uvicorn — ASGI server for running the FastAPI application

## Architecture / How It Works

Aura follows a strict four-layer architecture:

```
HTTP Request
     |
     v
[main.py — Route Layer]
  FastAPI endpoints receive and route requests.
  HTTPException raised on invalid resource access.
     |
     v
[schemas/task_schema.py — API Contract Layer]
  Pydantic models (TaskCreate, TaskResponse) validate
  and serialize all inbound and outbound data.
     |
     v
[models/task.py — Domain Model Layer]
  The Task class enforces business rules:
  valid priority, status, and energy values,
  non-zero duration, and non-empty title.
     |
     v
[repositories/task_repository.py — Data Access Layer]
  TaskRepository translates Task objects to/from
  parameterized SQL queries against aura.db.
```

All write operations open a connection, execute a parameterized query, and close via context manager — no persistent connection pooling is required at this scale.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/your-username/Aura.git
cd Aura
pip install fastapi uvicorn pydantic
```

> A `requirements.txt` is not yet included. Install the three dependencies above manually.

### Run Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

The SQLite database (`aura.db`) is created automatically on first startup.

## Usage

### Check API Status

```bash
curl http://127.0.0.1:8000/
```

```json
{"message": "Aura API running"}
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review system design document",
    "priority": "HIGH",
    "energy_required": "HIGH",
    "deadline": "2026-04-15T10:00:00",
    "estimated_duration": 90
  }'
```

### Retrieve All Tasks

```bash
curl http://127.0.0.1:8000/tasks
```

### Retrieve a Single Task

```bash
curl http://127.0.0.1:8000/tasks/1
```

### Update a Task

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review system design document",
    "priority": "HIGH",
    "energy_required": "MEDIUM",
    "deadline": "2026-04-15T10:00:00",
    "estimated_duration": 60
  }'
```

### Delete a Task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

```json
{"message": "Task deleted successfully"}
```

## Project Structure

```
Aura/
├── main.py                        # FastAPI app instance and all route definitions
├── database.py                    # SQLite connection factory and schema initialization
├── aura.db                        # SQLite database file (auto-generated)
├── models/
│   └── task.py                    # Task domain model with constructor and validation logic
├── repositories/
│   └── task_repository.py         # Data access layer — all SQL operations live here
├── schemas/
│   └── task_schema.py             # Pydantic schemas for API request/response contracts
├── test_repo.py                   # Manual end-to-end CRUD verification script
├── LICENSE                        # MIT License
└── README.md                      # Project documentation
```

## API Documentation

### Base URL

```
http://127.0.0.1:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a single task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Task Object Schema

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | integer | Auto-assigned, read-only |
| `title` | string | Required, non-empty |
| `priority` | string | `LOW` \| `MEDIUM` \| `HIGH` |
| `energy_required` | string | `LOW` \| `MEDIUM` \| `HIGH` |
| `deadline` | datetime (ISO 8601) | Required |
| `estimated_duration` | integer | Minutes, must be > 0 |
| `status` | string | `PENDING` \| `COMPLETED` \| `SKIPPED` |

### Example: POST /tasks

**Request Body**
```json
{
  "title": "Deep work session",
  "priority": "HIGH",
  "energy_required": "HIGH",
  "deadline": "2026-04-20T09:00:00",
  "estimated_duration": 120
}
```

**Response — 200 OK**
```json
{
  "id": 3,
  "title": "Deep work session",
  "priority": "HIGH",
  "energy_required": "HIGH",
  "deadline": "2026-04-20T09:00:00",
  "estimated_duration": 120,
  "status": "PENDING"
}
```

**Response — 404 Not Found**
```json
{
  "detail": "Task not found"
}
```

## Challenges & Solutions

**1. Dual-Layer Validation Without Redundancy**

The API uses both Pydantic and a custom domain model. The challenge was defining a clean boundary: Pydantic handles structural and type validation at the HTTP boundary, while the `Task` model enforces business rules (valid enum values, positive duration). This prevents invalid domain state from ever reaching the database, regardless of how the Task is constructed — from an API request or directly in code.

**2. Type Safety Across the Database Boundary**

SQLite stores all values as text or integers, but the application works with `datetime` objects and typed enums. `TaskRepository._row_to_task()` centralizes all row-to-object mapping, ensuring type coercion (datetime parsing, integer casting) happens in one place. This makes the rest of the codebase type-safe and prevents scattered conversion logic.

**3. Stateless Connection Management**

Rather than maintaining a persistent database connection (which would introduce shared-state complexity at this scale), each repository method opens a connection via a Python context manager and releases it automatically on exit. This prevents connection leaks and makes every database operation fully self-contained.

**4. Schema/Model Separation for API Flexibility**

A single `Task` class serves as the internal domain object, while separate `TaskCreate` and `TaskResponse` Pydantic models define what the API accepts and returns. This separation means the API contract can evolve (e.g., exposing new response fields) without touching the domain model, and internal fields like `status` are defaulted server-side on creation rather than accepted as untrusted client input.

## Future Improvements

- Add `requirements.txt` and migrate to `pyproject.toml` for proper dependency management
- Replace SQLite with PostgreSQL for concurrent write support and production readiness
- Implement SQLAlchemy ORM with Alembic migrations to manage schema evolution safely
- Add JWT-based authentication to protect write endpoints
- Introduce a background scheduler ("Watcher") that surfaces tasks based on deadline proximity and current energy level
- Add comprehensive test coverage using `pytest` with fixture-based in-memory SQLite
- Containerize with Docker and add a `docker-compose.yml` for one-command local setup
- Extend the task model with recurrence rules and tagging for richer scheduling context

## Author

**Mehedi Mostafa Hafiz**

Built as part of the Momentum productivity ecosystem.
Licensed under the MIT License.
