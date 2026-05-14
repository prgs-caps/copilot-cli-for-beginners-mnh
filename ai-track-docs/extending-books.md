# Extending BookCollection

`BookCollection` lives in `samples/book-app-project/books.py`.
It stores a list of `Book` dataclass instances and persists them to a JSON file.

---

## Add a new field to Book

1. Add the field to the `@dataclass`:
   ```python
   genre: str = ""

---

## Tuning the save-retry behaviour (Run Ex 3)

`_save_with_retry` in `books.py` accepts three keyword arguments:

| Param | Default | Notes |
|---|---|---|
| `max_attempts` | `3` | Total write attempts before re-raising `OSError` |
| `initial_delay` | `0.05` s | Sleep time before the first retry |
| `backoff` | `2.0` | Multiplier applied to `delay` after each failure |

**Examples:**

```python
# Exponential backoff (default): 0.05 s → 0.1 s → 0.2 s …
collection._save_with_retry()

# Linear backoff: 0.1 s → 0.1 s → 0.1 s …
collection._save_with_retry(initial_delay=0.1, backoff=1.0)

# Fast retry for tests (no sleep):
collection._save_with_retry(max_attempts=2, initial_delay=0)
```

**Rollback:** if you need to revert to the previous hardcoded `delay *= 2` behaviour,
set `backoff=2.0` (already the default) — no code change needed.

---

## Structured logging in load_books (Run Ex 3)

Corrupted JSON now emits a `logger.warning("load_books_corrupt", ...)` instead of
`print(...)`. To surface these warnings locally:

```powershell
cd samples/book-app-project
python -c "
import logging, books
logging.basicConfig(level=logging.WARNING)
b = books.BookCollection()
"
```

To suppress the warning in tests, use `caplog` or `monkeypatch` on the logger.
See `tests/test_books.py::test_load_books_corrupt_uses_logger_not_print` for an example.