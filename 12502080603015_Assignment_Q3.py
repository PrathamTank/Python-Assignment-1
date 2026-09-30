import re
import sys

sys.setrecursionlimit(1000000)

v = int(input())

variables = {}

for _ in range(v):
    line = input().strip()
    name, expression = line.split("=", 1)
    variables[name.strip()] = expression.strip()

expression = input().strip()

token_pattern = re.compile(r'\d+|[A-Za-z_][A-Za-z0-9_]*|[()+\-*]')


def tokenize(expr):
    tokens = token_pattern.findall(expr)

    cleaned = re.sub(r'\s+', '', expr)
    rebuilt = ''.join(tokens)

    if cleaned != rebuilt:
        raise ValueError

    return tokens


variable_tokens = {}

try:
    for name, expr in variables.items():
        variable_tokens[name] = tokenize(expr)

    main_tokens = tokenize(expression)
except:
    print("INVALID")
    sys.exit()


memo = {}
visiting = set()


def evaluate_variable(name):
    if name in memo:
        return memo[name]

    if name in visiting:
        raise RuntimeError("CYCLE")

    if name not in variable_tokens:
        raise ValueError

    visiting.add(name)

    tokens = variable_tokens[name]
    parser = Parser(tokens)
    value = parser.parse_expression()

    if parser.pos != len(tokens):
        raise ValueError

    visiting.remove(name)
    memo[name] = value

    return value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse_expression(self):
        value = self.parse_term()

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if token == "+":
                self.pos += 1
                value += self.parse_term()

            elif token == "-":
                self.pos += 1
                value -= self.parse_term()

            else:
                break

        return value

    def parse_term(self):
        value = self.parse_factor()

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if token == "*":
                self.pos += 1
                value *= self.parse_factor()
            else:
                break

        return value

    def parse_factor(self):
        if self.pos >= len(self.tokens):
            raise ValueError

        token = self.tokens[self.pos]

        if token == "(":
            self.pos += 1
            value = self.parse_expression()

            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ")":
                raise ValueError

            self.pos += 1
            return value

        if token.isdigit():
            self.pos += 1
            return int(token)

        if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
            self.pos += 1
            return evaluate_variable(token)

        raise ValueError


try:
    parser = Parser(main_tokens)
    result = parser.parse_expression()

    if parser.pos != len(main_tokens):
        raise ValueError

    print(result)

except RuntimeError:
    print("CYCLE")

except:
    print("INVALID")