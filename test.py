import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p> Hello World </p>")

    def test_getpersons(self):
        response = self.app.get("/persons")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Victor Craft" in response.data.decode())

    def test_getpersons_by_id(self):
        response = self.app.get("/persons/15")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Elisia Chi" in response.data.decode())


if __name__ == "__main__":
    unittest.main()
