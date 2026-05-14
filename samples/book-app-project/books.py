import json
import logging
import os
import time
from dataclasses import asdict, dataclass

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
        self.books: list[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file, retrying on transient OSError."""
        try:
            self._load_with_retry()
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            logger.warning(
                "load_books_corrupt",
                extra={"op": "load_books", "status": "corrupt", "file": DATA_FILE},
            )
            self.books = []

    def _load_with_retry(
        self,
        max_attempts: int | None = None,
        initial_delay: float | None = None,
        backoff: float = 2.0,
    ) -> None:
        """Read DATA_FILE and populate self.books, retrying on transient OSError.

        Args:
            max_attempts:  Total read attempts (default from BOOK_APP_MAX_RETRIES, else 3).
            initial_delay: Seconds before first retry
                (default from BOOK_APP_RETRY_DELAY, else 0.05).
            backoff:       Delay multiplier after each failure (2.0 = exponential).

        Raises:
            FileNotFoundError: If the file does not exist (propagated without retry).
            OSError:           If all retry attempts are exhausted.
            json.JSONDecodeError: If the file is present but malformed (propagated).
        """
        if max_attempts is None:
            max_attempts = int(os.environ.get("BOOK_APP_MAX_RETRIES", "3"))
        if initial_delay is None:
            initial_delay = float(os.environ.get("BOOK_APP_RETRY_DELAY", "0.05"))
        delay = initial_delay
        for attempt in range(1, max_attempts + 1):
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                self.books = [Book(**b) for b in data]
                return
            except FileNotFoundError:
                raise  # not transient — propagate immediately
            except json.JSONDecodeError:
                raise  # not transient — propagate immediately
            except OSError:
                if attempt == max_attempts:
                    raise
                logger.warning(
                    "load_retry",
                    extra={
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                        "delay_s": round(delay, 4),
                    },
                )
                time.sleep(delay)
                delay *= backoff

    def save_books(self) -> None:
        """Save the current book collection to JSON (with retry on transient OSError).

        Retry parameters are tunable via environment variables:
          BOOK_APP_MAX_RETRIES   — integer, total attempts (default 3)
          BOOK_APP_RETRY_DELAY   — float, initial delay in seconds (default 0.05)
        """
        max_attempts = int(os.environ.get("BOOK_APP_MAX_RETRIES", "3"))
        initial_delay = float(os.environ.get("BOOK_APP_RETRY_DELAY", "0.05"))
        self._save_with_retry(max_attempts=max_attempts, initial_delay=initial_delay)

    def _save_with_retry(
        self,
        max_attempts: int = 3,
        initial_delay: float = 0.05,
        backoff: float = 2.0,
    ) -> None:
        """Write the book list to DATA_FILE, retrying on transient OSError.

        Args:
            max_attempts:  Total number of write attempts before re-raising.
            initial_delay: Seconds before the first retry.
            backoff:       Multiplier applied to the delay after each failed
                           attempt (default 2.0 = exponential; 1.0 = linear).

        Raises:
            OSError: If all attempts are exhausted.
        """
        delay = initial_delay
        data = [asdict(b) for b in self.books]
        for attempt in range(1, max_attempts + 1):
            try:
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f)
                return
            except OSError:
                if attempt == max_attempts:
                    raise
                logger.warning(
                    "save_retry",
                    extra={
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                        "delay_s": round(delay, 4),
                    },
                )
                time.sleep(delay)
                delay *= backoff

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
        if (
            os.environ.get("BOOK_APP_STRICT_DUPLICATES") == "1"
            and self.find_book_by_title(title) is not None
        ):
            raise ValueError(f"duplicate title: {title!r}")
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

    def list_books(self) -> list[Book]:
        """Return all books in insertion order."""
        return list(self.books)

    def find_book_by_title(self, title: str) -> Book | None:
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

    def find_by_author(self, author: str) -> list[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
