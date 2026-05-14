# CI Reliability — book-app-ci.yml

**Run Ex 10 — 2026-05-14**  
**File:** `.github/workflows/book-app-ci.yml`

---

## Changes Applied

### 1. pip dependency caching

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.13"
    cache: "pip"
    cache-dependency-path: samples/book-app-project/pyproject.toml
```

**Why:** Without caching, every CI run re-downloads all packages from PyPI. With `cache: "pip"`, GitHub Actions stores the downloaded wheels keyed on `pyproject.toml`'s hash. Subsequent runs restore the cache in seconds instead of re-downloading.

**Impact:** Typical install time drops from ~30–45 s to ~3–5 s on cache hit. Cache is automatically invalidated when `pyproject.toml` changes.

**Rollback:** Remove the `cache` and `cache-dependency-path` lines from the `actions/setup-python` step.

---

### 2. Job-level timeout

```yaml
jobs:
  test:
    timeout-minutes: 10
```

**Why:** Without a timeout, a hung test (e.g. waiting on missing input or a deadlocked resource) will hold a GitHub Actions runner for up to 6 hours. A 10-minute cap is generous for this suite (which normally completes in < 60 s) and prevents queue starvation.

**Impact:** Job auto-cancels after 10 minutes. Alert: if a future test is expected to run longer, raise this value in the same PR.

**Rollback:** Remove the `timeout-minutes: 10` line.

---

### 3. Hardened test gate (remove `continue-on-error`)

**Before:**
```yaml
- name: Run tests with coverage
  id: run-tests
  continue-on-error: true
```

**After:**
```yaml
- name: Run tests with coverage
  id: run-tests
```

**Why:** `continue-on-error: true` meant a test failure would not fail the CI job — reviewers had no automatic signal that the suite was broken. The coverage summary step already uses `if: always()`, so it still posts even when tests fail.

**Impact:** A failing test now fails the CI job (red ✗). The coverage summary still appears in the job summary for diagnostics.

**Rollback:** Re-add `continue-on-error: true` to the `run-tests` step.

---

## How to Validate

Run tests locally before pushing to confirm green:

```powershell
cd samples/book-app-project
pytest -v
```

Expected: `41 passed`.

After pushing, check the **Actions** tab on GitHub. The job should:
1. Show a cache restore step (yellow on first run, green on subsequent runs)
2. Complete in well under 10 minutes
3. Fail the job (not just a step) if any test fails

---

## Rollback (all 3 changes)

```powershell
git revert <SHA>
```

Or revert individual lines described in each section above. No code behavior is affected — this is CI configuration only.
