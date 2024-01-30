from utils import *
from data import DATA
from config import help_str, the
from test import Test

if __name__ == "__main__":
    the = settings(help_str)

    if the['help']:
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
        if(the['run_tc'] == "" or the['run_tc'] is None):
            pass
        elif the['run_tc'] == "all":
            print("Running all test cases!")
            ts.run_tests()
        elif the['run_tc'] != "None":
            print(f"Running test {the['run_tc']}")
            try:
                tests[the['run_tc']]()
                print(f"Test {the['run_tc']} passed.")
            except AssertionError as e:
                print(f"Test {the['run_tc']} failed: {e}")

        file_path = the['file']

        def gate():
            budget0, budget, some = 4, 10, 0.5
            for i in range(20):
                d = DATA(file_path) 
                d.gate(budget0, budget, some)

            print('\n'.join(map(str, DATA.list_1)))
            print('\n')
            print('\n'.join(map(str, DATA.list_2)))
            print('\n')
            print('\n'.join(map(str, DATA.list_3)))
            print('\n')
            print('\n'.join(map(str, DATA.list_4)))
            print('\n')
            print('\n'.join(map(str, DATA.list_5)))
            print('\n')
            print('\n'.join(map(str, DATA.list_6)))

        gate()
        