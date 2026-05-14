# Build & Test

## Chosen Module

`samples/book-app-project/books.py` — `BookCollection` class with add/list/find/mark-as-read/remove operations.

## Install Dependencies

```powershell
pip install pytest
```

## Run Tests

```powershell
# From repo root:
cd samples/book-app-project
pytest -v
```

## Expected Output

```
collected 6 items

tests/test_books.py::test_add_book PASSED
tests/test_books.py::test_mark_book_as_read PASSED
tests/test_books.py::test_mark_book_as_read_invalid PASSED
tests/test_books.py::test_remove_book PASSED
tests/test_books.py::test_remove_book_invalid PASSED
tests/test_books.py::test_list_books_returns_empty_for_new_collection PASSED

6 passed
```

## Notes

- Tests are hermetic: each test gets an isolated `tmp_path` JSON file via `autouse` fixture — no shared state.
- No build step required; Python is interpreted.

## Local Test Script (CI Fallback)

A repeatable script is available for anyone on the team:

```powershell
# From repo root:
pwsh -File samples/book-app-project/run-tests.ps1
```

The script (`samples/book-app-project/run-tests.ps1`):
1. Navigates to the correct directory automatically
2. Installs/verifies pytest (`>=9.0,<10`)
3. Runs `pytest -v`
4. Exits with pytest's exit code (0 = all passed)

No CI workflow currently exists for this sub-project. This script is the repeatable baseline until one is added.
