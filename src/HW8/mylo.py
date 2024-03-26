from utils import *
from data import DATA
from config import help_str,the
from test import Test
from datetime import datetime
from ranges import RANGE
from rules import Rules

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
        
        def _ranges(cols, rowss):
            t = []
            for col in cols:
                for range in _ranges1(col, rowss):
                    t.append(range)
            return t

        def _ranges1(col, rowss):
            out, nrows = {}, 0
            for y, rows in rowss.items():
                nrows += len(rows)
                for row in list(rows):
                    x = row.cells[col.at]
                    if x != "?":
                        bin = col.bin(x)
                        if bin not in out:
                            out[bin] = RANGE(col.at, col.txt, x)
                        out[bin].add(x, y)
            out = list(out.values())
            out.sort(key=lambda r: r.x['lo'])
            return out if hasattr(col, 'has') else _mergeds(out, nrows / the['bins'])

        def _mergeds(ranges, tooFew):
            t = []
            i = 1
            while i <= len(ranges):
                a = ranges[i-1]
                if i < len(ranges):
                    both = a.merged(ranges[i], tooFew)
                    if both:
                        a = both
                        i += 1
                t.append(a)
                i += 1
            if len(t) < len(ranges):
                return _mergeds(t, tooFew)
            for i in range(1, len(t)):
                t[i].x['lo'] = t[i - 1].x['hi']
            t[0].x['lo'] = -math.inf
            t[-1].x['hi'] = math.inf
            return t

        print("score    mid selected                                          rule")
        print("-----   --------------------------------------------------     ------")

        d = DATA(the['file'])
        tmp = shuffle(d.rows)
        train = d.clone(tmp[:len(tmp) // 2])
        test = d.clone(tmp[len(tmp) // 2:])
        test.rows.sort(key=lambda row: row.d2h(d))
        test.rows = shuffle(test.rows)
        best0, rest, evals1 = train.branch(the['d'])
        best, _, evals2 = best0.branch(the['D'])
        LIKE = best.rows
        HATE = slice(shuffle(rest.rows), 1, 3 * len(LIKE))
        rowss = {'LIKE': LIKE, 'HATE': HATE}
        test.rows = shuffle(test.rows)
        random = test.clone(slice(test.rows, 1, int(evals1 + evals2 + the['D'] - 1)))
        random.rows.sort(key=lambda row: row.d2h(d))
        for i, rule in enumerate(Rules(_ranges(train.cols.x, rowss), "LIKE", rowss).sorted):
            result = train.clone(rule.selects(test.rows))
            if len(result.rows) > 0:
                result.rows.sort(key=lambda row: row.d2h(d))
                print(round(rule.scored), "\t", o(result.mid().cells), "\t", rule.show())
