# CI Soft Gating (Walk Ex 10)

## Workflow: `book-app-ci.yml`

**File:** `.github/workflows/book-app-ci.yml`

Runs on every push and pull request. Executes `pytest` with coverage in
`samples/book-app-project/` and writes the results to the GitHub Actions job
summary. CI is **non-blocking**: a test failure surfaces as a visible warning
in the summary but never prevents a merge.

## What it does

| Step | Detail |
|---|---|
| `Run tests with coverage` | `pytest -v --cov=. --cov-report=term-missing --cov-report=json` with `continue-on-error: true` |
| `Post coverage summary` | Appends total coverage % and full pytest output to `$GITHUB_STEP_SUMMARY` (runs even if tests fail via `if: always()`) |

## How to view the summary

1. Open the PR on GitHub.
2. Click the **Checks** tab → select **book-app CI (soft gate)** → **pytest + coverage summary**.
3. Scroll to the **Summary** panel on the right — coverage % and test output are listed there.

## How to run locally (equivalent)

```bash
cd samples/book-app-project
pytest -v --cov=. --cov-report=term-missing
```

## Rollback

To disable the workflow without deleting it, rename it to
`.github/workflows/book-app-ci.yml.bak` (mirrors the existing
`generate-demos.yml.bak` pattern in this repo) or add a
`branches-ignore: ['**']` filter under `on:`.

To remove entirely: `git rm .github/workflows/book-app-ci.yml`.
