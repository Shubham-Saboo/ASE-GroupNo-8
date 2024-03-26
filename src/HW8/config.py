"""
(c) 2023, Tim Menzies, BSD-2

USAGE:
  python gate.py [OPTIONS]

OPTIONS:
  -b --bins     maximum number of bins          = 16
  -B --Beam     max number of ranges            = 10
  -S --Support  coefficient on best             = 2
  -c --cohen    small effect size               = .35
  -C --Cut      ignore ranges less than C*max   = .1
  -d --d        first cut                       = 32
  -D --D        second cut                      = 4
  -f --file     csv data file name              = ./data/auto93.csv
  -h --help     show help                       = False
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
  -t --run_tc   run test-cases                  = None

LIST OF TESTS:
  all test cases:
    'all'
  individual test cases:  
    'coerce': ts.test_coerce_with_loop,
    'cells': ts.test_cells_random_data,
    'round': ts.test_round_various_numbers,
    'num_mid': ts.test_add_and_mid_num,
    'sym_mid': ts.test_add_and_mid_sym
"""
import re
from utils import *
help_str = __doc__

def settings(s):
    t = {}
    opt_dir = {}
    opts = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', s)
    for short_form, full_form, default_value in opts:
        t[full_form] = coerce(default_value)
        opt_dir[short_form] = full_form

    options = sys.argv[1:]
    if "--help" in options or "-h" in options:
        t["help"] = True
        return t

    options_dict = {}
    for i in range(0, len(options), 2):
        opt = options[i]
        val = options[i + 1] if i + 1 < len(options) else None
        options_dict[opt] = val

    for opt, val in options_dict.items():
        key = opt[2:] if opt.startswith('--') else opt_dir[opt[1:]]
        t[key] = coerce(val)

    return t
# the = {'k': 1, 'm': 2}
the = settings(help_str)