"""
Run Ex 15 — Resilience Sweep: failure tests for _load_with_retry and _save_with_retry
========================================================================================
Covers two call paths:
  1. Read path  — BookCollection._load_with_retry() called from load_books()
  2. Write path — BookCollection._save_with_retry() called from save_books()
     (now with tunable BOOK_APP_MAX_RETRIES / BOOK_APP_RETRY_DELAY env vars)

All tests use monkeypatch + unittest.mock to inject failures without hitting disk
or sleeping, keeping the suite fast and deterministic.
"""

from unittest.mock import MagicMock, patch

import pytest

from books import BookCollection

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def collection(tmp_path, monkeypatch):
    """Fresh BookCollection backed by a temp directory (no pre-existing data file)."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("BOOK_APP_MAX_RETRIES", raising=False)
    monkeypatch.delenv("BOOK_APP_RETRY_DELAY", raising=False)
    return BookCollection()


# ---------------------------------------------------------------------------
# Call path 1: _load_with_retry
# ---------------------------------------------------------------------------

class TestLoadWithRetry:
    """Failure behaviour of the read-path resilience helper."""

    def test_transient_oserror_retried_then_succeeds(self, tmp_path, monkeypatch):
        """A single transient OSError on read is retried and succeeds on attempt 2."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("BOOK_APP_MAX_RETRIES", raising=False)
        monkeypatch.delenv("BOOK_APP_RETRY_DELAY", raising=False)

        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)

        # Re-instantiate with a patched open: fail once with OSError, then succeed
        real_open = open
        call_count = 0

        def open_side_effect(name, *args, **kwargs):
            nonlocal call_count
            if "data.json" in str(name) and not kwargs.get("mode", "").startswith("w"):
                call_count += 1
                if call_count == 1:
                    raise OSError("transient read error")
            return real_open(name, *args, **kwargs)

        with patch("books.open", side_effect=open_side_effect), \
             patch("books.time.sleep"):  # don't actually sleep
            col2 = BookCollection()

        assert len(col2.list_books()) == 1
        assert col2.list_books()[0].title == "Dune"

    def test_persistent_oserror_raises_after_max_attempts(self, tmp_path, monkeypatch):
        """OSError on every attempt exhausts retries and re-raises."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("BOOK_APP_MAX_RETRIES", "2")
        monkeypatch.setenv("BOOK_APP_RETRY_DELAY", "0")

        # Write a valid data file so the file exists
        (tmp_path / "data.json").write_text("[]")

        with (
            patch("books.open", side_effect=OSError("permanent error")),
            patch("books.time.sleep"),
            pytest.raises(OSError, match="permanent error"),
        ):
            col = BookCollection()
            col._load_with_retry(max_attempts=2, initial_delay=0)

    def test_file_not_found_is_not_retried(self, tmp_path, monkeypatch):
        """FileNotFoundError is propagated immediately without retrying."""
        monkeypatch.chdir(tmp_path)
        # No data.json — collection should initialise empty, not retry
        attempt_count = 0

        real_load = BookCollection._load_with_retry

        def counting_load(self, *args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            return real_load(self, *args, **kwargs)

        with patch.object(BookCollection, "_load_with_retry", counting_load):
            col = BookCollection()

        assert col.list_books() == []
        assert attempt_count == 1  # called exactly once, not retried

    def test_env_var_controls_max_retries_on_load(self, tmp_path, monkeypatch):
        """BOOK_APP_MAX_RETRIES is respected by _load_with_retry."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("BOOK_APP_MAX_RETRIES", "1")
        monkeypatch.setenv("BOOK_APP_RETRY_DELAY", "0")

        (tmp_path / "data.json").write_text("[]")

        attempts = []

        real_open = open

        def counting_open(name, *args, **kwargs):
            if "data.json" in str(name):
                attempts.append(1)
                raise OSError("forced")
            return real_open(name, *args, **kwargs)

        with (
            patch("books.open", side_effect=counting_open),
            patch("books.time.sleep"),
            pytest.raises(OSError),
        ):
            BookCollection()

        assert len(attempts) == 1  # only 1 attempt when max_retries=1


# ---------------------------------------------------------------------------
# Call path 2: _save_with_retry (write path) — env-var tuning
# ---------------------------------------------------------------------------

class TestSaveWithRetryTuning:
    """Env-var tuning of the write-path resilience helper."""

    def test_env_max_retries_controls_write_attempts(self, collection, monkeypatch):
        """BOOK_APP_MAX_RETRIES limits write attempts on persistent OSError."""
        monkeypatch.setenv("BOOK_APP_MAX_RETRIES", "2")
        monkeypatch.setenv("BOOK_APP_RETRY_DELAY", "0")
        collection.add_book("Dune", "Frank Herbert", 1965)

        attempts = []

        real_open = open

        def counting_open(name, mode="r", *args, **kwargs):
            if "data.json" in str(name) and mode == "w":
                attempts.append(1)
                raise OSError("disk full")
            return real_open(name, mode, *args, **kwargs)

        with (
            patch("books.open", side_effect=counting_open),
            patch("books.time.sleep"),
            pytest.raises(OSError, match="disk full"),
        ):
            collection.save_books()

        assert len(attempts) == 2  # max_retries=2 → exactly 2 write attempts

    def test_transient_write_error_retried_then_succeeds(self, collection, monkeypatch):
        """A single transient OSError on write is retried and succeeds."""
        monkeypatch.setenv("BOOK_APP_MAX_RETRIES", "3")
        monkeypatch.setenv("BOOK_APP_RETRY_DELAY", "0")
        collection.add_book("Foundation", "Isaac Asimov", 1951)

        call_count = 0
        real_open = open

        def open_side_effect(name, mode="r", *args, **kwargs):
            nonlocal call_count
            if "data.json" in str(name) and mode == "w":
                call_count += 1
                if call_count == 1:
                    raise OSError("transient write error")
            return real_open(name, mode, *args, **kwargs)

        with patch("books.open", side_effect=open_side_effect), \
             patch("books.time.sleep"):
            collection.save_books()  # should not raise

        assert call_count == 2  # failed once, succeeded on retry

    def test_default_retry_params_used_when_env_unset(self, collection, monkeypatch):
        """When env vars are absent, defaults (3 attempts, 0.05 s delay) apply."""
        monkeypatch.delenv("BOOK_APP_MAX_RETRIES", raising=False)
        monkeypatch.delenv("BOOK_APP_RETRY_DELAY", raising=False)

        mock_retry = MagicMock(wraps=collection._save_with_retry)
        collection._save_with_retry = mock_retry
        collection.save_books()

        # Defaults should be passed through
        mock_retry.assert_called_once_with(max_attempts=3, initial_delay=0.05)
