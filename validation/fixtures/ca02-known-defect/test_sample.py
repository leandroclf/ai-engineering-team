import unittest

from sample import is_authorized


class AuthorizationTest(unittest.TestCase):
    def test_admin_is_authorized(self):
        self.assertIs(is_authorized("admin"), True)

    def test_other_roles_are_denied(self):
        for role in ("user", "guest", "viewer", "editor", "superadmin", "unknown", ""):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_admin_requires_exact_match(self):
        for role in ("Admin", "ADMIN", " admin", "admin ", "admin\n"):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_calls_do_not_share_authorization_state(self):
        for role in ("guest", "admin", "user", "admin", ""):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), role == "admin")


if __name__ == "__main__":
    unittest.main()
