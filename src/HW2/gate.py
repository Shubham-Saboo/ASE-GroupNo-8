from utils import *
from data import DATA
from config import help_str
from test import Test

if __name__ == "__main__":
    t = settings(help_str)

    if t['help']:
        print("You can refer to the following help: ")
        print(help_str)
    else:
        ts = Test()

        if t['run_test'] == "all":
            print("Running all test cases!")
            ts.run_tests()
        elif t['run_test'] != "None":
            print(f"Running test {t['run_test']}")
            try:
                tests[t['run_test']]()
                print(f"Test {t['run_test']} passed.")
            except AssertionError as e:
                print(f"Test {t['run_test']} failed: {e}")

        data = DATA(t['file'])
        print(data.stats())
