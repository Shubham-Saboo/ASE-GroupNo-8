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


        d = DATA(the['file'])
        best, rest, _ = d.branch()
        LIKE = best.rows
        HATE = slice(random.sample(rest.rows, min(3 * len(LIKE), len(rest.rows))))
        def score(range_):
            return range_.score("LIKE", len(LIKE), len(HATE))
        print()
        print("PART - 1")
        t = []
        for col in list(d.cols.x):
            print("")
            for range_ in _ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
                temp_x = {'hi':range_.x['hi'], 'lo':range_.x['lo']}
                temp_y = {}
                if 'HATE' in range_.y:
                    temp_y['HATE'] = range_.y['HATE']
                if 'LIKE' in range_.y:
                    temp_y['LIKE'] = range_.y['LIKE']
                d = {'at':(range_.at)+1, 'scored':range_.scored, 'txt':range_.txt, 'x':temp_x, 'y':temp_y}
                print(d)
                t.append(range_)
        t.sort(key=lambda a: score(a), reverse=True)
        max_score = score(t[0])
        print("\n\nPART - 2")
        print("\n#scores:\n")
        for v in t[:int(the['Beam'])]:
            if score(v) > max_score * 0.1:
                temp_x = {'hi':v.x['hi'], 'lo':v.x['lo']}
                temp_y = {}
                if 'HATE' in v.y:
                    temp_y['HATE'] = v.y['HATE']
                if 'LIKE' in v.y:
                    temp_y['LIKE'] = v.y['LIKE']
                d_v = {'at':(v.at)+1, 'scored':v.scored, 'txt':v.txt, 'x':temp_x, 'y':temp_y}
                print("{:.2f}".format(round(score(v), 2)), d_v)
        print({"HATE": len(HATE),"LIKE": len(LIKE),})