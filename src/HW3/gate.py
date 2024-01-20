from utils import *
from data import DATA
from config import help_str, the
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
        if(t['run_tc'] == "" or t['run_tc'] is None):
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
        # print(data.stats())

        def learn(data, row, my, n_hypotheses, most, tmp, out):
            my['n'] += 1
            kl = row.cells[data.cols.klass.at]
            if my['n'] > 10:
                my['tries'] += 1
                my['acc'] += 1 if kl == row.likes(my['datas'], my['n'], n_hypotheses, most, tmp, out)[0] else 0
            my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
            my['datas'][kl].add(row)


        def bayes():
            wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
            n_hypotheses, most, tmp, out = 0, None, None, None  # Add these variables
            DATA(t['file'], lambda data, t: learn(data, t, wme, n_hypotheses, most, tmp, out))
            accuracy = wme['acc'] / wme['tries']
            print(accuracy)
            return accuracy


        bayes()