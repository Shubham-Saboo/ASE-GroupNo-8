from utils import *
from data import DATA
from config import help_str, egs
from test_suite import TestSuite


if __name__ == "__main__":
    t, opt_dir = settings(help_str)
    t = cli(t, opt_dir)
    if(t['help']):
        print("You can use the following help: ")
        print(help_str)
    else:
        if(t['run_tc']=="all"):
            print("running all tests!")
            ts = TestSuite()
            ts.run_tests()
        elif(t['run_tc']==""):
            pass
        elif(t['run_tc']!="None"):
            print("running test "+ t['run_tc'])
            ts = TestSuite()
            try:
                egs[t['run_tc']]()
                print(f"Test {t['run_tc']} passed.")
            except AssertionError as e:
                print(f"Test {t['run_tc']} failed: {e}")

    data = DATA(t['file'])
    
