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
        'sym_mid': ts.test_add_and_mid_sym,
        'div_sym': ts.test_div_sym,
        'div_num': ts.test_div_num,
        'sym_like_different': ts.test_sym_like_different,
        'set_random_seed': ts.test_set_random_seed
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
        data = DATA(file_path)
        first_row = data.rows[0]
        print(first_row.cells)
        sorted_rows = first_row.neighbors(data, data.rows)

        for i in range(0, len(sorted_rows), 30):
            current_row = sorted_rows[i]
            distance = first_row.dist(current_row, data, 2)
            print("{:<7} {:<30} {:<10}".format(i + 1, ', '.join(map(str, current_row.cells)), round(distance, 2)))
