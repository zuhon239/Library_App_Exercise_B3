"""
LibraryApp — Main Entry Point
Layered Architecture Demo (Python + SQLite)

Run:  python main.py
"""

import sys
import os

# Make sure all packages resolve from the project root
sys.path.insert(0, os.path.dirname(__file__))

from Database.DBConnection import initialize_database
from Presentation.BookView   import BookView
from Presentation.MemberView import MemberView
from Presentation.BorrowView import BorrowView


def main():
    # Layer 4 — initialise DB on first run
    initialize_database()

    book_view   = BookView()
    member_view = MemberView()
    borrow_view = BorrowView()

    while True:
        print("\n========================================")
        print("    LIBRARY MANAGEMENT SYSTEM")
        print("    Layered Architecture Demo")
        print("========================================")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow / Return")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if   choice == "1": book_view.show_menu()
        elif choice == "2": member_view.show_menu()
        elif choice == "3": borrow_view.show_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    main()
