"""
Walk Ex 13 — Feature Flag: BOOKS_CASE_SENSITIVE
================================================
Explicit ON/OFF validation for the BOOKS_CASE_SENSITIVE env-var flag.

Flag contract:
  OFF (unset / not "1")  → titles_match and BookCollection ops are case-insensitive
  ON  (BOOKS_CASE_SENSITIVE=1) → titles_match and BookCollection ops are case-sensitive

All tests use monkeypatch to isolate the env var so they are order-independent
and safe to run in any environment.
"""

import pytest

from books import BookCollection
from utils import titles_match


# ---------------------------------------------------------------------------
# titles_match — unit-level
# ---------------------------------------------------------------------------


class TestTitlesMatchFlagOff:
    """Flag OFF (default): matching ignores case."""

    def test_same_case(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        assert titles_match("Dune", "Dune") is True

    def test_lower_vs_upper(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        assert titles_match("Dune", "dune") is True

    def test_upper_vs_mixed(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        assert titles_match("DUNE", "Dune") is True

    def test_different_titles_still_false(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        assert titles_match("Dune", "Foundation") is False

    def test_flag_value_zero_treated_as_off(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "0")
        assert titles_match("Dune", "dune") is True

    def test_flag_empty_string_treated_as_off(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "")
        assert titles_match("Dune", "dune") is True


class TestTitlesMatchFlagOn:
    """Flag ON (BOOKS_CASE_SENSITIVE=1): matching is strict."""

    def test_exact_case_matches(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        assert titles_match("Dune", "Dune") is True

    def test_wrong_case_does_not_match(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        assert titles_match("Dune", "dune") is False

    def test_all_upper_does_not_match_mixed(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        assert titles_match("DUNE", "Dune") is False

    def test_different_titles_false(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        assert titles_match("Dune", "Foundation") is False


# ---------------------------------------------------------------------------
# BookCollection.find_book_by_title — integration-level
# ---------------------------------------------------------------------------


class TestFindByTitleFlagOff:
    """Flag OFF: find_book_by_title is case-insensitive."""

    def test_finds_with_lowercase_query(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)
        assert col.find_book_by_title("dune") is not None

    def test_finds_with_uppercase_query(self, monkeypatch):
        monkeypatch.delenv("BOOKS_CASE_SENSITIVE", raising=False)
        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)
        assert col.find_book_by_title("DUNE") is not None


class TestFindByTitleFlagOn:
    """Flag ON: find_book_by_title requires exact case."""

    def test_wrong_case_returns_none(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)
        assert col.find_book_by_title("dune") is None

    def test_exact_case_returns_book(self, monkeypatch):
        monkeypatch.setenv("BOOKS_CASE_SENSITIVE", "1")
        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)
        assert col.find_book_by_title("Dune") is not None
