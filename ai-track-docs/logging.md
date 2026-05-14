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
