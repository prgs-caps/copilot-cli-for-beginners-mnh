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
