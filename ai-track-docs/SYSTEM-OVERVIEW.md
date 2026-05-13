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

## Subsystem Index

See [`ai-track-docs/subsystem-book-app.md`](subsystem-book-app.md) for the full file map of `samples/book-app-project/` — real paths, risk notes, and links to all related docs.

## Architecture

See [`ai-track-docs/architecture.mmd`](architecture.mmd) for the full component diagram (Mermaid).

**Key data flows:**
1. **User → CLI → Core → Persistence:** `book_app.py` calls `BookCollection` methods which read/write `data.json`
2. **Test execution:** `test_books.py` imports `BookCollection` directly; `monkeypatch` redirects `DATA_FILE` to `tmp_path` so the real `data.json` is never touched
3. **Benchmark:** `bench_find.py` calls `find_book` in a `timeit` loop against a seeded in-memory collection

## Chosen Low-Risk Module

**`samples/book-app-project/books.py`**

## Module Justification

- Already has a full pytest suite covering add, list, find, mark-as-read, and remove operations
- File I/O is fully isolated by test fixtures — no risk of corrupting real data
- Self-contained with no external service dependencies
- All upcoming Crawl exercises (refactor, validation, logging, feature flags, resilience) can be applied here with a clear test safety net
- Changes are small and reversible
