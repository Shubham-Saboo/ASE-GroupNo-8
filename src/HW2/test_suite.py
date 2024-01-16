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
        assert coerce("42") == 42
        assert coerce("3.14") == 3.14
        assert coerce("true") == True
        assert coerce("false") == False
        assert coerce("null") == None
        assert coerce("  hello  ") == "hello"
        assert coerce("  42  ") == 42

    def test_settings(self):
        input_str = "-c --cohen = 0.35\n -f --file = data.csv\n -h --help = False"
        result, opt_dir = settings(input_str)

        assert result == {'cohen': 0.35, 'file': 'data.csv', 'help': False}

    def test_cells(self):
        input_str = "1, 2, 3.14, true, false, null, hello"
        result = cells(input_str)
        assert result == [1, 2, 3.14, True, False, None, "hello"]

    def test_round(self):
        assert round(3.14159, 2) == 3.14
        assert round(42) == 42
        assert round("hello") == "hello"
        assert round(True) == True
        assert round(False) == False

    def test_add_num(self):
        num_obj = NUM()
        num_obj.add(5)
        assert num_obj.n == 1
        assert num_obj.mu == 5
        assert num_obj.m2 == 0
        assert num_obj.lo == 5
        assert num_obj.hi == 5

        num_obj.add(10)
        assert num_obj.n == 2
        assert num_obj.mu == 7.5
        assert num_obj.m2 == 12.5
        assert num_obj.lo == 5
        assert num_obj.hi == 10

    def test_mid_num(self):
        num_obj = NUM()
        num_obj.add(5)
        num_obj.add(10)
        assert num_obj.mid() == 7.5

    def test_div_num(self):
        num_obj = NUM()
        num_obj.add(5)
        num_obj.add(10)
        assert num_obj.div() == (12.5 / 1)**0.5

    def test_add_sym(self):
        sym_obj = SYM()
        sym_obj.add("a")
        assert sym_obj.n == 1
        assert sym_obj.has == {"a": 1}
        assert sym_obj.mode == "a"
        assert sym_obj.most == 1

        sym_obj.add("b")
        sym_obj.add("a")
        assert sym_obj.n == 3
        assert sym_obj.has == {"a": 2, "b": 1}
        assert sym_obj.mode == "a"
        assert sym_obj.most == 2

    def test_mid_sym(self):
        sym_obj = SYM()
        sym_obj.add("a")
        sym_obj.add("b")
        assert sym_obj.mid() == "a"

    def test_div_sym(self):
        sym_obj = SYM()
        sym_obj.add("a")
        sym_obj.add("b")
        sym_obj.add("a")
        sym_obj.add("c")
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