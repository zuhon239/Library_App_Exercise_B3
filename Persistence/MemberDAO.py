"""
Layer 3 - Persistence Layer
MemberDAO: Data Access Object for the Members table.
"""

from Database.DBConnection import get_connection


class MemberDAO:

    def add_member(self, full_name: str, email: str) -> int:
        """Insert a new member and return the generated MemberId."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Members (FullName, Email) VALUES (?, ?)",
            (full_name, email)
        )
        conn.commit()
        member_id = cursor.lastrowid
        conn.close()
        return member_id

    def get_all_members(self) -> list:
        """Return all members."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Members ORDER BY MemberId")
        members = cursor.fetchall()
        conn.close()
        return members

    def get_member_by_id(self, member_id: int):
        """Return a single member by MemberId, or None."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Members WHERE MemberId = ?", (member_id,))
        member = cursor.fetchone()
        conn.close()
        return member

    def get_member_by_email(self, email: str):
        """Return a member by email, or None."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Members WHERE Email = ?", (email,))
        member = cursor.fetchone()
        conn.close()
        return member

    def delete_member(self, member_id: int) -> bool:
        """Delete a member. Returns True on success."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE MemberId = ?", (member_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
