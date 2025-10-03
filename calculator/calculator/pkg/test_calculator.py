import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.evaluate("1 + 2"), 3)

    def test_subtract(self):
        self.assertEqual(self.calculator.evaluate("5 - 3"), 2)

    def test_multiply(self):
        self.assertEqual(self.calculator.evaluate("2 * 4"), 8)

    def test_divide(self):
        self.assertEqual(self.calculator.evaluate("10 / 2"), 5)

    def test_whitespace(self):
        self.assertEqual(self.calculator.evaluate("  1   +  2  "), 3)

    def test_empty_expression(self):
        self.assertIsNone(self.calculator.evaluate(""))

    def test_invalid_token(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("1 + a")

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(1 + 2) * 3"), 9)

    def test_nested_parentheses(self):
        self.assertEqual(self.calculator.evaluate("((1 + 2) * 3) / 3"), 3)

    def test_mismatched_parentheses_open(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("(1 + 2")

    def test_mismatched_parentheses_close(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("1 + 2)")

    def test_operator_precedence(self):
        self.assertEqual(self.calculator.evaluate("3 + 7 * 2"), 17)

if __name__ == '__main__':
    unittest.main()
