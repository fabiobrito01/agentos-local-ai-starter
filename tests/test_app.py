import unittest
from app import Handler
class TestApp(unittest.TestCase):
    def test_handler_exists(self): self.assertTrue(hasattr(Handler,"do_POST"))
if __name__=="__main__": unittest.main()
