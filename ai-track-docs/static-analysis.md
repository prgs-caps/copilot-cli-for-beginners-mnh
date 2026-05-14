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
