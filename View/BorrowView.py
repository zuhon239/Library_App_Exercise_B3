"""
Layer 1 - Presentation Layer
BorrowView: Console UI for borrow/return operations.
"""

from Business.BorrowService import BorrowService


class BorrowView:

    def __init__(self):
        self._service = BorrowService()

    def show_menu(self):
        while True:
            print("\n===== BORROW / RETURN =====")
            print("1. Borrow a book")
            print("2. Return a book")
            print("3. View all borrow records")
            print("4. View active borrows by member")
            print("5. View overdue records")
            print("0. Back")
            choice = input("Choose: ").strip()

            if   choice == "1": self._borrow_book()
            elif choice == "2": self._return_book()
            elif choice == "3": self._all_records()
            elif choice == "4": self._active_by_member()
            elif choice == "5": self._overdue()
            elif choice == "0": break
            else: print("[!] Invalid option.")

    def _borrow_book(self):
        try:
            book_id   = int(input("  Book ID   : "))
            member_id = int(input("  Member ID : "))
        except ValueError:
            print("[!] Invalid input."); return
        date_str = input("  Borrow date (YYYY-MM-DD, blank = today): ").strip() or None
        result = self._service.borrow_book(book_id, member_id, date_str)
        if result["success"]:
            print(f"[OK] Borrow record created. Record ID = {result['record_id']}")
        else:
            print(f"[ERROR] {result['error']}")

    def _return_book(self):
        try:
            record_id = int(input("  Record ID : "))
        except ValueError:
            print("[!] Invalid input."); return
        date_str = input("  Return date (YYYY-MM-DD, blank = today): ").strip() or None
        result = self._service.return_book(record_id, date_str)
        print("[OK] Book returned successfully." if result["success"] else f"[ERROR] {result['error']}")

    def _all_records(self):
        records = self._service.get_all_records()
        if not records:
            print("  No records found."); return
        print(f"\n{'RID':<5} {'Book Title':<30} {'Member':<20} {'Borrowed':<12} {'Returned'}")
        print("-" * 85)
        for r in records:
            returned = r["ReturnDate"] if r["ReturnDate"] else "NOT RETURNED"
            print(f"{r['RecordId']:<5} {r['Title']:<30} {r['FullName']:<20} {r['BorrowDate']:<12} {returned}")

    def _active_by_member(self):
        try:
            member_id = int(input("  Member ID: "))
        except ValueError:
            print("[!] Invalid input."); return
        records = self._service.get_active_borrows_by_member(member_id)
        if not records:
            print("  No active borrows for this member."); return
        print(f"\n{'RID':<5} {'Book Title':<35} {'Borrowed'}")
        print("-" * 55)
        for r in records:
            print(f"{r['RecordId']:<5} {r['Title']:<35} {r['BorrowDate']}")

    def _overdue(self):
        overdue = self._service.get_overdue_records(loan_days=14)
        if not overdue:
            print("  No overdue records."); return
        print(f"\n{'RID':<5} {'Book':<30} {'Member':<20} {'Days Overdue'}")
        print("-" * 70)
        for r, days in overdue:
            print(f"{r['RecordId']:<5} {r['Title']:<30} {r['FullName']:<20} {days} days")
