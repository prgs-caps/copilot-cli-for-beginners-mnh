# Resilience & Failure Scenarios

Documents the failure scenarios covered by the Ex15 resilience test suite
in `samples/book-app-project/tests/test_books.py`.

## Scenarios

| # | Test | Failure Scenario | Expected Behaviour |
|---|------|------------------|--------------------|
| 1 | `test_corrupted_data_file_starts_empty` | `data.json` contains invalid JSON | Collection initialises empty; no exception raised |
| 2 | `test_missing_data_file_starts_empty` | `data.json` does not exist | Collection initialises empty; no exception raised |
| 3 | `test_remove_already_removed_book_returns_false` | `remove_book` called on a title that was already removed | Returns `False`; collection length unchanged at 0 |
| 4 | `test_mark_as_read_idempotent` | `mark_as_read` called twice on the same book | Returns `True` both times; `book.read` stays `True` |

## Why these matter

- **Corrupted / missing file**: The JSON file is the only persistence layer. If it
  is absent or malformed (e.g. after a failed write or manual edit), the application
  must not crash on startup.
- **Double-remove**: Callers should be able to attempt removal without checking
  existence first; a safe `False` return prevents silent state corruption.
- **Idempotent mark-as-read**: Re-marking a book (e.g. after a UI retry) must not
  cause errors or flip the `read` flag back to `False`.

## Running the resilience tests

```powershell
cd samples/book-app-project
pytest -v -k "corrupted or missing or already_removed or idempotent"
```
