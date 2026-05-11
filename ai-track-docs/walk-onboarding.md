# Walk Workflow — Onboarding Guide

This guide describes the plan-first contribution workflow used at the Walk level of the AI Engineering Track. Follow it for every Walk exercise.

---

## What is the Walk level?

At Walk, you use GitHub Copilot as a **pair** — you write the plan, Copilot produces the diffs. Changes span 2–4 files per PR. Every PR includes coverage or contract evidence and a rollback path.

---

## Step-by-step workflow

### 1. Create your branch

Branch off the prior exercise's branch (not `main`):

```powershell
git checkout -b walk/<your-github-id>/ex<N>-<short-name>
```

Example: `walk/maharvey-prgs/ex4-contributing-onboarding`

### 2. Write the plan first

Before editing any file, decide:
- Which files will change and why
- What tests will verify the behavior

Include this plan in your PR description under `## Plan`.

### 3. Send the Walk prompt to Copilot Chat

Use this pattern at the end of every Walk prompt:

```
Create a plan first: list steps and files to change.
Then produce diffs file-by-file.
Include: test strategy, evidence to capture (coverage/contract), and rollback.
Keep scope small and reviewable.
Avoid submodules/vendor folders.
```

### 4. Apply changes

Copilot applies all file changes. You do not edit files manually.

### 5. Run tests

From `samples/book-app-project/`:

```powershell
pytest -v
```

With coverage:

```powershell
pytest -v --cov=. --cov-report=term-missing
```

All tests must pass before committing.

### 6. Commit

```powershell
git add <files>
git commit -m "Walk Ex <N>: <short description>"
```

### 7. Push

```powershell
git push -u origin walk/<your-github-id>/ex<N>-<short-name>
```

### 8. Open the PR

```powershell
gh pr create \
  --base walk/<your-github-id>/ex<N-1>-<prior-name> \
  --head walk/<your-github-id>/ex<N>-<short-name> \
  --title "GHCP - Walk: Ex<N> <title>" \
  --body-file "$env:TEMP\pr-body.txt"
```

---

## PR body template

```
## Plan
- Step 1: ...
- Step 2: ...

Files touched:
- path/to/file1
- path/to/file2

## Evidence
- Command: pytest -v
- Result: N/N passed
- Coverage: XX%

## Risk and Rollback
- Risk: low
- Rollback: git revert <SHA>

## Track
- Level: Walk
- Exercise: Ex<N>
```

---

## Key rules

| Rule | Detail |
|---|---|
| Plan before code | List files and reasons before making any change |
| One command at a time | Never chain commands — run one, confirm, then proceed |
| Tests must pass | No commit until `pytest -v` is green |
| Evidence in every PR | Include test count and coverage % |
| Rollback in every PR | Always include `git revert <SHA>` as the rollback |
| No vendor/submodule edits | Scope changes to `samples/` and `ai-track-docs/` |

---

## Related files

- [CONTRIBUTING.md](../CONTRIBUTING.md) — full contribution guide including Walk workflow
- [ai-track-docs/coverage.md](coverage.md) — coverage output and PR snippet template
- [ai-track-docs/build-test.md](build-test.md) — exact build and test commands
