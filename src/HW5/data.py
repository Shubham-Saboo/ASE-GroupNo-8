from row import ROW
from num import NUM
from sym import SYM
from cols import COLS
from utils import *;
from config import the
from Node import NODE;
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

    
    def half(self, rows, sortp, before):
        the_half = min(len(rows) // 2, len(rows))
        some = random.sample(rows, the_half)
        a, b, C, evals = self.farapart(some, sortp, before)
        def d(row1, row2):
            return row1.dist(row2, self)
        
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

    def tree(self, sortp):
        evals = 0

        def _tree(data, above = None):
            nonlocal evals
            node = NODE(data)

            if len(data.rows) > 2 * (len(self.rows) ** 0.5):
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals += evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)

            return node

        return _tree(self), evals

    def branch(self, stop=None, rest=None, _branch=None, evals=None):
        evals, rest = 1, []
        stop = stop or (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals, rest

            if len(data.rows) > stop:
                lefts, rights, left, _, _, _, _  = self.half(data.rows, True, above)
                evals += 1
                for row1 in rights:
                    rest.append(row1)

                return _branch(self.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals

        return _branch(self)
    
    def clone(self, rows=None, newData=None):
        newData = DATA([self.cols.names])
        for row in rows or []:
            newData.add(row)
        return newData