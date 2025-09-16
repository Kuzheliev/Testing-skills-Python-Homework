import unittest
import tempfile
import os
from main import generate_username, process_files

class TestUsernameGeneration(unittest.TestCase):

    def test_generate_username_basic(self):
        existing = set()
        self.assertEqual(generate_username("John", "Doe", existing), "jdoe")
        self.assertEqual(generate_username("John", "Doe", existing), "jdoe1")
        self.assertEqual(generate_username("John", "Doe", existing), "jdoe2")
        self.assertEqual(generate_username("Alice", "Smith", existing), "asmith")

    def test_process_files_normal_and_middle(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_in:
            temp_in.write("1:John:Doe:HR\n")
            temp_in.write("2:Jane:Mary:Smith:IT\n")
            temp_in_name = temp_in.name

        temp_out = tempfile.NamedTemporaryFile(mode="r+", delete=False)
        temp_out_name = temp_out.name
        temp_out.close()

        try:
            process_files([temp_in_name], temp_out_name)

            with open(temp_out_name, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]

            self.assertEqual(lines[0], "1:jdoe:John:Doe:HR")
            self.assertEqual(lines[1], "2:jsmith:Jane:Mary:Smith:IT")
        finally:
            os.remove(temp_in_name)
            os.remove(temp_out_name)

def test_process_files_duplicates_and_malformed(self):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_in:
        # First John Doe to create the initial username
        temp_in.write("1:John:Doe:HR\n")
        # Second John Doe triggers the duplicate username logic
        temp_in.write("3:John:Doe:Finance\n")
        # Malformed line
        temp_in.write("4:Incomplete\n")
        temp_in_name = temp_in.name

    temp_out = tempfile.NamedTemporaryFile(mode="r+", delete=False)
    temp_out_name = temp_out.name
    temp_out.close()

    try:
        process_files([temp_in_name], temp_out_name)

        with open(temp_out_name, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "1:jdoe:John:Doe:HR")      
        self.assertEqual(lines[1], "3:jdoe1:John:Doe:Finance") # duplicate handled
    finally:
        os.remove(temp_in_name)
        os.remove(temp_out_name)

    def test_missing_input_file(self):
        # Should print a warning but not raise an exception
        try:
            process_files(["nonexistent.txt"], tempfile.NamedTemporaryFile(delete=True).name)
        except Exception as e:
            self.fail(f"process_files raised an exception on missing file: {e}")


if __name__ == "__main__":
    unittest.main()
