import json
import logging
import time
from dataclasses import asdict, dataclass
from typing import List, Optional

from utils import titles_match

DATA_FILE = "data.json"

logger = logging.getLogger(__name__)


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
        self._validate_book_fields(title, author, year)
        t0 = time.monotonic()
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        elapsed_ms = (time.monotonic() - t0) * 1000
        logger.debug(
            "book_added",
            extra={
                "op": "add_book",
                "status": "ok",
                "title": title,
                "elapsed_ms": round(elapsed_ms, 3),
            },
        )
        return book

    def _validate_book_fields(self, title: str, author: str, year: int) -> None:
        """Raise ValueError if any book field is invalid."""
        if not title or not title.strip():
            raise ValueError("title must not be blank")
        if not author or not author.strip():
            raise ValueError("author must not be blank")
        if not isinstance(year, int) or year <= 0:
            raise ValueError("year must be a positive integer")

    def list_books(self) -> List[Book]:
        """Return all books in insertion order."""
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Return the first Book whose title matches, or None."""
        for book in self.books:
            if titles_match(book.title, title):
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
        """Remove a book by title.

        Uses a single-pass enumerate + pop(i) to avoid the double linear scan
        that find_book_by_title + list.remove would otherwise perform.
        """
        t0 = time.monotonic()
        for i, book in enumerate(self.books):
            if titles_match(book.title, title):
                self.books.pop(i)
                self.save_books()
                elapsed_ms = (time.monotonic() - t0) * 1000
                logger.debug(
                    "book_removed",
                    extra={
                        "op": "remove_book",
                        "status": "ok",
                        "title": title,
                        "elapsed_ms": round(elapsed_ms, 3),
                    },
                )
                return True
        elapsed_ms = (time.monotonic() - t0) * 1000
        logger.debug(
            "book_remove_miss",
            extra={
                "op": "remove_book",
                "status": "not_found",
                "title": title,
                "elapsed_ms": round(elapsed_ms, 3),
            },
        )
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
