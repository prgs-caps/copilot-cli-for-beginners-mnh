# PR Hygiene Guide (Walk Ex 11)

## PR Description Sections (Required)

| Section | Purpose |
|---------|---------|
| **Summary** | What changed and why; files touched |
| **Plan** | Steps taken before any code was changed |
| **Review Focus** | Where reviewers should spend their time |
| **Verification Steps** | Exact commands to confirm correctness |
| **Evidence** | Test output, benchmark numbers, or log snippets |
| **Risk & Rollback** | Risk level + exact rollback command |

A `.github/pull_request_template.md` is committed to enforce these sections on every PR.

---

## How to use Copilot to draft this

After making your changes, send Copilot Chat:

```
Draft a PR description for my latest commit using the pr-hygiene template in
ai-track-docs/pr-hygiene.md. Include: summary, review focus bullets, verification
steps, evidence (test output), and rollback command.
```

Copilot will read the changed files and produce ready-to-paste PR text. Edit the
evidence section to include actual test output before submitting.

---

## Filled-in PR Template (copy and adapt)

```
## Summary
- <one sentence: what changed and why>
- Files: <list of changed files>

## Plan
1. <first step taken>
2. <second step taken>

## Review Focus
- [ ] <file or function>: <what to check and why it matters>
- [ ] <file or function>: <what to check and why it matters>
- [ ] Tests: confirm new/changed tests cover the affected paths

## Verification Steps
1. cd samples/book-app-project
2. pytest -v          # all tests pass
3. <any additional command specific to this change>

## Evidence
- pytest -v: <N> passed, 0 failed
- Coverage: <total %>

## Risk & Rollback
- Risk: low / medium / high — <one sentence reason>
- Rollback: git revert <commit SHA> && git push
```

---

## Review Focus Bullets — book-app patterns

Use these pre-written bullets when the relevant path is touched:

| Changed area | Review focus bullet |
|---|---|
| `add_book` / `remove_book` validation | Confirm ValueError is raised for blank/whitespace title; check negative tests cover this path |
| `save_books` / `load_books` | Data integrity: verify round-trip (write then read) produces identical list; check file path is not user-controlled |
| Structured logging (`logger.debug`) | Fields consistent with schema: op, status, title, elapsed_ms; no PII in log values |
| `pyproject.toml` dependency change | Confirm version constraint is a range not a pin; verify `pytest -v` still green after change |
| `.github/workflows/*.yml` | Check `continue-on-error` is intentional; confirm no secrets in env vars; verify trigger scope |
| Feature flag / env var | Confirm default is safe (OFF for new behavior); both ON and OFF paths have tests |

---

## Verification Steps — standard sequence

```powershell
# From samples/book-app-project/
pytest -v                                    # all tests green
pytest -v --cov=. --cov-report=term-missing  # check coverage %
ruff check .                                 # no lint errors
bandit -r . -c pyproject.toml               # no new security findings
```

---

## Commit Message Conventions

Use the format: `<scope>: <short imperative description>`

| Scope | When to use |
|-------|------------|
| `walk:` | Walk track exercise commits |
| `crawl:` | Crawl track exercise commits |
| `fix:` | Bug fixes |
| `feat:` | New features |
| `docs:` | Documentation only |
| `test:` | Test additions or fixes |
| `refactor:` | Behavior-preserving code changes |
| `chore:` | Dependency/config/tooling updates |

**Examples:**
```
walk: ex11 add PR review focus template to pr-hygiene.md
fix: handle blank title in add_book
docs: add extending-books guide
```

---

## Rollback Guidance

Always include the commit SHA in the PR description. To roll back:
```powershell
git revert <commit SHA>
git push
```
For feature flags: document the toggle name and OFF state.
