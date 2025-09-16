import sys
import os
import importlib.util
import json
from datetime import datetime

def load_program(module_path):
    """Load main.py as a module."""
    spec = importlib.util.spec_from_file_location("main", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_tests(ugen_module, test_data_file, report_file="test_report.html"):
    """Run tests and generate HTML report."""
    with open(test_data_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []

    for idx, case in enumerate(test_cases, 1):
        description = case.get("description", f"Test {idx}")
        input_data = case.get("input")
        expected_username = case.get("expected_username")
        existing_usernames = set(case.get("existing_usernames", []))

        try:
            # Generate username
            actual_username = ugen_module.generate_username(
                input_data["forename"],
                input_data["surname"],
                existing_usernames
            )
            passed = actual_username == expected_username
            results.append({
                "description": description,
                "input": input_data,
                "expected": expected_username,
                "actual": actual_username,
                "passed": passed
            })
        except Exception as e:
            results.append({
                "description": description,
                "input": input_data,
                "expected": expected_username,
                "actual": str(e),
                "passed": False
            })

    # Generate HTML report
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Username Generator Test Report</title></head><body>")
        f.write(f"<h1>Test Report - {datetime.now()}</h1>")
        f.write(f"<h2>Total tests: {len(results)}</h2>")
        passed_count = sum(1 for r in results if r["passed"])
        f.write(f"<h2>Passed: {passed_count}, Failed: {len(results) - passed_count}</h2>")
        f.write("<table border='1' cellpadding='5'><tr><th>#</th><th>Description</th><th>Input</th><th>Expected</th><th>Actual</th><th>Result</th></tr>")
        for i, r in enumerate(results, 1):
            color = "green" if r["passed"] else "red"
            f.write(f"<tr><td>{i}</td><td>{r['description']}</td><td>{r['input']}</td><td>{r['expected']}</td><td>{r['actual']}</td><td style='color:{color}'>{'PASS' if r['passed'] else 'FAIL'}</td></tr>")
        f.write("</table></body></html>")

    print(f"Test report generated: {report_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 test.py main.py test_data.json")
        sys.exit(1)

    program_file = sys.argv[1]
    test_data_file = sys.argv[2]

    if not os.path.exists(program_file):
        print(f"Program file not found: {program_file}")
        sys.exit(1)
    if not os.path.exists(test_data_file):
        print(f"Test data file not found: {test_data_file}")
        sys.exit(1)

    ugen_module = load_program(program_file)
    run_tests(ugen_module, test_data_file)
