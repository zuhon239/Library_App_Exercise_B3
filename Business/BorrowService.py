"""
Layer 2 - Business Layer
BorrowService: Business logic for borrowing and returning books.

Business rules enforced here:
  - A member must exist before borrowing.
  - A book must exist and have available copies (Quantity > 0).
  - ReturnDate must be >= BorrowDate.
  - Cannot return an already-returned record.
"""

from datetime import date, datetime
from Persistence.BorrowDAO import BorrowDAO
from Business.BookService import BookService
from Business.MemberService import MemberService


class BorrowService:

    def __init__(self):
        self._dao            = BorrowDAO()
        self._book_service   = BookService()
        self._member_service = MemberService()

    # ------------------------------------------------------------------ #
    #  Borrow a book                                                       #
    # ------------------------------------------------------------------ #
    def borrow_book(self, book_id: int, member_id: int, borrow_date: str = None) -> dict:
        """
        Process a borrow request.
        borrow_date defaults to today if not provided (YYYY-MM-DD).
        Returns {"success": True, "record_id": int} or {"success": False, "error": str}.
        """
        # Validate member
        member = self._member_service.get_member_by_id(member_id)
        if not member:
            return {"success": False, "error": f"Member ID {member_id} does not exist."}

        # Validate book
        book = self._book_service.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": f"Book ID {book_id} does not exist."}
        if book["Quantity"] <= 0:
            return {"success": False, "error": f"'{book['Title']}' has no available copies."}

        # Determine borrow date
        if borrow_date is None:
            borrow_date = str(date.today())
        else:
            if not self._valid_date(borrow_date):
                return {"success": False, "error": "Invalid borrow date. Use YYYY-MM-DD."}

        # Decrease available quantity (business rule)
        result = self._book_service.decrease_quantity(book_id)
        if not result["success"]:
            return result

        # Persist the borrow record
        record_id = self._dao.add_record(book_id, member_id, borrow_date)
        return {"success": True, "record_id": record_id}

    # ------------------------------------------------------------------ #
    #  Return a book                                                       #
    # ------------------------------------------------------------------ #
    def return_book(self, record_id: int, return_date: str = None) -> dict:
        """
        Process a book return.
        return_date defaults to today if not provided.
        """
        record = self._dao.get_record_by_id(record_id)
        if not record:
            return {"success": False, "error": f"Borrow record ID {record_id} not found."}
        if record["ReturnDate"] is not None:
            return {"success": False, "error": "This book has already been returned."}

        if return_date is None:
            return_date = str(date.today())
        else:
            if not self._valid_date(return_date):
                return {"success": False, "error": "Invalid return date. Use YYYY-MM-DD."}

        # Business rule: ReturnDate must not be before BorrowDate
        if return_date < record["BorrowDate"]:
            return {
                "success": False,
                "error": f"Return date ({return_date}) cannot be before borrow date ({record['BorrowDate']})."
            }

        # Increase available quantity
        self._book_service.increase_quantity(record["BookId"])

        # Persist the return date
        self._dao.set_return_date(record_id, return_date)
        return {"success": True}

    # ------------------------------------------------------------------ #
    #  Query helpers                                                       #
    # ------------------------------------------------------------------ #
    def get_all_records(self) -> list:
        return self._dao.get_all_records()

    def get_active_borrows_by_member(self, member_id: int) -> list:
        return self._dao.get_active_borrows_by_member(member_id)

    def get_overdue_records(self, loan_days: int = 14) -> list:
        """
        Return all unreturned records whose BorrowDate is older than `loan_days` days.
        Default loan period is 14 days.
        """
        all_active = self._dao.get_all_records()
        today = date.today()
        overdue = []
        for r in all_active:
            if r["ReturnDate"] is None:
                borrow = datetime.strptime(r["BorrowDate"], "%Y-%m-%d").date()
                days_out = (today - borrow).days
                if days_out > loan_days:
                    overdue.append((r, days_out))
        return overdue

    # ------------------------------------------------------------------ #
    #  Private utilities                                                   #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _valid_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
