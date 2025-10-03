# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "(": None,  # For handling parentheses
            ")": None,  # For handling parentheses
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "(": 0,  # Lowest precedence for parentheses
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        # Add spaces around operators and parentheses for easier splitting
        expression = (
            expression.replace("(", " ( ")
            .replace(")", " ) ")
            .replace("+", " + ")
            .replace("-", " - ")
            .replace("*", " * ")
            .replace("/", " / ")
        )
        return [token for token in expression.split() if token]

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if operators and operators[-1] == "(":
                    operators.pop()  # Pop the opening parenthesis
                else:
                    raise ValueError("mismatched parentheses")
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] in self.precedence
                    and self.precedence[operators[-1]] > self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            if operators[-1] == "(":
                raise ValueError("mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
