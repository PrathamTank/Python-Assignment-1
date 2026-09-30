import csv
from datetime import datetime

file_path = input("Enter CSV file path: ").strip()

balances = {}

try:
    with open(file_path, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        required = ["tid", "acc", "type", "amount", "time"]

        if reader.fieldnames != required:
            raise ValueError("Invalid CSV header")

        with open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
             open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
             open("error.csv", "w", newline="", encoding="utf-8") as error_file:

            credit_writer = csv.DictWriter(credit_file, fieldnames=required)
            debit_writer = csv.DictWriter(debit_file, fieldnames=required)
            error_writer = csv.writer(error_file)

            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writerow(required + ["reason"])

            for row in reader:
                try:
                    tid = row["tid"].strip()
                    acc = row["acc"].strip()
                    trans_type = row["type"].strip().upper()
                    amount_text = row["amount"].strip()
                    timestamp = row["time"].strip()

                    if not tid:
                        raise ValueError("Invalid transaction_id")

                    if not acc:
                        raise ValueError("Invalid account_id")

                    if trans_type not in ("CREDIT", "DEBIT"):
                        raise ValueError("Invalid transaction type")

                    amount = float(amount_text)

                    if amount <= 0:
                        raise ValueError("Amount must be greater than 0")

                    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

                    if trans_type == "CREDIT":
                        credit_writer.writerow(row)
                        balances[acc] = balances.get(acc, 0) + amount
                    else:
                        debit_writer.writerow(row)
                        balances[acc] = balances.get(acc, 0) - amount

                except Exception as e:
                    error_writer.writerow(list(row.values()) + [str(e)])

except FileNotFoundError:
    print("Error: File not found.")
    exit()

except PermissionError:
    print("Error: Permission denied.")
    exit()

except Exception as e:
    print(f"Error: {e}")
    exit()


sorted_balances = sorted(
    balances.items(),
    key=lambda x: abs(x[1]),
    reverse=True
)

print("\nAccount-wise balance changes:")

for account, balance in sorted_balances:
    if balance == int(balance):
        balance = int(balance)

    print(account, balance)

print("\nFiles created:")
print("credit.csv")
print("debit.csv")
print("error.csv")