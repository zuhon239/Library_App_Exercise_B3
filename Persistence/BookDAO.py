"""
Layer 3 - Persistence Layer
BookDAO: Data Access Object for the Books table.
Handles all CRUD operations for books.
"""

from Database.DBConnection import get_connection


class BookDAO:

    def add_book(self, title: str, author: str, quantity: int) -> int:
        """Insert a new book and return its generated BookId."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Books (Title, Author, Quantity) VALUES (?, ?, ?)",
            (title, author, quantity)
        )
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return book_id

    def get_all_books(self) -> list:
        """Return all books as a list of Row objects."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books ORDER BY BookId")
        books = cursor.fetchall()
        conn.close()
        return books

    def get_book_by_id(self, book_id: int):
        """Return a single book by its BookId, or None if not found."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE BookId = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book

    def update_quantity(self, book_id: int, quantity: int) -> bool:
        """Update the available quantity of a book. Returns True on success."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Books SET Quantity = ? WHERE BookId = ?",
            (quantity, book_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    def delete_book(self, book_id: int) -> bool:
        """Delete a book by its BookId. Returns True on success."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE BookId = ?", (book_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def search_books(self, keyword: str) -> list:
        """Search books by title or author (case-insensitive partial match)."""
        conn = get_connection()
        cursor = conn.cursor()
        like = f"%{keyword}%"
        cursor.execute(
            "SELECT * FROM Books WHERE Title LIKE ? OR Author LIKE ?",
            (like, like)
        )
        books = cursor.fetchall()
        conn.close()
        return books
