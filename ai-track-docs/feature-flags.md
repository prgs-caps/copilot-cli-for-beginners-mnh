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

---

## Flag Lifecycle

### 1. Introduce (default OFF)
Add the env-var guard in the target function. Default behaviour is unchanged.
No tests need updating — existing tests pass as-is.

### 2. Enable & validate
Set `BOOKS_CASE_SENSITIVE=1` in the target environment and run the test suite:

```powershell
# Windows PowerShell
$env:BOOKS_CASE_SENSITIVE = "1"
cd samples/book-app-project
pytest tests/test_feature_flags.py -v
Remove-Item Env:\BOOKS_CASE_SENSITIVE
```

```bash
# Linux/macOS
BOOKS_CASE_SENSITIVE=1 pytest samples/book-app-project/tests/test_feature_flags.py -v
```

Expected: all `*_flag_on` tests pass, all `*_flag_off` tests still pass.

### 3. Ship
Deploy with the env var set (or unset) for the target audience.
No code change required to toggle.

### 4. Rollback
Unset (or remove) `BOOKS_CASE_SENSITIVE` to revert to case-insensitive behaviour
instantly, without a code change or restart.

### 5. Remove (when stable)
Once the flag has been ON in production for a release cycle and no rollback is
needed, inline the chosen behaviour and delete the env-var branch.
Update tests to remove `monkeypatch` calls.

---

## Validation Evidence (CI)

The CI workflow (`book-app-ci.yml`) runs the full test suite on every push.
To validate both modes in CI, run two separate commands:

```yaml
# In .github/workflows/book-app-ci.yml (optional matrix extension)
env:
  BOOKS_CASE_SENSITIVE: "1"   # or omit for OFF
```

For local evidence capture:

```powershell
# OFF (default)
pytest tests/test_feature_flags.py -v 2>&1 | Tee-Object flag-off.txt

# ON
$env:BOOKS_CASE_SENSITIVE = "1"
pytest tests/test_feature_flags.py -v 2>&1 | Tee-Object flag-on.txt
Remove-Item Env:\BOOKS_CASE_SENSITIVE
```
