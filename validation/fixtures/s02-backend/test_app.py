import json
import unittest

import app


class ItemApiTest(unittest.TestCase):
    def setUp(self):
        app.ITEMS.clear()

    def test_create_and_get(self):
        status, item = app.handle("POST", "/items", json.dumps({"name": "pen"}))
        self.assertEqual(status, 201)
        self.assertEqual(app.handle("GET", f"/items/{item['id']}"), (200, item))

    def test_create_requires_name(self):
        self.assertEqual(app.handle("POST", "/items", "{}")[0], 400)


if __name__ == "__main__":
    unittest.main()
