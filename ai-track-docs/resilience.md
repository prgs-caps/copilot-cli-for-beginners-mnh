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

---

## Walk Ex 15 — Save Retry / Backoff

### What was added

`BookCollection._save_with_retry()` wraps the `data.json` write with a simple
retry loop and exponential back-off. `save_books()` now delegates to this helper
so all persistence paths (add, mark-as-read, remove) automatically inherit the
protection.

```
add_book()     ─┐
mark_as_read() ─┤─▶ save_books() ─▶ _save_with_retry()
remove_book()  ─┘
```

### Parameters and tuning

| Parameter | Default | Notes |
|-----------|---------|-------|
| `max_attempts` | `3` | Total write attempts before re-raising |
| `initial_delay` | `0.05 s` | Wait before the first retry; doubles each attempt |

Retry timeline with defaults:

| Attempt | Sleep before attempt |
|---------|----------------------|
| 1       | — (no sleep)         |
| 2       | 0.05 s               |
| 3       | 0.10 s               |
| fail    | OSError re-raised    |

**Increase `max_attempts`** if the deployment environment has a network-attached
file share with higher latency spikes.  
**Increase `initial_delay`** if the storage layer needs longer to recover between
burst writes.

### Failure tests added (Walk Ex 15)

| Test | Scenario | Expected behaviour |
|------|----------|--------------------|
| `test_save_with_retry_succeeds_after_transient_oserror` | First write raises `OSError`; second succeeds | Returns normally; data persisted |
| `test_save_with_retry_raises_after_max_attempts` | Every write raises `OSError` | `OSError` re-raised after exhausting all attempts |

Run just the Ex 15 retry tests:

```powershell
cd samples/book-app-project
pytest -v -k "retry"
```

### Rollback

To remove the retry helper and revert `save_books()` to a single-attempt write:

```powershell
git revert <ex15-commit-hash>
```

Or manually: delete `_save_with_retry()` and restore `save_books()` to:

```python
def save_books(self):
    with open(DATA_FILE, "w") as f:
        json.dump([asdict(b) for b in self.books], f, indent=2)
```

No schema or data-file format changes were made; rollback is purely additive-code
removal and carries zero data-migration risk.

