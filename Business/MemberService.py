"""
Layer 2 - Business Layer
MemberService: Business logic for library member management.
"""

import re
from Persistence.MemberDAO import MemberDAO


_EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


class MemberService:

    def __init__(self):
        self._dao = MemberDAO()

    # ------------------------------------------------------------------ #
    #  Register a member                                                   #
    # ------------------------------------------------------------------ #
    def register_member(self, full_name: str, email: str) -> dict:
        """
        Validate and register a new member.
        Returns {"success": True, "member_id": int} or {"success": False, "error": str}.
        """
        full_name = full_name.strip()
        email     = email.strip().lower()

        if not full_name:
            return {"success": False, "error": "Full name cannot be empty."}
        if not _EMAIL_REGEX.match(email):
            return {"success": False, "error": "Invalid email address format."}

        existing = self._dao.get_member_by_email(email)
        if existing:
            return {"success": False, "error": f"Email '{email}' is already registered."}

        member_id = self._dao.add_member(full_name, email)
        return {"success": True, "member_id": member_id}

    # ------------------------------------------------------------------ #
    #  Query                                                               #
    # ------------------------------------------------------------------ #
    def get_all_members(self) -> list:
        return self._dao.get_all_members()

    def get_member_by_id(self, member_id: int):
        return self._dao.get_member_by_id(member_id)

    # ------------------------------------------------------------------ #
    #  Delete                                                              #
    # ------------------------------------------------------------------ #
    def delete_member(self, member_id: int) -> dict:
        member = self._dao.get_member_by_id(member_id)
        if not member:
            return {"success": False, "error": f"Member ID {member_id} not found."}
        self._dao.delete_member(member_id)
        return {"success": True}
