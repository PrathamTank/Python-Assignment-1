class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


variables = {}


def get_value(value):
    try:
        return float(value)
    except ValueError:
        if value in variables:
            return variables[value]
        raise UnknownVariableError(
            f"Unknown variable: {value}"
        )


def calculate(left, operator, right):
    left = get_value(left)
    right = get_value(right)

    if operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return left * right
    elif operator == "/":
        if right == 0:
            raise DivisionByZeroError(
                "Cannot divide by zero"
            )
        return left / right
    elif operator == "%":
        if right == 0:
            raise DivisionByZeroError(
                "Cannot perform modulo by zero"
            )
        return left % right
    else:
        raise UnsupportedOperatorError(
            f"Unsupported operator: {operator}"
        )


print("=== Interactive Formula Validator ===")
print("Enter formulas, assignments, or quit.")

while True:

    try:
        line = input("\nEnter formula: ").strip()

        if line.lower() == "quit":
            print("Calculator terminated.")
            break

        if not line:
            raise InvalidFormatError(
                "Formula cannot be empty"
            )

        if "=" in line:
            parts = line.split("=")

            if len(parts) != 2:
                raise InvalidFormatError(
                    "Invalid assignment format"
                )

            variable = parts[0].strip()
            value = parts[1].strip()

            if not variable.isidentifier():
                raise InvalidFormatError(
                    "Invalid variable name"
                )

            if not value:
                raise InvalidFormatError(
                    "Missing value"
                )

            try:
                variables[variable] = float(value)
            except ValueError:
                if value not in variables:
                    raise UnknownVariableError(
                        f"Unknown variable: {value}"
                    )
                variables[variable] = variables[value]

            continue

        parts = line.split()

        if len(parts) != 3:
            raise InvalidFormatError(
                "Formula must be: operand operator operand"
            )

        left, operator, right = parts

        result = calculate(left, operator, right)

        if result.is_integer():
            print(int(result))
        else:
            print(result)

    except InvalidFormatError as e:
        print("InvalidFormatError")
        print(e)

    except UnknownVariableError as e:
        print("UnknownVariableError")
        print(e)

    except DivisionByZeroError as e:
        print("DivisionByZeroError")
        print(e)

    except UnsupportedOperatorError as e:
        print("UnsupportedOperatorError")
        print(e)