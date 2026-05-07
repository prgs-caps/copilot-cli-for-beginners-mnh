# Dependency Notes — book-app-project

## Policy

- Pin test dependencies to `>=current_minor,<next_major` to avoid surprise breaking changes.
- No runtime dependencies beyond the Python standard library (`json`, `dataclasses`, `typing`, `timeit`, `tempfile`).
- Review pins when upgrading Python or moving to a new major pytest release.

## Current dependencies

| Package | Declared constraint | Installed (verified) | Role |
|---------|--------------------|-----------------------|------|
| pytest  | `>=9.0,<10`        | 9.0.3                 | Test runner |

## Standard-library modules used

| Module       | Purpose |
|--------------|---------|
| `json`       | Persist book collection to/from data.json |
| `dataclasses`| `Book` dataclass definition |
| `typing`     | Type hints (`List`, `Optional`) |
| `timeit`     | Micro-benchmark in bench_find.py |
| `tempfile`   | Temporary files in bench_find.py and tests |
| `os`         | File cleanup in bench_find.py |

## Gaps / notes

- No `requirements.txt` — `pyproject.toml` is the single source of truth for this sub-project.
- `pytest` is the only third-party dependency; no transitive deps of concern.
- If a `requirements.txt` is added in future, it should be generated from `pyproject.toml` via `pip-compile` or equivalent.
