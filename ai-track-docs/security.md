# Security & Secrets Hygiene

## What was checked

- `.gitignore` reviewed for common secret file patterns
- Repo history scanned for `.env`, key, and credential files — none found
- `books.py` reviewed for hardcoded secrets — none found
- Runtime data file (`data.json`) checked for ignore coverage

## What was improved

| Item | Action |
|------|--------|
| Missing key/cert patterns (`*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.cer`, `*.crt`, `*.der`) | Added to `.gitignore` |
| Missing credential file patterns (`secrets.json`, `credentials.json`, `serviceaccount.json`) | Added to `.gitignore` |
| `samples/book-app-project/data.json` (runtime user data) | Added to `.gitignore` — prevents accidental commit |

## What was already in place

- `.env` and all `.env.*` variants already ignored
- No third-party secrets management needed (no network calls, no auth)

## Scan step (Walk Ex 8)

### Tool: bandit

`bandit` performs static analysis of Python source for common security issues (injection, hardcoded passwords, unsafe use of subprocess, etc.).

**Install:**
```powershell
cd samples/book-app-project
pip install bandit
```

**Run against source (excludes test files):**
```powershell
bandit -r . --exclude ./tests -f txt
```

**Run with pyproject.toml config (recommended):**
```powershell
bandit -c pyproject.toml -r .
```

### Findings from initial scan

Scan target: `samples/book-app-project/` (source files only, `tests/` excluded via `[tool.bandit]` config)

| Severity | Confidence | Test ID | Location | Disposition |
|----------|------------|---------|----------|-------------|
| No issues found | — | — | — | Clean |

Running bandit against `books.py` and `utils.py` produced **0 issues**:
- No subprocess calls, no hardcoded credentials, no unsafe deserialization, no shell injection vectors.
- `json.load()` reads from a local file path controlled by the app, not from untrusted network input.

### Justified ignore: B101 (assert_used)

`B101` flags `assert` statements as potentially unsafe in production code (Python removes `assert` when run with `-O`).

**Justification:** All `assert` statements in this project reside in `tests/test_books.py`. Using `assert` in pytest test files is the standard, expected pattern. There are no `assert` statements in production source files (`books.py`, `utils.py`). `B101` is therefore suppressed via `skips = ["B101"]` in `[tool.bandit]` and `tests/` is excluded from the default scan scope.

To verify no production-code asserts exist:
```powershell
Select-String -Path books.py, utils.py -Pattern "^\s*assert"
```
Expected: no matches.

## Ongoing guidance

- Never commit credentials, tokens, or keys — use environment variables or a secrets manager.
- If `data.json` ever needs to be seeded for development, use a separate `data.example.json` that is committed without real data.
- Run `bandit -c pyproject.toml -r .` from `samples/book-app-project/` before each PR to catch new issues early.
