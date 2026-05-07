# Extending BookCollection

`BookCollection` lives in `samples/book-app-project/books.py`.
It stores a list of `Book` dataclass instances and persists them to a JSON file.

---

## Add a new field to Book

1. Add the field to the `@dataclass`:
   ```python
   genre: str = ""