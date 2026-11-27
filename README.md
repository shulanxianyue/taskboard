# TaskBoard

## Purpose

TaskBoard is a lightweight FastAPI application for managing tasks. It exposes REST endpoints for creating, listing, retrieving, updating, and deleting tasks, plus a health-check endpoint. Task data is currently stored in memory.

## Requirements

- Python 3.11+
- `pip`
- `pytest`

## Installation

1. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run

Start the development server:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Tests

Run the test suite with pytest:

```powershell
pytest
```

## Environment variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Available variables:

- `APP_ENV`: application environment
- `LOG_LEVEL`: application log level
- `DATABASE_URL`: database connection URL
- `SECRET_KEY`: application secret key

Never commit `.env` to source control. It may contain local configuration or secrets.

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── tasks.py
├── docs/
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
├── .env.example
├── requirements.txt
└── README.md
```

## Validation rules

Invalid input is rejected with **422 Unprocessable Entity**.

| Field | Rule | Response |
| --- | --- | --- |
| `title` | Required on create, trimmed, 1–200 characters, never null | 422 |
| `description` | Optional, at most 2,000 characters | 422 |
| `status` | One of `todo`, `in_progress`, `done`; default `todo`; never null | 422 |
| Unknown fields (`id`, `owner`, …) | Rejected | 422 |
| `task_id` (path) | Positive integer | 422 if not, 404 if unknown |
