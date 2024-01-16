from utils import *
from data import DATA
from config import help_str
from test_suite import TestSuite

if __name__ == "__main__":
    t = settings(help_str)

    if t['help']:
        print("You can refer to the following help: ")
        print(help_str)
    else:
        ts = TestSuite()

        if t['run_tc'] == "all":
            print("Running all test cases!")
            ts.run_tests()
        elif t['run_tc'] != "None":
            print(f"Running test {t['run_tc']}")
            try:
                tests[t['run_tc']]()
                print(f"Test {t['run_tc']} passed.")
            except AssertionError as e:
                print(f"Test {t['run_tc']} failed: {e}")

        data = DATA(t['file'])
        print(data.stats())
