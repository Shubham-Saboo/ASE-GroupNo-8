import sys
import io
import math
from num import NUM
from sym import SYM
from data import DATA
from utils import coerce, settings, cells, csv, round, cli
import os
import platform
class TestSuite:
 
    def test_coerce(self):
        assert coerce("100") == 100
        assert coerce("2.718") == 2.718
        assert coerce("True") == True
        assert coerce("False") == False
        assert coerce("None") == None
        assert coerce("  world  ") == "world"
     
    def test_settings(self):
        input_str = "-e --epsilon = 0.05\n -s --seed = 42\n -v --verbose = True"
        result, opt_dir = settings(input_str)

        assert result == {'epsilon': 0.05, 'seed': 42, 'verbose': True}


    def test_cells(self):
        input_str = "10, 20, 2.718, false, true, none, world"
        result = cells(input_str)
        assert result == [10, 20, 2.718, False, True, None, "world"]


    def test_round(self):
        assert round(2.71828, 3) == 2.718
        assert round(100) == 100
        assert round("world") == "world"
        assert round(None) == None


    def test_add_num(self):
        num_obj = NUM()
        num_obj.add(15)
        assert num_obj.n == 1
        assert num_obj.mu == 15
        assert num_obj.m2 == 0
        assert num_obj.lo == 15
        assert num_obj.hi == 15

        num_obj.add(5)
        assert num_obj.n == 2
        assert num_obj.mu == 10
        assert num_obj.m2 == 50
        assert num_obj.lo == 5
        assert num_obj.hi == 15


    def test_mid_num(self):
        num_obj = NUM()
        num_obj.add(15)
        num_obj.add(5)
        assert num_obj.mid() == 10


    def test_div_num(self):
        num_obj = NUM()
        num_obj.add(15)
        num_obj.add(5)
        assert num_obj.div() == (50 / 1)**0.5


    def test_add_sym(self):
        sym_obj = SYM()
        sym_obj.add("x")
        assert sym_obj.n == 1
        assert sym_obj.has == {"x": 1}
        assert sym_obj.mode == "x"
        assert sym_obj.most == 1

        sym_obj.add("y")
        sym_obj.add("x")
        sym_obj.add("x")
        assert sym_obj.n == 4
        assert sym_obj.has == {"x": 3, "y": 1}
        assert sym_obj.mode == "x"
        assert sym_obj.most == 3


    def test_mid_sym(self):
        sym_obj = SYM()
        sym_obj.add("x")
        sym_obj.add("y")
        assert sym_obj.mid() == "a"

    def test_div_sym(self):
        sym_obj = SYM()
        sym_obj.add("x")
        sym_obj.add("x")
        sym_obj.add("y")
        sym_obj.add("z")
        assert math.isclose(sym_obj.div(), 1.5)

    def test_small_sym(self):
        sym_obj = SYM()
        assert sym_obj.small() == 0

    def _run_test(self, test_func, test_name):
        try:
            test_func()
            print(f"Test {test_name} passed.")
        except AssertionError as e:
            # self.f_tests[test_name[5:]] = test_name[5:]  # append to failing test lists
            print(f"Test {test_name} failed: {e}")

    def run_tests(self):
        print("Running tests in TestSuite")
        test_functions = [func for func in dir(self) if func.startswith('test_') and callable(getattr(self, func))]
        for test_func_name in test_functions:
            test_func = getattr(self, test_func_name)
            self._run_test(test_func, test_func_name)        
        

def set_environment_variable(variable_name, value):
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system(f'setx {variable_name} "{value}"')
    else:
        os.system(f'export {variable_name}="{value}"')

if __name__ == '__main__':
    test_suite = TestSuite()
    test_suite.run_tests()
