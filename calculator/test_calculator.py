import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_standard_precedence(self):
        # According to standard mathematical precedence, 3 + 7 * 2 should be 17
        self.assertEqual(Calculator().evaluate("3 + 7 * 2"), 17.0)

    def test_user_expected_result(self):
        # To get 20, the user needs to use parentheses: (3 + 7) * 2
        self.assertEqual(Calculator().evaluate("(3 + 7) * 2"), 20.0)

if __name__ == '__main__':
    unittest.main()
