import unittest

from sample import is_authorized


class AuthorizationTest(unittest.TestCase):
    def test_admin_is_authorized(self):
        self.assertIs(is_authorized("admin"), True)

    def test_other_roles_are_denied(self):
        for role in ("user", "guest", "viewer", "editor", "superadmin", ""):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_admin_must_match_exactly(self):
        for role in ("Admin", "ADMIN", " admin", "admin ", "admin\n"):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_invalid_inputs_are_denied(self):
        for role in (None, 0, True, [], {}, b"admin"):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), False)

    def test_calls_do_not_share_authorization_state(self):
        for role, expected in (("user", False), ("admin", True), ("guest", False), ("admin", True)):
            with self.subTest(role=role):
                self.assertIs(is_authorized(role), expected)


if __name__ == "__main__":
    unittest.main()
