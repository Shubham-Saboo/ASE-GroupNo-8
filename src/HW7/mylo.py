from utils import *
from data import DATA
from config import help_str,the
from test import Test
from datetime import datetime
from ranges import RANGE

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


        def _mergeds(ranges, tooFew):
            i, t = 0, []
            while i < len(ranges):
                a = ranges[i]
                if i < len(ranges) - 1:
                    both = a.merged(ranges[i + 1], tooFew)
                    if both:
                        a = both
                        i += 1
                t.append(a)
                i += 1

            if len(t) < len(ranges):
                return _mergeds(t, tooFew)

            for i in range(1, len(t)):
                t[i].x['lo'] = t[i - 1].x['hi']

            t[0].x['lo'] = float('-inf')
            t[-1].x['hi'] = float('inf')

            return t

        def _ranges1(col, rowss):
            out, nrows = {}, 0
            for y, rows in rowss.items():
                nrows += len(rows)
                for row in rows:
                    x = row.cells[col.at]
                    if x != "?":
                        bin_ = col.bin(x)
                        out[bin_] = RANGE(col.at, col.txt, x)
                        out[bin_].add(x, y)

            out = list(out.values())
            out.sort(key=lambda a: a.x['lo'])

            return out if hasattr(col, 'has') else _mergeds(out, nrows / the['bins'])

        file_path = the['file']
        d = DATA(file_path)
        
        best, rest, _ = d.branch()
        LIKE = best.rows
        HATE = rest.rows[:3 * len(LIKE)]

        def score(range):
            return range.score("LIKE", len(LIKE), len(HATE))

        t = []
        for col in d.cols.x:
            print("")
            for range_ in _ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
                temp_x = {'hi': range_.x['hi'], 'lo': range_.x['lo']}
                temp_y = {key: range_.y[key] for key in ('HATE', 'LIKE') if key in range_.y}
                d = {'at': range_.at + 1, 'scored': range_.scored, 'txt': range_.txt, 'x': temp_x, 'y': temp_y}
                print(d)
                t.append(range_)

        t.sort(key=lambda x: score(x), reverse=True)
        max_score = score(t[0])

        print("\n#scores:\n")
        for v in t[:int(the['Beam'])]:
            if score(v) > max_score * 0.1:
                print(round(score(v)))  

        print({"LIKE": len(LIKE), "HATE": len(HATE)})

