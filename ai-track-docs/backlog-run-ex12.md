# Run Ex 12 — Backlog Analysis: book-app-project Subsystem

Generated: 2026-05-14  
Scope: `samples/book-app-project/` + `.github/workflows/book-app-ci.yml`  
Method: Copilot-assisted subsystem sweep following Runs Ex 1–11

---

## Item 1 — Add CI push branch filter (P2 · Size: S)

**Problem**  
`.github/workflows/book-app-ci.yml` triggers on every `push` event with no `branches` filter.
This causes CI to run on every branch push — including ephemeral work-in-progress branches
that have no open PR — wasting runner minutes and generating noise.

**Acceptance Criteria**
- `on: push` block includes a `branches` filter scoped to `main` and the `run/**` / `walk/**` / `crawl/**` prefixes
- `on: pull_request` trigger is unaffected
- CI still triggers correctly on branch push and PR open
- Change documented in `ai-track-docs/ci-reliability.md`

**Code Path**  
`.github/workflows/book-app-ci.yml` — `on:` block, lines 1–8

**Rollback**  
Remove the `branches:` key from `on: push`; reverts to triggering on all pushes.

---

## Item 2 — Pin GitHub Actions to commit SHAs (P2 · Size: S)

**Problem**  
`book-app-ci.yml` uses `actions/checkout@v4` and `actions/setup-python@v5` — mutable
major-version tags. A tag can be silently moved to a different commit, allowing a
supply-chain compromise to inject code into the CI pipeline without any diff being visible.

**Acceptance Criteria**
- `actions/checkout` and `actions/setup-python` references replaced with full commit SHAs
  (with a trailing `# vX.Y.Z` comment for human readability)
- SHA values verified against the official action repositories at time of change
- No functional change to CI behavior; all tests still pass

**Code Path**  
`.github/workflows/book-app-ci.yml` — lines 17 and 19 (`uses:` entries)

**Rollback**  
Revert to tag references (e.g. `actions/checkout@v4`); or `git revert <SHA>`.

---

## Item 3 — Enforce coverage threshold in CI (P2 · Size: S)

**Problem**  
CI reports coverage (currently ~75%) but does not fail if coverage drops below an accepted
floor. A PR that deletes tests or skips previously-covered branches would pass CI silently.

**Acceptance Criteria**
- `pytest` step in `book-app-ci.yml` passes `--cov-fail-under=75` (or equivalent
  `[tool.coverage.report] fail_under = 75` in `pyproject.toml`)
- CI build fails when coverage falls below the threshold
- Threshold documented in `ai-track-docs/ci-reliability.md`
- All 41 existing tests still pass; current coverage (~75%) meets the floor

**Code Path**  
`.github/workflows/book-app-ci.yml` — pytest step (`run:` block)  
`samples/book-app-project/pyproject.toml` — `[tool.pytest.ini_options]` or `[tool.coverage.report]`

**Rollback**  
Remove `--cov-fail-under` flag (or `fail_under` key) and redeploy.

---

## Item 4 — Add structured logging to `handle_find` (P3 · Size: S)

**Problem**  
`book_app.py::handle_find()` is the only command handler with no observability. All other
handlers (`handle_list`, `handle_add`, `handle_remove`) gained structured logging in Run Ex 9
with consistent fields (`op`, `status`, `elapsed_ms`). The gap means find-command failures
produce no log signal, making triage harder.

**Acceptance Criteria**
- `handle_find` logs `INFO cmd_find` with `op`, `status=found`, `title`, `elapsed_ms` on hit
- Logs `WARNING cmd_find` with `op`, `status=not_found`, `title`, `elapsed_ms` on miss
- Existing 41 tests still pass; at least one new test covers the log path
- `ai-track-docs/logging.md` updated with the new instrumented path

**Code Path**  
`samples/book-app-project/book_app.py` — `handle_find()` function (line 76)

**Rollback**  
Remove the `logger.*` calls from `handle_find`; no behavior change.

---

## Item 5 — Implement `BookCollection.update_book()` (P3 · Size: M)

**Problem**  
`books.py::BookCollection` exposes `add_book` and `remove_book` but has no `update_book`
method. Any caller that needs to change a book's title or year must do a remove + add round
trip, which is fragile (loses position in the list) and bypasses the retry/logging pattern
already in place for the other mutating operations.

**Acceptance Criteria**
- `update_book(old_title, new_title, new_year)` method added to `BookCollection`
- Method raises `ValueError` if `old_title` is not found (consistent with `remove_book`)
- Validates `new_year` using the same rules as `add_book`
- Calls `_save_with_retry` and emits structured log entries (`op=update_book`, `status=ok|not_found`)
- At least 3 new tests: happy path, not-found, invalid-year
- `ai-track-docs/SYSTEM-OVERVIEW.md` updated to document the completed CRUD surface

**Code Path**  
`samples/book-app-project/books.py` — `BookCollection` class (after `remove_book`)  
`samples/book-app-project/test_books.py` — new test class `TestUpdateBook`

**Rollback**  
Remove the `update_book` method; no other code references it at time of addition.

---

## Summary Table

| # | Title | Priority | Size | Code Path |
|---|-------|----------|------|-----------|
| 1 | CI push branch filter | P2 | S | `book-app-ci.yml` `on:` block |
| 2 | Pin Actions to SHAs | P2 | S | `book-app-ci.yml` lines 17–19 |
| 3 | Coverage threshold enforcement | P2 | S | `book-app-ci.yml` + `pyproject.toml` |
| 4 | Structured logging in `handle_find` | P3 | S | `book_app.py::handle_find()` |
| 5 | `BookCollection.update_book()` | P3 | M | `books.py::BookCollection` |
