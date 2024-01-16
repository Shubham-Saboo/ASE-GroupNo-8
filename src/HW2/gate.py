from utils import *
from data import DATA
from config import help_str
from test import Test

if __name__ == "__main__":
    t = settings(help_str)

    if t['help']:
        print(help_str)
    else:
        ts = Test()
        tests = {
            'coerce': ts.test_coerce_with_loop,
            'cells': ts.test_cells_random_data,
            'round': ts.test_round_various_numbers,
            'num_mid': ts.test_add_and_mid_num,
            'sym_mid': ts.test_add_and_mid_sym
        }
        if(t['run_tc']=="" or t['run_tc']==None):
            pass
        elif t['run_tc'] == "all":
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
