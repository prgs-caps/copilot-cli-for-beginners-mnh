# Feature Flags

## BOOKS_CASE_SENSITIVE

| Setting | Behavior |
|---------|----------|
| unset or any value other than `1` | Title matching is **case-insensitive** (default) |
| `1` | Title matching is **case-sensitive** |

**Affected operations:** `find_book_by_title`, `mark_as_read`, `remove_book`  
**Implementation:** `BookCollection._titles_match` in `samples/book-app-project/books.py`

### Usage

```powershell
# Enable case-sensitive mode for a single pytest run
$env:BOOKS_CASE_SENSITIVE = "1"; pytest -v; Remove-Item Env:\BOOKS_CASE_SENSITIVE
```

```bash
# Linux/macOS
BOOKS_CASE_SENSITIVE=1 pytest -v
```

### Rationale

Case-insensitive matching is the safe, user-friendly default (preserves all
existing behaviour). The flag exists to allow environments where exact-case
titles are required (e.g. data-migration scripts that must distinguish
"Dune" from "dune") to opt in without a code change.

### Risk

Low. The default path is unchanged. The flag is read at call-time via
`os.environ.get`, so it can be toggled per-process without restart.
