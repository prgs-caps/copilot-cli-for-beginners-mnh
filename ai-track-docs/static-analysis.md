# Static Analysis

## Tool: ruff

[ruff](https://docs.astral.sh/ruff/) is an extremely fast Python linter written in Rust.
It is zero-config friendly, covers the most important pycodestyle / pyflakes / isort rules,
and replaces flake8 + isort in a single binary.

## Configuration

Configured in `samples/book-app-project/pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["ruff>=0.4,<1"]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
```

| Rule set | Covers |
|----------|--------|
| `E` | pycodestyle errors |
| `F` | pyflakes (unused imports, undefined names) |
| `W` | pycodestyle warnings |
| `I` | isort (import ordering) |

## How to run

```powershell
# Install ruff (one-time)
pip install "ruff>=0.4,<1"

# Check for violations (from repo root or samples/book-app-project/)
ruff check samples/book-app-project

# Auto-fix safe violations
ruff check --fix samples/book-app-project

# Check a single file
ruff check samples/book-app-project/books.py
```

## Baseline

As of Ex14, `ruff check samples/book-app-project` reports **0 violations**.

---

## Walk Ex 14 — Strict Gate on utils.py

### Scope

Strictness is increased for one path only: `samples/book-app-project/utils.py`.
All other files remain subject to the baseline ruleset (`E, F, W, I`).

### Additional rules applied to utils.py

| Rule group | What it catches |
|---|---|
| `ANN2xx` (ANN201, ANN202) | Missing return-type annotations on public/private functions |
| `ANN001` | Missing type annotation on function arguments |

Run locally (strict, utils.py only):
```powershell
cd samples/book-app-project
ruff check utils.py --select E,F,W,I,ANN2
```

### CI Gate

Step name: **"Ruff strict gate — utils.py"** in `.github/workflows/book-app-ci.yml`.
This step has **no `continue-on-error`** — it fails the pipeline on any violation.

### Findings Resolved

| Location | Rule | Fix applied |
|---|---|---|
| `utils.py:print_menu` | ANN201 | Added `-> None` return annotation |
| `utils.py:get_book_details` | ANN201 | Added `-> tuple[str, str, int]` return annotation |
| `utils.py:print_books` | ANN201 | Added `-> None` return annotation |
| `utils.py:print_books(books)` | ANN001 | Added `books: list` parameter annotation |

### Suppressions

None. All findings were resolved by adding the missing annotations.

If a future finding warrants suppression, add an inline comment with justification:
```python
some_func()  # noqa: ANN201 — return type is None, omitted intentionally
```
Document the justification in this file before merging.

### Rollback

1. Remove the **"Ruff strict gate — utils.py"** step from `book-app-ci.yml`
2. Optionally revert annotations in `utils.py` (no behavior change — annotations are runtime-transparent)
3. `git revert <commit-sha>`
