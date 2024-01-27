"""
(c) 2023, Tim Menzies, BSD-2

USAGE:
  python gate.py [OPTIONS]

OPTIONS:
  -c --cohen    small effect size               = .35
  -f --file     csv data file name              = ./data/diabetes.csv
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

help_str = __doc__

the = {'k': 1, 'm': 2}