"""
Run Ex 13 — Progressive Hardening Flag: BOOK_APP_STRICT_DUPLICATES
====================================================================
Validates ON/OFF behaviour of the strict-duplicate-detection safety switch.

Flag contract:
  OFF (unset / any value other than "1") — default:
      add_book allows duplicate titles (current permissive behaviour).
  ON  (BOOK_APP_STRICT_DUPLICATES=1):
      add_book raises ValueError if a book with the same title already exists
      (case-insensitive, consistent with find_book_by_title).

All tests monkeypatch the env var so they are order-independent and safe
to run in any environment without touching disk (tmp_path fixture used for
the JSON data file to avoid side-effects).
"""

import os

import pytest

from books import BookCollection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def collection(tmp_path, monkeypatch):
    """Return a fresh BookCollection backed by a temp data file."""
    monkeypatch.chdir(tmp_path)
    return BookCollection()


# ---------------------------------------------------------------------------
# Flag OFF (default) — permissive duplicates
# ---------------------------------------------------------------------------

class TestStrictDuplicatesFlagOff:
    """Flag OFF: adding a duplicate title is allowed."""

    def test_duplicate_allowed_when_flag_unset(self, collection, monkeypatch):
        monkeypatch.delenv("BOOK_APP_STRICT_DUPLICATES", raising=False)
        collection.add_book("Dune", "Frank Herbert", 1965)
        # Should not raise
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert len(collection.list_books()) == 2

    def test_duplicate_allowed_when_flag_zero(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "0")
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        assert len(collection.list_books()) == 2

    def test_duplicate_allowed_when_flag_empty(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "")
        collection.add_book("Neuromancer", "William Gibson", 1984)
        collection.add_book("Neuromancer", "William Gibson", 1984)
        assert len(collection.list_books()) == 2


# ---------------------------------------------------------------------------
# Flag ON — strict duplicate rejection
# ---------------------------------------------------------------------------

class TestStrictDuplicatesFlagOn:
    """Flag ON: adding a duplicate title raises ValueError."""

    def test_exact_duplicate_raises(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "1")
        collection.add_book("Dune", "Frank Herbert", 1965)
        with pytest.raises(ValueError, match="duplicate title"):
            collection.add_book("Dune", "Frank Herbert", 1965)

    def test_case_insensitive_duplicate_raises(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "1")
        collection.add_book("Dune", "Frank Herbert", 1965)
        with pytest.raises(ValueError, match="duplicate title"):
            collection.add_book("dune", "Frank Herbert", 1965)

    def test_unique_title_still_succeeds(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "1")
        collection.add_book("Dune", "Frank Herbert", 1965)
        # Different title — must not raise
        collection.add_book("Foundation", "Isaac Asimov", 1951)
        assert len(collection.list_books()) == 2

    def test_collection_unchanged_after_duplicate_rejection(self, collection, monkeypatch):
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "1")
        collection.add_book("Dune", "Frank Herbert", 1965)
        with pytest.raises(ValueError):
            collection.add_book("Dune", "Frank Herbert", 1965)
        # Collection should still have exactly one book
        assert len(collection.list_books()) == 1

    def test_flag_value_must_be_exactly_one(self, collection, monkeypatch):
        """Only the string '1' enables strict mode; 'true', 'yes', '2' do not."""
        monkeypatch.setenv("BOOK_APP_STRICT_DUPLICATES", "true")
        collection.add_book("Dune", "Frank Herbert", 1965)
        # Should NOT raise — 'true' != '1'
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert len(collection.list_books()) == 2
