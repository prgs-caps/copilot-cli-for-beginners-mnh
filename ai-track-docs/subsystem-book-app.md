# Subsystem Index — book-app-project

> **Run Ex 4 — Documentation Sync at Subsystem Level**
> Scope: `samples/book-app-project/`
> Updated: 2026-05-13

This document maps every file in the subsystem to its purpose, risk level, and related documentation.
Use it as the first stop for orientation before making changes.

---

## File Map

| File | Real path | Purpose | Risk |
|---|---|---|---|
| `books.py` | `samples/book-app-project/books.py` | Core domain — `BookCollection` class, `Book` dataclass, all CRUD + persistence | **Medium** — mutating methods write to disk; retry logic is sensitive to `initial_delay`/`backoff` params |
| `utils.py` | `samples/book-app-project/utils.py` | Shared helpers — `titles_match()` (case flag), `print_menu()`, `get_book_details()`, `print_books()` | **Low** — pure functions with no I/O side effects; `BOOKS_CASE_SENSITIVE` env var is the only toggle |
| `book_app.py` | `samples/book-app-project/book_app.py` | Interactive CLI entry point — wires `BookCollection` + `utils` into a REPL loop | **Low** — UI only; no business logic; excluded from coverage target |
| `bench_find.py` | `samples/book-app-project/bench_find.py` | Stand-alone micro-benchmark for `find_book_by_title` using `timeit` | **Low** — measurement only; never imported by production code |
| `pyproject.toml` | `samples/book-app-project/pyproject.toml` | Build config, pytest config, coverage settings, ruff lint config | **Medium** — changes here affect CI and all developer tool invocations |
| `run-tests.ps1` | `samples/book-app-project/run-tests.ps1` | Local PowerShell test script — runs pytest + ruff + bandit in one command | **Low** — CI fallback script; safe to modify |
| `data.json` | `samples/book-app-project/data.json` | Runtime persistence file — written by `BookCollection.save_books()` | **Low** for dev; **do not commit real user data** |
| `tests/test_books.py` | `samples/book-app-project/tests/test_books.py` | Primary test suite — unit + contract + resilience tests (38 tests) | **Low** — tests only; monkeypatched to use `tmp_path`, never touches real `data.json` |
| `tests/test_feature_flags.py` | `samples/book-app-project/tests/test_feature_flags.py` | Feature-flag tests — validates `BOOKS_CASE_SENSITIVE` ON/OFF behavior (14 tests) | **Low** |

---

## Related ai-track-docs

| Doc | Purpose |
|---|---|
| [extending-books.md](extending-books.md) | How to add fields, new methods, tune `backoff`, verify structured logging |
| [build-test.md](build-test.md) | Exact commands to run tests, coverage, ruff, bandit |
| [resilience.md](resilience.md) | Retry parameters, tuning guidance, rollback steps |
| [contract-tests.md](contract-tests.md) | Boundary contracts for `add_book` / `list_books` return shapes |
| [feature-flags.md](feature-flags.md) | `BOOKS_CASE_SENSITIVE` flag lifecycle and ON/OFF validation |
| [logging.md](logging.md) | Structured log fields (`op`, `status`, `elapsed_ms`) and how to view locally |
| [perf-baseline.md](perf-baseline.md) | `find_book_by_title` benchmark baseline numbers |
| [security.md](security.md) | Security scan results, bandit suppressions, `.gitignore` hygiene |
| [static-analysis.md](static-analysis.md) | Ruff configuration, suppressions, how to run locally |
| [dependencies.md](dependencies.md) | Pinned dependency policy and upgrade notes |

---

## Risk Notes

- **`books.py`** is the highest-risk file in the subsystem. Any change to `_save_with_retry`, `add_book`, or `remove_book` must be accompanied by a test and a rollback note.
- **`pyproject.toml`** controls pytest, coverage thresholds, and ruff strictness — changes here silently affect all contributors.
- **`data.json`** must never contain real user data. It is safe to delete and let the app recreate it on first run.
- **`utils.py`** is safe to extend; the `BOOKS_CASE_SENSITIVE` toggle is the only behavioral flag and is fully tested.

---

## Rollback

Any change in this subsystem can be reverted with:

```powershell
git revert <commit-SHA>
```

No database migrations. No config state. Re-running `pytest -v` from `samples/book-app-project/` is the full validation step.
