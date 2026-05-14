import logging
import sys
import time

from books import BookCollection

logger = logging.getLogger(__name__)

# Global collection instance
collection = BookCollection()


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    t0 = time.monotonic()
    books = collection.list_books()
    elapsed_ms = (time.monotonic() - t0) * 1000
    logger.debug(
        "cmd_list",
        extra={
            "op": "handle_list",
            "status": "ok",
            "count": len(books),
            "elapsed_ms": round(elapsed_ms, 3),
        },
    )
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        t0 = time.monotonic()
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        elapsed_ms = (time.monotonic() - t0) * 1000
        logger.info(
            "cmd_add",
            extra={
                "op": "handle_add",
                "status": "ok",
                "title": title,
                "elapsed_ms": round(elapsed_ms, 3),
            },
        )
        print("\nBook added successfully.\n")
    except ValueError as e:
        logger.warning(
            "cmd_add_failed",
            extra={"op": "handle_add", "status": "error", "error": str(e)},
        )
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    removed = collection.remove_book(title)
    logger.info(
        "cmd_remove",
        extra={"op": "handle_remove", "status": "ok" if removed else "not_found", "title": title},
    )
    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "help":
        show_help()
    else:
        logger.warning(
            "cmd_unknown",
            extra={"op": "main", "status": "unknown_command", "command": command},
        )
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
