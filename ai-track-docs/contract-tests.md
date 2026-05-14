# Contract Tests

## Boundary: `BookCollection.add_book()` return shape

**File:** `samples/book-app-project/books.py`  
**Test file:** `samples/book-app-project/tests/test_books.py` (Walk Ex5 section)

### Contract

`add_book(title, author, year)` must always return a `Book` dataclass with exactly these fields:

| Field | Type | Default |
|---|---|---|
| `title` | `str` | (from input) |
| `author` | `str` | (from input) |
| `year` | `int` | (from input) |
| `read` | `bool` | `False` |

`list_books()` must return a list of `Book` objects that serialize (via `dataclasses.asdict`) to dicts with the same four keys.

### Tests

- `test_add_book_return_shape` — validates field names and types
- `test_add_book_return_values_match_inputs` — validates values echo inputs
- `test_list_books_serialization_shape` — validates serialization shape

### Running contract tests

```powershell
cd samples/book-app-project
pytest -v -k "contract"
```

Or run all tests (contract tests are included):

```powershell
pytest -v
```

### How to update this contract

If the `Book` dataclass gains, loses, or renames a field:

1. Update `books.py` (the `Book` dataclass definition)
2. Update the `assert set(d.keys()) == {...}` assertions in `test_books.py`
3. Update the table in this file
4. Run `pytest -v` to confirm all tests pass
5. Include the schema change in the PR description under `## Plan`

### Rollback

```
git revert <SHA>
```

This reverts both the test additions and this doc in a single commit.

---

## Boundary: `save_books()` / `load_books()` persistence round-trip (Run Ex 5)

**File:** `samples/book-app-project/books.py`  
**Test file:** `samples/book-app-project/tests/test_books.py` (Run Ex 5 section)

### Contract

A `Book` written by `save_books()` and reloaded by `load_books()` (i.e. via a new `BookCollection()`) must preserve all four fields with the correct Python types:

| Field | JSON type | Python type after reload |
|---|---|---|
| `title` | string | `str` |
| `author` | string | `str` |
| `year` | number (integer) | `int` |
| `read` | boolean | `bool` |

The field set after reload must be exactly `{"title", "author", "year", "read"}` — no extras, no omissions.

### Tests

- `test_persistence_round_trip_contract` — saves a book, reloads in a fresh `BookCollection`, asserts field names and Python types are preserved exactly

### How to update this contract

If `Book` gains a new field or the JSON serialization changes (e.g. `year` stored as string):

1. Update `books.py` (the `Book` dataclass and `save_books` / `load_books` methods)
2. Update `test_persistence_round_trip_contract` in `test_books.py` — add/remove key assertions and type checks
3. Update the table above
4. Run `pytest -v` to confirm all 41+ tests pass
5. Include the schema change in the PR under `## Plan`

### Rollback

```
git revert <SHA>
```

---

## Boundary: `find_book_by_title()` return shape (Run Ex 5)

**File:** `samples/book-app-project/books.py`  
**Test file:** `samples/book-app-project/tests/test_books.py` (Run Ex 5 section)

### Contract

`find_book_by_title(title)` must return:

| Condition | Return value |
|---|---|
| Book not found | Exactly `None` (not `[]`, not `False`, not `0`) |
| Book found | A `Book` dataclass with fields `{"title", "author", "year", "read"}` and correct Python types |

### Tests

- `test_find_book_returns_none_for_missing_contract` — asserts `result is None` (identity check, not truthiness)
- `test_find_book_return_shape_contract` — asserts found book has correct field set and types

### How to update this contract

If `find_book_by_title` changes its return type or `Book` gains/loses fields:

1. Update `books.py`
2. Update `test_find_book_returns_none_for_missing_contract` and `test_find_book_return_shape_contract`
3. Update the tables above
4. Run `pytest -v`
5. Include the change in the PR under `## Plan`

### Rollback

```
git revert <SHA>
```
