import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False

def test_list_books_returns_empty_for_new_collection():
    """Deterministic baseline: a fresh collection always starts with zero books."""
    collection = BookCollection()
    assert collection.list_books() == []

def test_add_book_blank_title_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="title"):
        collection.add_book("", "Some Author", 2000)

def test_add_book_blank_author_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="author"):
        collection.add_book("Some Title", "  ", 2000)

def test_add_book_invalid_year_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="year"):
        collection.add_book("Some Title", "Some Author", -1)

def test_find_book_case_insensitive_by_default(monkeypatch):
    """Default (BOOKS_CASE_SENSITIVE unset): title matching is case-insensitive."""
    monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.find_book_by_title("dune") is not None

def test_find_book_case_sensitive_when_flag_on(monkeypatch):
    """ON (BOOKS_CASE_SENSITIVE=1): wrong case returns None, exact case succeeds."""
    monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.find_book_by_title("dune") is None
    assert collection.find_book_by_title("Dune") is not None
