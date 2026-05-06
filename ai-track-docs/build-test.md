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
