# Structured Logging — book-app-project

## What is logged

`books.py` uses Python's standard `logging` module with a module-level logger:

```python
logger = logging.getLogger(__name__)  # name: "books"
```

### Instrumented path: `add_book`

Every successful `add_book` call emits a `DEBUG` record with these fields:

| Field | Value |
|-------|-------|
| `op` | `"add_book"` |
| `status` | `"ok"` |
| `title` | The title that was added |
| `elapsed_ms` | Time taken for append + save, in milliseconds |

### Instrumented path: `remove_book` (Walk Ex 9)

Every `remove_book` call emits a `DEBUG` record. Two outcomes are covered:

| Field | Found case | Not-found case |
|-------|------------|----------------|
| `op` | `"remove_book"` | `"remove_book"` |
| `status` | `"ok"` | `"not_found"` |
| `title` | The title requested | The title requested |
| `elapsed_ms` | Time taken for scan + pop + save, in ms | Time taken for full scan, in ms |

## How to view logs locally

Logging is off by default. To enable it, configure the root logger before calling any `BookCollection` methods.

### Option 1 — quick one-liner in a script

```python
import logging
logging.basicConfig(level=logging.DEBUG, format="%(name)s %(message)s %(op)s %(status)s %(elapsed_ms)s")
```

### Option 2 — run the app with logging enabled

```powershell
cd samples/book-app-project
python -c "
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(name)s %(message)s | op=%(op)s status=%(status)s elapsed_ms=%(elapsed_ms)s')
import books
from books import BookCollection
col = BookCollection()
col.add_book('Dune', 'Frank Herbert', 1965)
col.remove_book('Dune')
col.remove_book('Missing Title')
"
```

Expected output:
```
DEBUG books book_added       | op=add_book    status=ok        elapsed_ms=<n>
DEBUG books book_removed     | op=remove_book status=ok        elapsed_ms=<n>
DEBUG books book_remove_miss | op=remove_book status=not_found elapsed_ms=<n>
```

## Notes

- Log output is suppressed in tests — `pytest` does not configure the root logger.
- `add_book` and `remove_book` are both instrumented; extend to `mark_as_read` following the same pattern.
- To persist logs to a file, add a `FileHandler` to the logger configuration.

---

## Run Ex 9 — Observability Sweep (Folder-Level)

**Date:** 2026-05-13  
**Files instrumented:** `book_app.py`, `utils.py`

### New instrumented paths

#### `book_app.py` — module logger: `"book_app"`

| Path | Level | Event key | Fields |
|------|-------|-----------|--------|
| `handle_list` | DEBUG | `cmd_list` | `op`, `status`, `count`, `elapsed_ms` |
| `handle_add` (success) | INFO | `cmd_add` | `op`, `status`, `title`, `elapsed_ms` |
| `handle_add` (error) | WARNING | `cmd_add_failed` | `op`, `status`, `error` |
| `handle_remove` | INFO | `cmd_remove` | `op`, `status` (`ok`/`not_found`), `title` |
| `main` (unknown command) | WARNING | `cmd_unknown` | `op`, `status`, `command` |

#### `utils.py` — module logger: `"utils"`

| Path | Level | Event key | Fields |
|------|-------|-----------|--------|
| `get_book_details` (bad year) | WARNING | `invalid_year_input` | `op`, `status`, `input` |

### How to validate (local)

```powershell
cd samples/book-app-project
python -c "
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(name)s %(message)s | op=%(op)s status=%(status)s'
)
import book_app
import books, tempfile, os
books.DATA_FILE = tempfile.mktemp(suffix='.json')
book_app.collection = books.BookCollection()
book_app.collection.add_book('Dune', 'Frank Herbert', 1965)
book_app.handle_list()
"
```

Expected log output includes:
```
DEBUG  book_app cmd_list   | op=handle_list   status=ok
```

### Rollback

`git revert <SHA>` removes all Run Ex 9 log statements from `book_app.py` and `utils.py`.

