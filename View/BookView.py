"""
Layer 1 - Presentation Layer
BookView: Console UI for book management.
Only communicates with BookService — never touches DAO directly.
"""

from Business.BookService import BookService


class BookView:

    def __init__(self):
        self._service = BookService()

    def show_menu(self):
        while True:
            print("\n===== BOOK MANAGEMENT =====")
            print("1. List all books")
            print("2. Search books")
            print("3. Add a book")
            print("4. Update book quantity")
            print("5. Delete a book")
            print("0. Back")
            choice = input("Choose: ").strip()

            if   choice == "1": self._list_books()
            elif choice == "2": self._search_books()
            elif choice == "3": self._add_book()
            elif choice == "4": self._update_quantity()
            elif choice == "5": self._delete_book()
            elif choice == "0": break
            else: print("[!] Invalid option.")

    # --- Handlers ---

    def _list_books(self):
        books = self._service.get_all_books()
        if not books:
            print("  No books found.")
            return
        print(f"\n{'ID':<5} {'Title':<35} {'Author':<25} {'Qty'}")
        print("-" * 70)
        for b in books:
            print(f"{b['BookId']:<5} {b['Title']:<35} {b['Author']:<25} {b['Quantity']}")

    def _search_books(self):
        kw = input("  Enter keyword: ").strip()
        books = self._service.search_books(kw)
        if not books:
            print("  No matching books.")
            return
        print(f"\n{'ID':<5} {'Title':<35} {'Author':<25} {'Qty'}")
        print("-" * 70)
        for b in books:
            print(f"{b['BookId']:<5} {b['Title']:<35} {b['Author']:<25} {b['Quantity']}")

    def _add_book(self):
        title    = input("  Title  : ").strip()
        author   = input("  Author : ").strip()
        qty_str  = input("  Qty    : ").strip()
        try:
            qty = int(qty_str)
        except ValueError:
            print("[!] Quantity must be an integer.")
            return
        result = self._service.add_book(title, author, qty)
        if result["success"]:
            print(f"[OK] Book added with ID = {result['book_id']}")
        else:
            print(f"[ERROR] {result['error']}")

    def _update_quantity(self):
        try:
            book_id = int(input("  Book ID : "))
            qty     = int(input("  New Qty : "))
        except ValueError:
            print("[!] Please enter valid integers.")
            return
        result = self._service.update_quantity(book_id, qty)
        print(f"[OK] Updated." if result["success"] else f"[ERROR] {result['error']}")

    def _delete_book(self):
        try:
            book_id = int(input("  Book ID to delete: "))
        except ValueError:
            print("[!] Invalid ID.")
            return
        confirm = input(f"  Delete book {book_id}? (y/n): ").strip().lower()
        if confirm != "y":
            print("  Cancelled.")
            return
        result = self._service.delete_book(book_id)
        print("[OK] Deleted." if result["success"] else f"[ERROR] {result['error']}")
