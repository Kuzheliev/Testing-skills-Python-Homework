import sys
import os
import unittest
import tempfile

def generate_username(forename, surname, existing_usernames):
    base_username = (forename[0] + surname).lower()
    username = base_username
    counter = 1
    while username in existing_usernames:
        username = f"{base_username}{counter}"
        counter += 1
    existing_usernames.add(username)
    return username


def process_files(input_files, output_file):
    existing_usernames = set()
    with open(output_file, "w", encoding="utf-8") as out:
        for file in input_files:
            if not os.path.exists(file):
                print(f"Warning: file {file} not found, skipping.")
                continue

            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) < 4:
                        # Invalid line (needs at least ID, forename, surname, dept)
                        continue    

                    # Unpack with optional middle name
                    if len(parts) == 5:
                        id_str, forename, middle, surname, dept = parts
                        middle_name = middle
                    else:
                        id_str, forename, surname, dept = parts
                        middle_name = None

                    username = generate_username(forename, surname, existing_usernames)

                    if middle_name:
                        out.write(f"{id_str}:{username}:{forename}:{middle_name}:{surname}:{dept}\n")
                    else:
                        out.write(f"{id_str}:{username}:{forename}:{surname}:{dept}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py output.txt input1.txt [input2.txt ...]")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    process_files(input_files, output_file)
    print(f"Done. Output written to {output_file}")
