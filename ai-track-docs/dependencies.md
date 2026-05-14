# Dependency Notes — book-app-project

## Policy

- Pin test dependencies to `>=current_minor,<next_major` to avoid surprise breaking changes.
- **Lower bounds must reflect the minimum actually tested version** — never allow a version older than what was validated.
- No runtime dependencies beyond the Python standard library (`json`, `dataclasses`, `typing`, `timeit`, `tempfile`).
- Review pins when upgrading Python or moving to a new major pytest release.
- Re-run the full test suite (`pytest -v`) after any dependency change before committing.

## Current dependencies (as of Run Ex 7 — 2026-05-13)

| Package | Declared constraint | Installed | Latest available | Role |
|---------|---------------------|-----------|-----------------|------|
| pytest     | `>=9.0.3,<10`  | 9.0.3   | 9.0.3   | Test runner |
| pytest-cov | `>=7.1,<8`     | 7.1.0   | 7.1.0   | Coverage reporting (dev) |
| ruff       | `>=0.15,<1`    | 0.15.12 | 0.15.12 | Linter/formatter (dev) |
| bandit     | `>=1.9,<2`     | 1.9.4   | 1.9.4   | Security scanner (dev) |

All packages are at their latest available versions. No upgrades pending.

> **Run Ex 7 note:** Lower bounds tightened from vague minimums (`>=9.0`, `>=0.4`, `>=5.0`, `>=1.7`) to exact installed floors (`>=9.0.3`, `>=0.15`, `>=7.1`, `>=1.9`). No install changes — constraints only. `bandit` added to the table (was installed but undocumented here).

> **Walk Ex 7 note:** `pytest-cov` constraint was previously declared as `<6` but the installed version (7.1.0) already exceeded it. Updated to `<8` to align declared constraint with installed reality. No functional change — same package, same behavior.

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
- `pytest` is the only runtime third-party dependency; no transitive deps of concern.
- `ruff` replaces both `flake8` and `isort` — no need to add those separately.
- `bandit` is configured via `[tool.bandit]` in `pyproject.toml` with `B101` suppressed (assert usage in test files is intentional).
- If a `requirements.txt` is added in future, it should be generated from `pyproject.toml` via `pip-compile` or equivalent.

## How to check for outdated packages

```powershell
cd samples/book-app-project
pip index versions pytest
pip index versions pytest-cov
pip index versions ruff
pip index versions bandit
```

## Rollback (Run Ex 7 constraint tighten)

```powershell
git revert <SHA>
pytest -v
```

Or manually restore in `pyproject.toml`:

```toml
dependencies = ["pytest>=9.0,<10"]

[project.optional-dependencies]
dev = ["ruff>=0.4,<1", "pytest-cov>=5.0,<8", "bandit>=1.7,<2"]
```

