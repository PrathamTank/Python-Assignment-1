class BankError(Exception):
    pass


class AccountNotFound(BankError):
    pass


class InsufficientBalance(BankError):
    pass


class InvalidAmount(BankError):
    pass


class Account:
    def __init__(self, account_id, balance):
        self._account_id = account_id
        self._balance = balance

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmount
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmount
        if amount > self._balance:
            raise InsufficientBalance
        self._balance -= amount


class Transaction:
    def __init__(self, transaction_type, account_from=None,
                 account_to=None, amount=0):
        self.transaction_type = transaction_type
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount


class Bank:
    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFound
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)
        self.history.append(
            Transaction("DEPOSIT", account_to=account_id, amount=amount)
        )

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)
        self.history.append(
            Transaction("WITHDRAW", account_from=account_id, amount=amount)
        )

    def transfer(self, from_id, to_id, amount):
        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.history.append(
            Transaction(
                "TRANSFER",
                account_from=from_id,
                account_to=to_id,
                amount=amount
            )
        )

    def snapshot(self):
        return {
            account_id: account.balance
            for account_id, account in self.accounts.items()
        }

    def rollback(self, snapshot):
        for account_id, balance in snapshot.items():
            self.accounts[account_id]._balance = balance


print("=== Bank Settlement System ===")

n = int(input("Enter number of accounts: "))

bank = Bank()

print("\nEnter account details:")

for i in range(n):
    account_id = input(f"Enter account ID for account {i + 1}: ")
    balance = int(input(f"Enter initial balance for {account_id}: "))

    bank.add_account(Account(account_id, balance))


q = int(input("\nEnter number of operations: "))

print("\nEnter operations:")
print("DEPOSIT account amount")
print("WITHDRAW account amount")
print("TRANSFER from_account to_account amount")
print("BATCH_BEGIN")
print("BATCH_END")

batch_active = False
batch_number = 0
batch_snapshot = None
batch_failed = False
failed_batches = []

for i in range(q):

    print(f"\nOperation {i + 1}:")
    parts = input("Enter operation: ").split()

    operation = parts[0]

    if operation == "BATCH_BEGIN":

        batch_active = True
        batch_number += 1
        batch_snapshot = bank.snapshot()
        batch_failed = False

    elif operation == "BATCH_END":

        if batch_active:
            if batch_failed:
                bank.rollback(batch_snapshot)
                failed_batches.append(batch_number)

            batch_active = False
            batch_snapshot = None

    else:

        try:

            if batch_failed:
                continue

            if operation == "DEPOSIT":

                account_id = parts[1]
                amount = int(parts[2])

                bank.deposit(account_id, amount)

            elif operation == "WITHDRAW":

                account_id = parts[1]
                amount = int(parts[2])

                bank.withdraw(account_id, amount)

            elif operation == "TRANSFER":

                from_id = parts[1]
                to_id = parts[2]
                amount = int(parts[3])

                bank.transfer(from_id, to_id, amount)

            else:
                raise BankError

        except BankError:

            if batch_active:
                batch_failed = True


print("\n=== Final Result ===")

for batch in failed_batches:
    print("FAILED", batch)

for account_id in sorted(bank.accounts):
    print(account_id, bank.accounts[account_id].balance)