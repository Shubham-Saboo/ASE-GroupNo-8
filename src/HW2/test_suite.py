import sys
import math
from num import NUM
from sym import SYM
from data import DATA
from utils import coerce, settings, cells, csv, round


class UtilityTestSuite:

    def test_coerce(self):
        assert coerce("42") == 42
        assert coerce("3.14159265359") == 3.14159265359
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
        input_str = "1, 2, 3.14159265359, true, false, null, hello"
        result = cells(input_str)
        assert result == [1, 2, 3.14159265359, True, False, None, "hello"]

    def test_round(self):
        assert round(3.14159265359, 2) == 3.14
        assert round(42) == 42
        assert round("world") == "world"
        assert round(True) == True
        assert round(False) == False

    def _run_test(self, test_func, test_name):
        try:
            test_func()
            print(f"Test {test_name} passed.")
        except AssertionError as e:
            print(f"Test {test_name} failed: {e}")

    def run_tests(self):
        print("Running tests in UtilityTestSuite")
        test_functions = [func for func in dir(self) if func.startswith('test_') and callable(getattr(self, func))]
        for test_func_name in test_functions:
            test_func = getattr(self, test_func_name)
            self._run_test(test_func, test_func_name)


class NumTestSuite:

    def test_add(self):
        num_obj = NUM()
        num_obj.add(10)
        assert num_obj.n == 1
        assert num_obj.mu == 10
        assert num_obj.m2 == 0
        assert num_obj.lo == 10
        assert num_obj.hi == 10

        num_obj.add(20)
        assert num_obj.n == 2
        assert num_obj.mu == 15
        assert num_obj.m2 == 50
        assert num_obj.lo == 10
        assert num_obj.hi == 20

    def test_mid(self):
        num_obj = NUM()
        num_obj.add(5)
        num_obj.add(15)
        assert num_obj.mid() == 10

    def test_div(self):
        num_obj = NUM()
        num_obj.add(5)
        num_obj.add(15)
        assert math.isclose(num_obj.div(), (50 / 1) ** 0.5)

    def _run_test(self, test_func, test_name):
        try:
            test_func()
            print(f"Test {test_name} passed.")
        except AssertionError as e:
            print(f"Test {test_name} failed: {e}")

    def run_tests(self):
        print("Running tests in NumTestSuite")
        test_functions = [func for func in dir(self) if func.startswith('test_') and callable(getattr(self, func))]
        for test_func_name in test_functions:
            test_func = getattr(self, test_func_name)
            self._run_test(test_func, test_func_name)


class SymTestSuite:

    def test_add(self):
        sym_obj = SYM()
        sym_obj.add("apple")
        assert sym_obj.n == 1
        assert sym_obj.has == {"apple": 1}
        assert sym_obj.mode == "apple"
        assert sym_obj.most == 1

        sym_obj.add("banana")
        sym_obj.add("apple")
        assert sym_obj.n == 3
        assert sym_obj.has == {"apple": 2, "banana": 1}
        assert sym_obj.mode == "apple"
        assert sym_obj.most == 2

    def test_mid(self):
        sym_obj = SYM()
        sym_obj.add("apple")
        sym_obj.add("banana")
        assert sym_obj.mid() == "apple"

    def test_div(self):
        sym_obj = SYM()
        sym_obj.add("apple")
        sym_obj.add("banana")
        sym_obj.add("apple")
        sym_obj.add("cherry")
        assert math.isclose(sym_obj.div(), 1.5)

    def test_small(self):
        sym_obj = SYM()
        assert sym_obj.small() == 0

    def _run_test(self, test_func, test_name):
        try:
            test_func()
            print(f"Test {test_name} passed.")
        except AssertionError as e:
            print(f"Test {test_name} failed: {e}")

    def run_tests(self):
        print("Running tests in SymTestSuite")
        test_functions = [func for func in dir(self) if func.startswith('test_') and callable(getattr(self, func))]
        for test_func_name in test_functions:
            test_func = getattr(self, test_func_name)
            self._run_test(test_func, test_func_name)


if __name__ == '__main__':
    util_test_suite = UtilityTestSuite()
    util_test_suite.run_tests()

    num_test_suite = NumTestSuite()
    num_test_suite.run_tests()

    sym_test_suite = SymTestSuite()
    sym_test_suite.run_tests()
