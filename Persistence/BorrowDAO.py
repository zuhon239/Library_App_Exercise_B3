"""
Layer 3 - Persistence Layer
BorrowDAO: Data Access Object for the BorrowRecords table.
"""

from Database.DBConnection import get_connection


class BorrowDAO:

    def add_record(self, book_id: int, member_id: int, borrow_date: str) -> int:
        """Insert a new borrow record. ReturnDate starts as NULL."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO BorrowRecords (BookId, MemberId, BorrowDate, ReturnDate)
               VALUES (?, ?, ?, NULL)""",
            (book_id, member_id, borrow_date)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    def set_return_date(self, record_id: int, return_date: str) -> bool:
        """Mark a borrow record as returned by setting its ReturnDate."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE BorrowRecords SET ReturnDate = ? WHERE RecordId = ?",
            (return_date, record_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    def get_active_borrows_by_member(self, member_id: int) -> list:
        """Return all unreturned borrow records for a given member."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT br.*, b.Title, m.FullName
               FROM BorrowRecords br
               JOIN Books b   ON br.BookId   = b.BookId
               JOIN Members m ON br.MemberId = m.MemberId
               WHERE br.MemberId = ? AND br.ReturnDate IS NULL""",
            (member_id,)
        )
        records = cursor.fetchall()
        conn.close()
        return records

    def get_active_borrows_by_book(self, book_id: int) -> list:
        """Return all unreturned borrow records for a specific book."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT br.*, b.Title, m.FullName
               FROM BorrowRecords br
               JOIN Books b   ON br.BookId   = b.BookId
               JOIN Members m ON br.MemberId = m.MemberId
               WHERE br.BookId = ? AND br.ReturnDate IS NULL""",
            (book_id,)
        )
        records = cursor.fetchall()
        conn.close()
        return records

    def get_all_records(self) -> list:
        """Return all borrow records with book title and member name."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT br.*, b.Title, m.FullName
               FROM BorrowRecords br
               JOIN Books b   ON br.BookId   = b.BookId
               JOIN Members m ON br.MemberId = m.MemberId
               ORDER BY br.RecordId"""
        )
        records = cursor.fetchall()
        conn.close()
        return records

    def get_record_by_id(self, record_id: int):
        """Return a single borrow record by RecordId, or None."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM BorrowRecords WHERE RecordId = ?", (record_id,)
        )
        record = cursor.fetchone()
        conn.close()
        return record
