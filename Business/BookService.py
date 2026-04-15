"""
Layer 2 - Business Layer
BookService: Business logic for book management.
Validates inputs, enforces rules, and delegates to BookDAO.
"""

from Persistence.BookDAO import BookDAO


class BookService:

    def __init__(self):
        self._dao = BookDAO()

    # ------------------------------------------------------------------ #
    #  Add a book                                                          #
    # ------------------------------------------------------------------ #
    def add_book(self, title: str, author: str, quantity: int) -> dict:
        """
        Validate and add a new book.
        Returns {"success": True, "book_id": int} or {"success": False, "error": str}.
        """
        title   = title.strip()
        author  = author.strip()

        if not title:
            return {"success": False, "error": "Title cannot be empty."}
        if not author:
            return {"success": False, "error": "Author cannot be empty."}
        if quantity < 0:
            return {"success": False, "error": "Quantity cannot be negative."}

        book_id = self._dao.add_book(title, author, quantity)
        return {"success": True, "book_id": book_id}

    # ------------------------------------------------------------------ #
    #  List / Search                                                       #
    # ------------------------------------------------------------------ #
    def get_all_books(self) -> list:
        return self._dao.get_all_books()

    def search_books(self, keyword: str) -> list:
        if not keyword.strip():
            return self._dao.get_all_books()
        return self._dao.search_books(keyword.strip())

    def get_book_by_id(self, book_id: int):
        return self._dao.get_book_by_id(book_id)

    # ------------------------------------------------------------------ #
    #  Update quantity                                                     #
    # ------------------------------------------------------------------ #
    def update_quantity(self, book_id: int, quantity: int) -> dict:
        if quantity < 0:
            return {"success": False, "error": "Quantity cannot be negative."}
        book = self._dao.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": f"Book ID {book_id} not found."}
        self._dao.update_quantity(book_id, quantity)
        return {"success": True}

    # ------------------------------------------------------------------ #
    #  Delete                                                              #
    # ------------------------------------------------------------------ #
    def delete_book(self, book_id: int) -> dict:
        book = self._dao.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": f"Book ID {book_id} not found."}
        self._dao.delete_book(book_id)
        return {"success": True}

    # ------------------------------------------------------------------ #
    #  Internal helpers (used by BorrowService)                           #
    # ------------------------------------------------------------------ #
    def decrease_quantity(self, book_id: int) -> dict:
        """Decrease quantity by 1 (called when a book is borrowed)."""
        book = self._dao.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": "Book not found."}
        if book["Quantity"] <= 0:
            return {"success": False, "error": "No copies available to borrow."}
        self._dao.update_quantity(book_id, book["Quantity"] - 1)
        return {"success": True}

    def increase_quantity(self, book_id: int) -> dict:
        """Increase quantity by 1 (called when a book is returned)."""
        book = self._dao.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": "Book not found."}
        self._dao.update_quantity(book_id, book["Quantity"] + 1)
        return {"success": True}
