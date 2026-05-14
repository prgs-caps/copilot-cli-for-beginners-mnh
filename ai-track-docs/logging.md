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
"
```

Expected output:
```
DEBUG books book_added | op=add_book status=ok elapsed_ms=<n>
```

## Notes

- Log output is suppressed in tests — `pytest` does not configure the root logger.
- Only `add_book` is instrumented in this baseline; extend to `mark_as_read` and `remove_book` following the same pattern.
- To persist logs to a file, add a `FileHandler` to the logger configuration.
