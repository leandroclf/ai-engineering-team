import unittest

from sample import is_authorized


class AuthorizationTest(unittest.TestCase):
    def test_admin_is_authorized(self):
        self.assertIs(is_authorized("admin"), True)

    def test_other_roles_are_denied(self):
        for role in ("user", "guest", "editor", "superadmin", "", "ADMIN",
                     "Admin", " admin", "admin ", "admin\n"):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_authorization_does_not_carry_between_calls(self):
        for role, expected in (("user", False), ("admin", True),
                               ("guest", False), ("admin", True)):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), expected)


if __name__ == "__main__":
    unittest.main()
