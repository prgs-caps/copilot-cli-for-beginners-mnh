# Performance Baseline — BookCollection

**Date:** 2026-05-07  
**Machine:** Windows, Python 3.13.9  
**Module:** `samples/book-app-project/books.py`  
**Function:** `BookCollection.find_book_by_title`

## How to run

```powershell
cd samples/book-app-project
python bench_find.py
```

## Setup

- Collection size: 100 books
- Search target: last book ("Book 99") — worst-case linear scan
- Iterations per run: 10,000
- Repeat runs: 5

## Results (baseline)

| Metric | Value |
|--------|-------|
| min    | 0.0084 ms |
| max    | 0.0087 ms |
| mean   | 0.0085 ms |

Raw runs: `[0.0086, 0.0084, 0.0087, 0.0087, 0.0084]`

## Variance notes

- Variance is negligible (<4%) — consistent linear scan over a small list.
- No optimization needed at this scale.
- Re-run this benchmark after any change to `find_book_by_title` or `_titles_match` to detect regressions.

---

## Walk Ex 6 — Micro-optimization: `remove_book` single-pass refactor

**Date:** 2026-05-11  
**Machine:** Windows, Python 3.13.9  
**Function:** `BookCollection.remove_book`

### Change

**Before:** `find_book_by_title()` (scan 1, O(n)) + `list.remove(book)` (scan 2, O(n)) = 2n comparisons worst case  
**After:** `enumerate` + `pop(i)` (single scan, O(n)) = n comparisons worst case

### Benchmark (worst case: target is last element, N=1000 books, 500 reps)

| Approach | ms/op |
|---|---|
| OLD (2 scans) | 0.7975 ms |
| NEW (1 scan)  | 0.7650 ms |
| Improvement   | ~4.1% |

### Notes

- Improvement is modest at N=1000 but grows linearly with collection size.
- No behavior change — all existing tests pass (20/20).
- Rollback: `git revert <SHA>` restores the two-scan approach.

---

## Run Ex 6 — Micro-optimizations: `_save_with_retry` + `list_books` defensive copy

**Date:** 2026-05-13  
**Machine:** Windows, Python 3.13.9  
**Function:** `BookCollection._save_with_retry` / `BookCollection.list_books`

### Changes

**Win 1 — Precompute serialization once before the retry loop:**
`data = [asdict(b) for b in self.books]` is now computed once before the retry
loop. Previously each failed attempt recomputed the full list comprehension.

**Win 2 — Compact JSON (remove `indent=2`):**
`json.dump(data, f)` replaces `json.dump(..., f, indent=2)`. Compact JSON is
faster to serialize and produces smaller files; `json.load` is unaffected.

**Win 3 — `list_books()` defensive copy:**
Returns `list(self.books)` instead of the raw `self.books` reference. Callers
can no longer corrupt the collection by mutating the returned list.

### Benchmark (`save_books`, 100 books, n=1000 per run, 5 runs)

```
python -c "import timeit, books, tempfile, os, importlib ..."
```

| Metric | Before | After |
|--------|--------|-------|
| min    | 1.2973 ms | 1.0945 ms |
| max    | 1.3325 ms | 1.1848 ms |
| mean   | 1.3078 ms | 1.1304 ms |
| improvement | — | **~13.5%** |

Before runs: `[1.3325, 1.2976, 1.2973, 1.3090, 1.3024]`  
After runs:  `[1.1848, 1.0945, 1.1195, 1.0976, 1.1556]`

### Notes

- `find_book_by_title` behaviour and timing unchanged — no regression.
- All 41 tests pass.
- Rollback: `git revert <SHA>` restores pretty-print indent and raw list return.

