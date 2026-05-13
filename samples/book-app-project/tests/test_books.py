import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import books
from books import BookCollection
from utils import titles_match


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


# --- Resilience / failure tests (Ex15) ---


def test_corrupted_data_file_starts_empty(tmp_path, monkeypatch):
    """Corrupted JSON is handled gracefully — collection starts empty, no crash."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json!!}")
    monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
    collection = BookCollection()
    assert collection.list_books() == []


def test_missing_data_file_starts_empty(tmp_path, monkeypatch):
    """Missing data file is handled gracefully — collection starts empty."""
    missing = tmp_path / "nonexistent.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing))
    collection = BookCollection()
    assert collection.list_books() == []


def test_remove_already_removed_book_returns_false():
    """remove_book on an already-removed book returns False without corrupting state."""
    collection = BookCollection()
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    collection.remove_book("Foundation")
    result = collection.remove_book("Foundation")
    assert result is False
    assert len(collection.list_books()) == 0


def test_mark_as_read_idempotent():
    """Calling mark_as_read twice on the same book is safe and returns True both times."""
    collection = BookCollection()
    collection.add_book("Neuromancer", "William Gibson", 1984)
    assert collection.mark_as_read("Neuromancer") is True
    assert collection.mark_as_read("Neuromancer") is True
    book = collection.find_book_by_title("Neuromancer")
    assert book.read is True


# --- utils.titles_match unit tests (Walk Ex3) ---


def test_titles_match_case_insensitive(monkeypatch):
    """titles_match is case-insensitive when BOOKS_CASE_SENSITIVE is unset."""
    monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
    assert titles_match("Dune", "dune") is True
    assert titles_match("DUNE", "Dune") is True


def test_titles_match_case_sensitive_flag(monkeypatch):
    """titles_match is strict when BOOKS_CASE_SENSITIVE=1."""
    monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
    assert titles_match("Dune", "dune") is False
    assert titles_match("Dune", "Dune") is True


# --- Contract tests (Walk Ex5) ---
# Boundary: add_book() and list_books() return shape.
# These tests lock the public API surface so any field rename or type change
# is caught immediately. Update the assertions here when the schema changes.

def test_add_book_return_shape():
    """Contract: add_book always returns a Book with the expected fields and types."""
    from dataclasses import asdict
    collection = BookCollection()
    book = collection.add_book("Brave New World", "Aldous Huxley", 1932)
    d = asdict(book)
    assert set(d.keys()) == {"title", "author", "year", "read"}, (
        "Book schema changed — update contract tests and ai-track-docs/contract-tests.md"
    )
    assert isinstance(d["title"], str)
    assert isinstance(d["author"], str)
    assert isinstance(d["year"], int)
    assert isinstance(d["read"], bool)
    assert d["read"] is False  # new books are always unread


def test_add_book_return_values_match_inputs():
    """Contract: add_book echoes inputs exactly in the returned Book."""
    collection = BookCollection()
    book = collection.add_book("Fahrenheit 451", "Ray Bradbury", 1953)
    assert book.title == "Fahrenheit 451"
    assert book.author == "Ray Bradbury"
    assert book.year == 1953


# --- Walk Ex 15 — retry/backoff resilience tests ---


def test_save_with_retry_succeeds_after_transient_oserror(tmp_path, monkeypatch):
    """_save_with_retry retries and succeeds when the first write raises OSError."""
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    collection = BookCollection()

    real_open = open
    write_calls = [0]

    def patched_open(*args, **kwargs):
        mode = args[1] if len(args) > 1 else kwargs.get("mode", "r")
        if mode == "w":
            write_calls[0] += 1
            if write_calls[0] == 1:
                raise OSError("simulated transient disk error")
        return real_open(*args, **kwargs)

    monkeypatch.setattr("builtins.open", patched_open)
    collection._save_with_retry(max_attempts=2, initial_delay=0)

    assert write_calls[0] == 2  # failed once, then succeeded


def test_save_with_retry_raises_after_max_attempts(tmp_path, monkeypatch):
    """_save_with_retry raises OSError after exhausting all retry attempts."""
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    collection = BookCollection()

    real_open = open

    def always_fail_on_write(*args, **kwargs):
        mode = args[1] if len(args) > 1 else kwargs.get("mode", "r")
        if mode == "w":
            raise OSError("permanent write failure")
        return real_open(*args, **kwargs)

    monkeypatch.setattr("builtins.open", always_fail_on_write)
    with pytest.raises(OSError, match="permanent write failure"):
        collection._save_with_retry(max_attempts=2, initial_delay=0)


def test_list_books_serialization_shape():
    """Contract: list_books entries serialize to dicts with the expected keys."""
    from dataclasses import asdict
    collection = BookCollection()
    collection.add_book("The Road", "Cormac McCarthy", 2006)
    books_list = collection.list_books()
    assert len(books_list) == 1
    d = asdict(books_list[0])
    assert set(d.keys()) == {"title", "author", "year", "read"}, (
        "Serialization schema changed — update contract tests and ai-track-docs/contract-tests.md"
    )


# --- Run Ex 3 — backoff param + structured-log refactor tests ---


def test_save_with_retry_backoff_param_controls_delay(tmp_path, monkeypatch):
    """_save_with_retry uses the backoff multiplier, not a hardcoded 2.0.

    With backoff=1.0 (linear), each sleep call should use the same initial_delay.
    """
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    collection = BookCollection()

    real_open = open
    call_count = [0]
    sleep_args: list[float] = []

    def failing_open(*args, **kwargs):
        mode = args[1] if len(args) > 1 else kwargs.get("mode", "r")
        if mode == "w":
            call_count[0] += 1
            if call_count[0] < 3:
                raise OSError("transient")
        return real_open(*args, **kwargs)

    monkeypatch.setattr("builtins.open", failing_open)
    monkeypatch.setattr("time.sleep", lambda s: sleep_args.append(s))

    collection._save_with_retry(max_attempts=3, initial_delay=0.1, backoff=1.0)

    # With backoff=1.0, every sleep should be exactly initial_delay (0.1)
    assert sleep_args == [0.1, 0.1], f"Expected linear delays [0.1, 0.1], got {sleep_args}"


def test_load_books_corrupt_uses_logger_not_print(tmp_path, monkeypatch, caplog):
    """Corrupted data file triggers logger.warning (not print) — Run Ex 3 refactor."""
    import logging
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json!!}")
    monkeypatch.setattr(books, "DATA_FILE", str(bad_file))

    with caplog.at_level(logging.WARNING, logger="books"):
        collection = BookCollection()

    assert collection.list_books() == []
    assert any("load_books_corrupt" in r.message for r in caplog.records), (
        "Expected a 'load_books_corrupt' warning log entry"
    )


# --- Run Ex 5 — Contract Sweep ---
# Two additional boundaries: persistence round-trip and find_book_by_title return shape.
# If the Book schema or JSON format changes, update these tests AND
# ai-track-docs/contract-tests.md (the "How to update" section there lists the steps).


def test_persistence_round_trip_contract(tmp_path, monkeypatch):
    """Contract: save_books + load_books preserves all Book fields with correct types.

    This locks the data.json serialization format. If save/load changes how a field
    is stored (e.g. 'year' becomes a string), this test catches it immediately.
    Update the assertions here and the table in ai-track-docs/contract-tests.md.
    """
    from dataclasses import asdict

    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    c1 = BookCollection()
    c1.add_book("Solaris", "Stanislaw Lem", 1961)
    c1.mark_as_read("Solaris")
    c1.save_books()

    c2 = BookCollection()
    loaded = c2.list_books()
    assert len(loaded) == 1, "Round-trip must preserve book count"

    d = asdict(loaded[0])
    assert set(d.keys()) == {"title", "author", "year", "read"}, (
        "Persistence schema changed — update contract tests and ai-track-docs/contract-tests.md"
    )
    assert d["title"] == "Solaris"
    assert d["author"] == "Stanislaw Lem"
    assert isinstance(d["year"], int) and d["year"] == 1961, (
        "'year' must survive round-trip as int — check JSON serialization"
    )
    assert isinstance(d["read"], bool) and d["read"] is True, (
        "'read' must survive round-trip as bool — check JSON serialization"
    )


def test_find_book_returns_none_for_missing_contract():
    """Contract: find_book_by_title returns exactly None (not falsy) when absent."""
    collection = BookCollection()
    result = collection.find_book_by_title("No Such Book")
    assert result is None, (
        "find_book_by_title must return None (not [] or False) when book is absent"
    )


def test_find_book_return_shape_contract():
    """Contract: find_book_by_title returns a Book with the expected fields when found.

    If Book gains, loses, or renames a field, this test and the table in
    ai-track-docs/contract-tests.md must be updated together.
    """
    from dataclasses import asdict

    collection = BookCollection()
    collection.add_book("Hyperion", "Dan Simmons", 1989)
    result = collection.find_book_by_title("Hyperion")
    assert result is not None, "find_book_by_title must return a Book when the title exists"

    d = asdict(result)
    assert set(d.keys()) == {"title", "author", "year", "read"}, (
        "Book schema changed — update contract tests and ai-track-docs/contract-tests.md"
    )
    assert isinstance(d["title"], str)
    assert isinstance(d["author"], str)
    assert isinstance(d["year"], int)
    assert isinstance(d["read"], bool)
