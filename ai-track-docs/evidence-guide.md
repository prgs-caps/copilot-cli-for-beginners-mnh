# Evidence Surfacing Guide

> **Purpose:** Standardize how evidence (test output, logs, metrics) is captured and presented in every PR so reviewers always know what to look for and trust is built incrementally.

---

## The Evidence Pattern

Every PR in this repo MUST include an **Evidence** section with at least one concrete artifact. Use this template:

```markdown
## Evidence

| Type    | Command                                                      | Result                  |
|---------|--------------------------------------------------------------|-------------------------|
| Tests   | `cd samples/book-app-project && pytest -v`                   | 36 passed, 0 failed     |
| Lint    | `ruff check samples/book-app-project/`                       | All checks passed       |
| Security| `bandit -r samples/book-app-project/ -ll`                    | No issues found         |
| Coverage| `pytest --cov=. --cov-report=term-missing`                   | 99% (books.py)          |
```

Include only the rows relevant to your change. At minimum, always include **Tests**.

---

## Step-by-Step: Capturing Evidence Before Opening a PR

### 1. Run tests and save output

```powershell
cd samples/book-app-project
pytest -v 2>&1 | Tee-Object -FilePath "$env:TEMP\pytest-output.txt"
```

Paste the last 10–15 lines (the summary) into the PR Evidence section.

### 2. Run coverage (optional but recommended)

```powershell
pytest --cov=. --cov-report=term-missing 2>&1 | Tee-Object -FilePath "$env:TEMP\coverage-output.txt"
```

Record the `TOTAL` line from the output, e.g.:

```
TOTAL    142     1    99%
```

### 3. Run lint (if applicable)

```powershell
ruff check samples/book-app-project/
```

Record: `All checks passed` or list findings fixed.

### 4. Run security scan (if applicable)

```powershell
bandit -r samples/book-app-project/ -ll
```

Record: `No issues identified` or summarize findings addressed.

---

## PR Evidence Section Template

Copy this block into every PR description and fill in the results:

```markdown
## Evidence

**Tests:**
```
pytest -v
36 passed in 0.42s
```

**Coverage** *(if changed)*:
```
pytest --cov=. --cov-report=term-missing
TOTAL    142     1    99%
```

**Lint** *(if linting changed)*:
```
ruff check samples/book-app-project/
All checks passed.
```

**Security** *(if security-relevant change)*:
```
bandit -r samples/book-app-project/ -ll
No issues identified.
```
```

---

## Evidence Artifact Reference Table

| Evidence Type | When Required             | Command                                          | What to Record              |
|---------------|---------------------------|--------------------------------------------------|-----------------------------|
| Test results  | Always                    | `pytest -v`                                      | Pass/fail counts + duration |
| Coverage      | When logic changes        | `pytest --cov=. --cov-report=term-missing`       | TOTAL % line                |
| Lint          | When style/lint changes   | `ruff check <path>`                              | "All passed" or fixed count |
| Security scan | When security-relevant    | `bandit -r <path> -ll`                           | Finding count or "none"     |
| Perf baseline | When perf-relevant        | `python -m timeit` or custom benchmark           | Before/after ms             |

---

## Rollback

This file is documentation only. To roll back:
```
git revert <commit-sha>   # removes evidence-guide.md
```

No code changes were introduced in this exercise.

---

## Reuse

Reference this guide in PRs with:
> Evidence captured per `ai-track-docs/evidence-guide.md`.
