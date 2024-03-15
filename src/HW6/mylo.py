from utils import *
from data import DATA
from config import help_str,the
from test import Test
from datetime import datetime
import statistics
from stats import SAMPLE, eg0

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
        
        data_new = DATA(the['file'])
        full_mid, full_div = data_new.mid_div()
        # print(full_mid, full_div)

        smo_output = []
        any50_output = []

        budget0, budget, some = 4, 10, 0.5
        for i in range(20):
            random_seed = set_random_seed()
            d = DATA(file_path) 
            ign1, ign2, line = d.gate(random_seed, budget0, budget, some)
            smo_output.append(line)
            any50_output.append(d.any50(random_seed))

        best = d.best_100(random_seed)
    
        print("date : {} \nfile : {} \nrepeat : {} \nseed : {} \nrows : {} \ncols : {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),the['file'],"20",the['seed'],len(data_new.rows), len(data_new.rows[0].cells)))
        print("names : \t{}\t\t{}".format(d.cols.names,"D2h-"))
        print("mid : \t\t{}\t\t\t\t{}".format(list(full_mid[0].values())[1:],full_mid[1]))
        print("div : \t\t{}\t\t\t\t\t{}".format(list(full_div[0].values())[1:],full_div[1]))
        print("#")
        smo_output = sorted(smo_output, key=lambda x: x[1])
        for op in smo_output:
            print("smo9\t\t{}\t\t\t\t{}".format(op[0],op[1]))
        print("#")
        any50_output = sorted(any50_output, key=lambda x: x[1])
        for op in any50_output:
            print("any50\t\t{}\t\t\t\t{}".format(op[0],op[1]))
        print("#")
        print("100%\t\t{}\t\t\t\t{}".format(best[0],best[1]))

       
