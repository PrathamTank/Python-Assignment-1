from collections import deque

class AhoCorasick:
    def __init__(self):
        self.children = [{}]
        self.fail = [0]
        self.output = [False]

    def insert(self, word):
        node = 0

        for ch in word.lower():
            if ch not in self.children[node]:
                self.children[node][ch] = len(self.children)
                self.children.append({})
                self.fail.append(0)
                self.output.append(False)

            node = self.children[node][ch]

        self.output[node] = True

    def build(self):
        queue = deque()

        for child in self.children[0].values():
            queue.append(child)

        while queue:
            current = queue.popleft()

            for ch, child in self.children[current].items():
                queue.append(child)

                failure = self.fail[current]

                while failure != 0 and ch not in self.children[failure]:
                    failure = self.fail[failure]

                if ch in self.children[failure]:
                    self.fail[child] = self.children[failure][ch]
                else:
                    self.fail[child] = 0

                self.output[child] = (
                    self.output[child] or
                    self.output[self.fail[child]]
                )

    def contains_banned_word(self, text):
        node = 0

        for ch in text.lower():
            while node != 0 and ch not in self.children[node]:
                node = self.fail[node]

            if ch in self.children[node]:
                node = self.children[node][ch]
            else:
                node = 0

            if self.output[node]:
                return True

        return False


def classify_password(password, automaton):
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "$#@":
            has_special = True

    if not (has_lower and has_upper and has_digit and has_special):
        return "WEAK_PATTERN"

    count = 1

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count > 3:
                return "WEAK_PATTERN"
        else:
            count = 1

    if automaton.contains_banned_word(password):
        return "COMPROMISED"

    return "STRONG"


b = int(input("Enter number of banned words: "))

automaton = AhoCorasick()

for i in range(b):
    word = input(f"Enter banned word {i + 1}: ").strip()
    automaton.insert(word)

automaton.build()

n = int(input("Enter number of passwords: "))

for i in range(1, n + 1):
    password = input(f"Enter password {i}: ")
    result = classify_password(password, automaton)
    print(f"{i}: {result}")