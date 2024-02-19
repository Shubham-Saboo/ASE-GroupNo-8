from utils import *
from data import DATA
from config import help_str,the
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
        'set_random_seed': ts.test_set_random_seed,
        'test_far':ts.test_far
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

        # print("Task 1: Get distance working\n")
        # first_row = data.rows[0]
        # sorted_rows = first_row.neighbors(data)

        # for i in range(0, len(sorted_rows), 30):
        #     current_row = sorted_rows[i]
        #     distance = first_row.dist(current_row, data)

        #     print("{:<7} {:<50} {:<10}".format(i + 1, ', '.join(map(str, current_row.cells)), round(distance, 2)))
    

        data_new = DATA(the['file'])
        # DATA.far(the, data_new)

        # print("Task 1: Implementing the recursive tree\n")
        # t, evals = data_new.tree(True)
        # t.show()
        # print("evals: ", evals)

        # print("Task 2: Optimization output - Single Descent\n")
        # best, rest, evals = data_new.branch()
        # print("centroid of output cluster: ")
        # print(o(best.mid().cells), o(rest.mid().cells))
        # print("evals: ", evals)

        print("Task 3: doubletap\n")
        best1, rest, evals1 = data_new.branch(32)
        best2, _, evals2 = best1.branch(4)
        print("median and best found in that four: ")
        print(o(best2.mid().cells), o(rest.mid().cells))
        print("evals: ",evals1 + evals2)