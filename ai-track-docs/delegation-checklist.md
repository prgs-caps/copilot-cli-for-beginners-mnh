# Run Delegation Checklist

Reusable checklist for every Run exercise. Complete each phase in order.
Copy this file or reference it in your PR description for each Run exercise.

---

## Phase 1 — Patch Plan

Before touching any file, write the plan.

- [ ] State the goal in one sentence
- [ ] List every file to change (path + reason)
- [ ] Identify the subsystem/folder scope (do not exceed it)
- [ ] Note any files explicitly out of scope (submodules, vendor folders, generated files)
- [ ] Identify the rollback strategy (revert commit SHA or toggle flag)

**Template:**

```
Goal: <one sentence>

Files to change:
- <path/to/file.py>  -- reason
- <path/to/test_file.py>  -- reason
- <path/to/doc.md>  -- reason

Out of scope: submodules/, vendor/, generated/

Rollback: git revert <commit-sha>
```

---

## Phase 2 — Diffs

Produce diffs file-by-file before applying them.

- [ ] Show diff for each changed file individually
- [ ] Confirm no unintended files are touched
- [ ] Confirm no secrets, credentials, or tokens in diffs
- [ ] Confirm diff stays within the declared subsystem scope

---

## Phase 3 — Tests

- [ ] Identify which existing tests cover the changed paths
- [ ] Add or update tests if behavior changed
- [ ] Run the full test suite: `cd samples/book-app-project && python -m pytest -v`
- [ ] Confirm 0 failures before proceeding
- [ ] Note the test count before and after (evidence artifact)

---

## Phase 4 — Docs

- [ ] Update any doc that references changed behavior or file paths
- [ ] Confirm all file path references in docs are real and correct
- [ ] Add risk notes where relevant (e.g. "this step has no continue-on-error")
- [ ] Docs updated in the same PR as the code change

---

## Phase 5 — Evidence

Capture at least one concrete evidence artifact for the PR.

| Artifact | Command | Where to include |
|----------|---------|-----------------|
| Test output | `python -m pytest -v` | PR body -- Evidence section |
| Coverage | `python -m pytest --cov` | PR body -- Evidence section |
| Lint/gate | `ruff check <path>` | PR body -- Evidence section |
| Log sample | `python -m pytest -s -k <test>` | PR body or inline comment |

- [ ] At least one artifact captured and included in PR

---

## Phase 6 — PR

- [ ] Title: `GHCP -- Run: Ex<N> <short-name>`
- [ ] Summary: what changed and why, files touched
- [ ] Evidence: paste artifact output
- [ ] Review focus: 2-3 bullets on what reviewers should check
- [ ] Risk: low / medium + explanation
- [ ] Rollback: `git revert <sha>` or toggle instruction
- [ ] Track: Level: Run / Exercise: Ex<N>

---

## Rollback Reference

| Scenario | Rollback action |
|----------|----------------|
| Bad commit | `git revert <sha>` |
| Bad push | `git revert <sha>` then `git push` |
| Flag-guarded behavior | Set env var to disable flag |
| CI step added | Remove step from workflow YAML |
| Docs only | Revert the doc commit |

---

## Run Ex 1 Instance (this PR)

**Goal:** Create this reusable delegation checklist in ai-track-docs/.

**Files changed:**
- `ai-track-docs/delegation-checklist.md` -- new file (this checklist)

**Out of scope:** all code files, submodules, vendor folders

**Rollback:** `git revert <ex1-commit-sha>`

**Evidence:** No code changed -- checklist is a docs-only artifact. Test suite: 36 passed, 0 failed (unchanged).
