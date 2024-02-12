from row import ROW
from num import NUM
from sym import SYM
from cols import COLS
from utils import *;
from config import the
import math
import random

class DATA:

    def __init__(self, src=[], fun=None):
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            for _, x in csv(src):
                self.add(x, fun)
        else:
            self.add(src, fun)

    def add(self, t, fun=None):
        row = t if isinstance(t, ROW) else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [round(col.mid(),2) for col in (cols or self.cols.all)]
        return ROW(u)

    def stats(data):
        statistics = {}
        total_rows = max(col.n for col in data.cols.all)
        statistics[".N"] = total_rows
        for col in data.cols.all:
            if isinstance(col, NUM):
                mean = col.mid()
                statistics[f"{col.txt}"] = round(mean, 2)
            elif isinstance(col, SYM):
                mode = col.mid()
                statistics[f"{col.txt}"] = int(mode) if type(mode) == float else mode
        return statistics
    
    def farapart(self, rows, sortp, a=None, b=None, far=None, evals=0):
        far = int(len(rows) * 0.95) + 1
        evals = 1 if a is not None else 2
        
        a = a or random.choice(rows)
    
        sorted_neighbors = a.neighbors(self, rows)
        a = a or sorted_neighbors[0]
        b = sorted_neighbors[min(far, len(sorted_neighbors) - 1)]
        
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        
        return a, b, a.dist(b, self), evals

    
    def half(self, rows, sortp, before, evals):
        the_half = min(len(rows) // 2, len(rows))
        some = random.sample(rows, the_half)
        a, b, C, evals = self.farapart(some, sortp, before)
        def d(row1, row2):
            return self.dist(row1, row2)
        
        def project(r):
            return (d(r, a)**2 + C**2 - d(r, b)**2) / (2 * C)
        rows_sorted = sorted(rows, key=project)
        mid_point = len(rows) // 2
        as_ = rows_sorted[:mid_point]
        bs = rows_sorted[mid_point:]
        return as_, bs, a, b, C, d(a, bs[0]), evals
    
    def far(the, data_new):
        print()
        print("Task 2: Get Far Working\n")
        target_distance = 0.95
        current_distance = 0
        attempts = 0

        while current_distance < target_distance and attempts < 200:
            a, b, C, _ = data_new.farapart(data_new.rows, sortp=True)
            current_distance = C
            attempts += 1
            #print(f"Attempt {attempts}: Current Distance = {C}")
        if current_distance <= target_distance:
            #print("Far apart points found:")
            print(f"far1: {a.cells}")
            print(f"far2: {b.cells}")
            print(f"distance: {current_distance}")
        else:
            print("No pair found within the target distance after maximum attempts.")

        print(f"Total Attempts: {attempts}")
        return current_distance, attempts