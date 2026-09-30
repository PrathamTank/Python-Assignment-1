import os
import re
import sys
import pickle
import zipfile

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")

mode = input("Enter mode (BUILD/SEARCH): ").strip().upper()

if mode == "BUILD":
    folder = input("Enter logs folder path: ").strip()
    zip_name = input("Enter output zip name: ").strip()

    index = {}
    total_files = 0
    total_lines = 0

    log_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".txt"):
                log_files.append(os.path.join(root, file))

    for file_path in sorted(log_files):
        total_files += 1
        file_name = os.path.relpath(file_path, folder)

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_number, line in enumerate(f, 1):
                    total_lines += 1
                    tokens = set(TOKEN_PATTERN.findall(line.lower()))

                    for token in tokens:
                        if token not in index:
                            index[token] = []
                        index[token].append((file_name, line_number))
        except OSError:
            continue

    pickle_name = "index.pkl"

    with open(pickle_name, "wb") as f:
        pickle.dump(index, f, protocol=pickle.HIGHEST_PROTOCOL)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in log_files:
            archive.write(
                file_path,
                os.path.relpath(file_path, folder)
            )
        archive.write(pickle_name)

    os.remove(pickle_name)

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))

elif mode == "SEARCH":
    pickle_path = input("Enter pickle file path: ").strip()
    q = int(input("Enter number of query tokens: "))

    queries = []

    for i in range(q):
        token = input(f"Enter query token {i + 1}: ").strip().lower()
        queries.append(token)

    try:
        with open(pickle_path, "rb") as f:
            index = pickle.load(f)

        for token in queries:
            print(token)

            matches = index.get(token, [])

            for file_name, line_number in matches:
                print(f"{file_name}:{line_number}")

    except FileNotFoundError:
        print("ERROR File not found")
    except (pickle.PickleError, EOFError):
        print("ERROR Invalid pickle file")

else:
    print("ERROR Invalid mode")