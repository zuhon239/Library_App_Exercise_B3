"""
Layer 1 - Presentation Layer
MemberView: Console UI for member management.
"""

from Business.MemberService import MemberService


class MemberView:

    def __init__(self):
        self._service = MemberService()

    def show_menu(self):
        while True:
            print("\n===== MEMBER MANAGEMENT =====")
            print("1. List all members")
            print("2. Register new member")
            print("3. Delete a member")
            print("0. Back")
            choice = input("Choose: ").strip()

            if   choice == "1": self._list_members()
            elif choice == "2": self._register_member()
            elif choice == "3": self._delete_member()
            elif choice == "0": break
            else: print("[!] Invalid option.")

    def _list_members(self):
        members = self._service.get_all_members()
        if not members:
            print("  No members registered.")
            return
        print(f"\n{'ID':<5} {'Full Name':<30} {'Email'}")
        print("-" * 65)
        for m in members:
            print(f"{m['MemberId']:<5} {m['FullName']:<30} {m['Email']}")

    def _register_member(self):
        name  = input("  Full name : ").strip()
        email = input("  Email     : ").strip()
        result = self._service.register_member(name, email)
        if result["success"]:
            print(f"[OK] Member registered with ID = {result['member_id']}")
        else:
            print(f"[ERROR] {result['error']}")

    def _delete_member(self):
        try:
            member_id = int(input("  Member ID to delete: "))
        except ValueError:
            print("[!] Invalid ID.")
            return
        confirm = input(f"  Delete member {member_id}? (y/n): ").strip().lower()
        if confirm != "y":
            print("  Cancelled.")
            return
        result = self._service.delete_member(member_id)
        print("[OK] Deleted." if result["success"] else f"[ERROR] {result['error']}")
