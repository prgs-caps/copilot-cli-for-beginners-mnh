"""Micro-benchmark for BookCollection.find_book_by_title.

Run from the samples/book-app-project directory:
    python bench_find.py

Uses a temporary file so it never touches data.json.
"""
import os
import tempfile
import timeit

import books
from books import BookCollection

REPEATS = 5
NUMBER = 10_000


def setup(tmp_path):
    books.DATA_FILE = tmp_path
    col = BookCollection()
    for i in range(100):
        col.add_book(f"Book {i}", "Author", 2000 + (i % 30))
    return col


def main():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name
    try:
        col = setup(tmp)
        times = timeit.repeat(
            lambda: col.find_book_by_title("Book 99"),
            number=NUMBER,
            repeat=REPEATS,
        )
        ms = [t / NUMBER * 1000 for t in times]
        print(f"find_book_by_title (100-book collection, n={NUMBER})")
        print(f"  min   : {min(ms):.4f} ms")
        print(f"  max   : {max(ms):.4f} ms")
        print(f"  mean  : {sum(ms)/len(ms):.4f} ms")
        print(f"  runs  : {ms}")
    finally:
        os.unlink(tmp)


if __name__ == "__main__":
    main()
