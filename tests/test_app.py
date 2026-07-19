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
        self.assertFalse(valid_messages([{"role": "user", "content": ""}]))
        self.assertFalse(valid_messages([{"role": "user", "content": "x"}] * 201))

    def test_interface_has_model_history_and_export_controls(self):
        html = __import__("pathlib").Path(__file__).parents[1].joinpath("web", "index.html").read_text(encoding="utf-8")
        self.assertIn('id="model"', html)
        self.assertIn('id="export"', html)
        self.assertIn("localStorage", html)


if __name__ == "__main__":
    unittest.main()
