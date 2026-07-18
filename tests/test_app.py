import unittest

from app import Handler, valid_messages


class AppTests(unittest.TestCase):
    def test_handler_endpoints_exist(self):
        self.assertTrue(hasattr(Handler, "do_POST"))
        self.assertTrue(hasattr(Handler, "do_GET"))

    def test_message_validation(self):
        self.assertTrue(valid_messages([{"role": "user", "content": "Olá"}]))
        self.assertFalse(valid_messages([]))
        self.assertFalse(valid_messages([{"role": "admin", "content": "x"}]))


if __name__ == "__main__":
    unittest.main()
