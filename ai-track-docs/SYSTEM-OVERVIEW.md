# System Overview

> **Status:** Updated Ex 1 (Repo Orientation).

## Repo Purpose

A structured GitHub Copilot learning course (`copilot-cli-for-beginners`) containing tutorial chapters, sample applications, and tooling scripts. Audience: developers learning to use GitHub Copilot with the CLI and in VS Code.

## Languages & Runtimes

| Language | Version | Where used |
|---|---|---|
| Python | 3.10+ | `samples/book-app-project/` — primary sample app |
| JavaScript / Node.js | LTS | `samples/src/`, `package.json` scripts |
| C# | .NET | `samples/book-app-project-cs/` — alternate sample |

## Entry Points

| Entry Point | Purpose |
|---|---|
| `samples/book-app-project/book_app.py` | Interactive CLI book collection app |
| `samples/src/index.js` | JavaScript sample entry point |
| `package.json` scripts | Demo/header generation tooling (Node) |

## Test Approach

- Framework: **pytest**
- Test file: `samples/book-app-project/tests/test_books.py`
- Run from `samples/book-app-project/`: `pytest`
- Tests are hermetic — `tmp_path` + `monkeypatch` fixtures isolate all file I/O so no real `data.json` is touched during tests

## Chosen Low-Risk Module

**`samples/book-app-project/books.py`**

## Module Justification

- Already has a full pytest suite covering add, list, find, mark-as-read, and remove operations
- File I/O is fully isolated by test fixtures — no risk of corrupting real data
- Self-contained with no external service dependencies
- All upcoming Crawl exercises (refactor, validation, logging, feature flags, resilience) can be applied here with a clear test safety net
- Changes are small and reversible
