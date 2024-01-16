import sys
import io
import math
import random
from num import NUM
from sym import SYM
from data import DATA
from utils import coerce, settings, cells, csv, round
import os
import platform

class Test:

    def test_coerce_with_loop(self):
        values_to_test = [("100", 100), ("3.14", 3.14), 
                          ("False", False), ("Hello", "Hello")]
        for input_val, expected_output in values_to_test:
            assert coerce(input_val) == expected_output

    def test_cells_random_data(self):
        random_numbers = [random.randint(1, 100) for _ in range(5)]
        input_str = ", ".join(map(str, random_numbers))
        result = cells(input_str)
        assert result == random_numbers

    def test_round_various_numbers(self):
        numbers_to_round = [(3.14159, 2, 3.14), (10.8, 0, 11), 
                            (0.333, 1, 0.3)]
        for num, precision, expected in numbers_to_round:
            assert round(num, precision) == expected

    def test_add_and_mid_num(self):
        num_obj = NUM()
        for num in [10, 20, 30, 40, 50]:
            num_obj.add(num)
        assert num_obj.mid() == 30
    
    def test_add_and_mid_sym(self):
        sym_obj = SYM()
        for x in ["a","a","a","b","b","c","d"]:
            sym_obj.add(x)
        return sym_obj.mid() == "a"

    def _run_test(self, test_func, test_name):
        try:
            test_func()
            print(f"Test {test_name} passed.")
        except AssertionError as e:
            print(f"Test {test_name} failed: {e}")

    def run_tests(self):
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
	test = Test()
	test.run_tests()
