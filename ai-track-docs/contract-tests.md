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
