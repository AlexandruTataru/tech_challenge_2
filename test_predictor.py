"""Unit tests"""
import unittest


class MyTestCase(unittest.TestCase):
    """Test class"""
    def test_something(self):
        """This is just a basic test made to fail"""
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
