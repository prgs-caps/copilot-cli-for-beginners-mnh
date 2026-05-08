# Coverage

## Overview

Test coverage is measured with [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/).
Coverage runs automatically on every `pytest` invocation via `addopts` in `pyproject.toml`.

## Install

```powershell
pip install pytest-cov
```

Or install the full dev extras:

```powershell
pip install -e ".[dev]"
```

## Run Coverage

```powershell
# From samples/book-app-project/
pytest -v
```

Coverage is enabled by default (`addopts = "--cov=. --cov-report=term-missing"` in `pyproject.toml`).

To run coverage explicitly or override the report format:

```powershell
pytest --cov=. --cov-report=term-missing -v
```

## Sample Output

```
================================= tests coverage =================================
________________ coverage: platform win32, python 3.13.9-final-0 _________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
bench_find.py            28     28     0%   8-48
book_app.py              57     57     0%   1-98
books.py                 72      1    99%   137
tests\test_books.py      94      0   100%
utils.py                 27     27     0%   1-36
---------------------------------------------------
TOTAL                   278    113    59%
=============================== 15 passed in 0.23s ===============================
```

> **Note:** The low TOTAL (59%) reflects that `bench_find.py`, `book_app.py`, and `utils.py` have no tests — they are out of scope for this exercise. The core module under test (`books.py`) is at 99%.

## Configuration

Coverage is configured in `samples/book-app-project/pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=term-missing"
```

To omit coverage for a single run (e.g. quick smoke test):

```powershell
pytest --no-cov -v
```

## PR Snippet Template

Copy this block into every PR description under the **Evidence** section:

```
Coverage
- Command: pytest --cov=. --cov-report=term-missing -v
- Total: <TOTAL>%
- Uncovered lines (if any): <file>:<lines>
- All existing tests: PASSED
```

**Example (filled in — Walk Ex 2 baseline):**

```
Coverage
- Command: pytest --cov=. --cov-report=term-missing -v
- Total: 59% (books.py: 99%, bench_find.py/book_app.py/utils.py not under test)
- Uncovered lines: books.py:137
- All existing tests: PASSED (15/15)
```

## Rollback

To remove coverage from the default test run:

1. In `pyproject.toml`, remove or comment out the `[tool.pytest.ini_options]` section.
2. Uninstall if desired: `pip uninstall pytest-cov`

No source files are modified — this is purely a dev tooling change.
