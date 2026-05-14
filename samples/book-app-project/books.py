import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    """A single book record.

    Attributes:
        title:  Book title (display-case preserved).
        author: Author full name.
        year:   Publication year.
        read:   True once mark_as_read() has been called.
    """
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manages an in-memory list of Book objects backed by a JSON file.

    The collection is loaded from DATA_FILE on construction and
    automatically saved after every mutating operation.
    """
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Create a new Book, append it to the collection, and persist.

        Args:
            title:  Book title.
            author: Author full name.
            year:   Publication year.

        Returns:
            The newly created Book instance.

        Raises:
            ValueError: If title or author is blank, or year is not a positive integer.
        """
        if not title or not title.strip():
            raise ValueError("title must not be blank")
        if not author or not author.strip():
            raise ValueError("author must not be blank")
        if not isinstance(year, int) or year <= 0:
            raise ValueError("year must be a positive integer")
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in insertion order."""
        return self.books

    def _titles_match(self, a: str, b: str) -> bool:
        """Case-insensitive equality check for two title strings."""
        return a.lower() == b.lower()

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Return the first Book whose title matches (case-insensitive), or None."""
        for book in self.books:
            if self._titles_match(book.title, title):
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark the matching book as read and persist.

        Returns:
            True if a book was found and updated, False otherwise.
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
