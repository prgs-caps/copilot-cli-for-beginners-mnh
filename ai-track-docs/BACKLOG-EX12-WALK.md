# Walk Ex 12 — Backlog & Epics

**Epic: book-app reliability and UX hardening**

Observations drawn from Walk exercises 1–11. Each issue is scoped small enough to land in one PR. No tracker access — items committed here as the canonical backlog artifact.

---

## Issue 1 — Atomic `save_books` write to prevent data corruption

**File:** `samples/book-app-project/books.py` — `BookCollection.save_books` (~line 55)

**Observation:**  
`open(DATA_FILE, "w")` truncates the file before writing begins. If the process crashes mid-write (e.g. disk full, SIGKILL), `data.json` is left empty or partially written. `load_books` handles `json.JSONDecodeError` with a warning and an empty collection — silently discarding all data.

**Proposed fix:**  
Write to a temporary file in the same directory, then call `os.replace(tmp, DATA_FILE)`. `os.replace` is atomic on POSIX and near-atomic on Windows (same-volume rename).

**Acceptance criteria:**
- [ ] `save_books` writes to `<DATA_FILE>.tmp` then renames
- [ ] A test simulates a corrupted file and confirms the original is not touched on error
- [ ] Existing tests remain green

**Code link:** [books.py#save_books](../samples/book-app-project/books.py)

---

## Issue 2 — Surface "book not found" feedback in `handle_remove`

**File:** `samples/book-app-project/book_app.py` — `handle_remove` (~line 45)

**Observation:**  
`remove_book` returns `True` (found) or `False` (not found), but `handle_remove` discards the return value and always prints `"Book removed if it existed."` — giving users no confirmation either way.

**Proposed fix:**  
Capture the return value and branch:
```python
if collection.remove_book(title):
    print("\nBook removed.\n")
else:
    print("\nBook not found.\n")
```

**Acceptance criteria:**
- [ ] `handle_remove` uses the bool return value
- [ ] Manual smoke test: remove existing title → "Book removed."; remove unknown title → "Book not found."
- [ ] No new test file required (behavior is CLI I/O, covered by manual check; a test with `capsys` is a bonus)

**Code link:** [book_app.py#handle_remove](../samples/book-app-project/book_app.py)

---

## Issue 3 — Replace silent `year=0` fallback in `utils.get_book_details`

**File:** `samples/book-app-project/utils.py` — `get_book_details` (~line 30)

**Observation:**  
When the user types a non-numeric year, `get_book_details` catches the `ValueError`, prints `"Invalid year. Defaulting to 0."` and passes `year=0` to `add_book`. `add_book` then raises `ValueError("year must be a positive integer")` — a second, harder-to-understand error from deep inside the library. The validation boundary is at the wrong layer.

**Proposed fix:**  
Re-prompt the user (or raise immediately) instead of coercing to 0:
```python
try:
    year = int(year_input)
    if year <= 0:
        raise ValueError
except ValueError:
    print("Invalid year. Please enter a positive integer.")
    return None  # or re-prompt in a loop
```
Caller (`book_app.main`) handles `None` gracefully.

**Acceptance criteria:**
- [ ] `get_book_details` never returns `year=0`
- [ ] User sees one clear error message, not two
- [ ] `test_add_book_invalid_year_raises` still passes (validation in `_validate_book_fields` is a backstop, not primary)

**Code link:** [utils.py#get_book_details](../samples/book-app-project/utils.py)

---

## Issue 4 — Add missing tests for `find_by_author`

**File:** `samples/book-app-project/tests/test_books.py`

**Observation:**  
`BookCollection.find_by_author` is called from `book_app.handle_find` and is part of the public API, but has zero test coverage. Three important cases are untested: no match, single match, multiple matches (and case-insensitive matching).

**Proposed fix:**  
Add three parametrised or separate tests:
1. `find_by_author` with no matching books → returns `[]`
2. `find_by_author` with one match → returns list of length 1
3. `find_by_author` case-insensitive → `"frank herbert"` finds `"Frank Herbert"`

**Acceptance criteria:**
- [ ] Three new tests added to `tests/test_books.py`
- [ ] `pytest -v --cov=. --cov-report=term-missing` shows `find_by_author` fully covered
- [ ] Coverage total does not decrease

**Code link:** [tests/test_books.py](../samples/book-app-project/tests/test_books.py) · [books.py#find_by_author](../samples/book-app-project/books.py)

---

## Issue 5 — Cache pip dependencies in CI to reduce run time

**File:** `.github/workflows/book-app-ci.yml` — `actions/setup-python@v5` step

**Observation:**  
The CI workflow installs all dependencies fresh on every run (`pip install -e ".[dev]"`). There is no `cache: 'pip'` on the `setup-python` step. For small projects this costs ~15–25 s per run; the fix is one line.

**Proposed fix:**  
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.13"
    cache: 'pip'
    cache-dependency-path: 'samples/book-app-project/pyproject.toml'
```

**Acceptance criteria:**
- [ ] `cache: 'pip'` added with `cache-dependency-path` pointing to `pyproject.toml`
- [ ] CI run after the change shows "Cache restored" in the setup-python step log
- [ ] Job still passes end-to-end

**Code link:** [.github/workflows/book-app-ci.yml](../.github/workflows/book-app-ci.yml)

---

## Rollback

This file is documentation only. To roll back: `git revert <SHA>` or delete `ai-track-docs/BACKLOG-EX12-WALK.md` and amend the branch.
