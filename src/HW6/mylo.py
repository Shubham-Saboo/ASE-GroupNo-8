from utils import *
from data import DATA
from config import help_str,the
from test import Test
from datetime import datetime
import statistics
from stats import SAMPLE, eg0

def hw7_part2(the):
    print("\n")
    print("\n")
    d = DATA(src = the['file'])
    print("date:{}\nfile:{}\nrepeat:{}\nseed:{}\nrows:{}\ncols:{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),the['file'],"20",the['seed'],len(d.rows), len(d.rows[0].cells)))
    sortedRows =  sorted(d.rows, key=lambda x: x.d2h(d))
    print(f"best: {o(sortedRows[0].d2h(d),n=2)}")
    all = base(d)
    print(f"tiny: {o(statistics.stdev(all)*0.35,n=2)}")
    print("#base #bonr9 #rand9 #bonr15 #rand15 #bonr20 #rand20 #rand358 ")
    eg0([
        SAMPLE(randN(d,9, the=the), "rand9"),
        SAMPLE(randN(d,15, the=the), "rand15"),
        SAMPLE(randN(d,20, the=the), "rand20"), 
        SAMPLE(randN(d,358, the=the), "rand358"), 
        SAMPLE(bonrN(d,9, the=the), "bonr9"),
        SAMPLE(bonrN(d,15,the=the), "bonr15"),
        SAMPLE(bonrN(d,20, the=the), "bonr20"),
        SAMPLE(base(d), "base")
    ])

def base(d):
    baseline_output = [row.d2h(d) for row in d.rows]
    return baseline_output

def randN(d, n, the):
    random.seed(the['seed'])
    rand_arr = []
    for _ in range(20):
        rows = d.rows
        random.shuffle(rows)
        rowsN = random.sample(rows,n)
        rowsN.sort(key=lambda row: row.d2h(d))
        rand_arr.append(round(rowsN[0].d2h(d),2))

    return rand_arr

def bonrN(d, n, the):
    bonr_arr = []
    for _ in range(20):
        _,_, best_stats = d.gate(the['seed'], 4, n-4, 0.5)
        bonr_arr.append(best_stats[1])

    return bonr_arr

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

        hw7_part2(the)

       
