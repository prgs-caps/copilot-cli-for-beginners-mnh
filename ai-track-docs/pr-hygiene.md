# PR Hygiene Guide

## PR Description Sections (Required)

| Section | Purpose |
|---------|---------|
| **Summary** | What changed and why; files touched |
| **Review Focus** | Where reviewers should spend their time |
| **Evidence** | Test output, benchmark numbers, or log snippets |
| **Risk & Rollback** | Risk level + exact rollback command |

A `.github/pull_request_template.md` is committed to enforce these sections on every PR.

## Commit Message Conventions

Use the format: `<scope>: <short imperative description>`

| Scope | When to use |
|-------|------------|
| `crawl:` | Crawl track exercise commits |
| `fix:` | Bug fixes |
| `feat:` | New features |
| `docs:` | Documentation only |
| `test:` | Test additions or fixes |
| `refactor:` | Behavior-preserving code changes |
| `chore:` | Dependency/config/tooling updates |

**Examples:**
```
crawl: ex11 pr-hygiene
fix: handle blank title in add_book
docs: add extending-books guide
```

## Review Focus Tips

- Call out any validation logic changes — these affect all callers
- Flag any changes to persistence (save_books/load_books) — data integrity risk
- Note if a change is additive-only (safe) vs. mutating existing behavior (needs closer review)

## Rollback Guidance

Always include the commit SHA in the PR description. To roll back:
```powershell
git revert <commit SHA>
git push
```
For feature flags: document the toggle name and OFF state.
