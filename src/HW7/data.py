from row import ROW
from num import NUM
from sym import SYM
from cols import COLS
from utils import *;
from config import the
from Node import NODE;
import math
import random
import numpy as np

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
            self.cols.add(row)
            self.rows.append(row)
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [round(col.mid(),2) for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [round(col.div(),2) for col in (cols or self.cols.all)]
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

    list_1, list_2, list_3, list_4, list_5, list_6 = [[] for _ in range(6)]

    def gate(self, random_seed, budget0, budget, some):
        random.seed(random_seed)
        rows = random.sample(self.rows, len(self.rows)) 
        #y values of first 6 examples in ROWS
        DATA.list_1.append(f"1. top6: {[r.cells[len(r.cells)-3:] for r in rows[:6]]}")
        
        # y values of first 50 examples in ROWS
        DATA.list_2.append(f"2. top50:{[[r.cells[len(r.cells)-3:] for r in rows[:50]]]}")
        
        rows.sort(key=lambda row: row.d2h(self))
        # y values of ROW[1]
        DATA.list_3.append(f"3. most: {rows[0].cells[len(rows[0].cells)-3:]}")

        random.shuffle(rows)
        lite = rows[:budget0]
        dark = rows[budget0:]

        stats = []
        bests = []

        for i in range(budget):
            best, rest = self.best_rest(lite, (len(lite) ** some))
            todo, selected = self.split(best, rest, lite, dark)
            # y values of centroid of (from DARK, select BUDGET0+i rows at random)
            selected_rows_rand = random.sample(dark, budget0+i)
            y_values_sum = [0.0, 0.0, 0.0]
            for row in selected_rows_rand:
                y_val = list(map(coerce, row.cells[-3:]))
                y_values_sum = [sum(x) for x in zip(y_values_sum, y_val)]
            num_rows = len(selected_rows_rand)
            y_values_centroid = [round(val / num_rows,2) for val in y_values_sum]

            DATA.list_4.append(f"4: rand:{y_values_centroid}")

            # y values of centroid of SELECTED
            DATA.list_5.append(f"5. mid: {selected.mid().cells[len(selected.mid().cells)-3:]}")

            # y values of first row in BEST
            DATA.list_6.append(f"6. top: {best.rows[0].cells[len(best.rows[0].cells)-3:]}")

            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
        return stats, bests, [bests[-1].cells, round(bests[-1].d2h(self),2)]

    def stats_div(self, fun=None, ndivs=None):
        u = {}
        for col in self.cols.all:
            if(isinstance(col, SYM)):
                if(col.txt == "origin"):
                    u[col.txt] = round(col.div(),2)
                else:
                    u[col.txt] = col.div()
            else:
                u[col.txt] = round(col.div(),2)
        return u

    def mid_div(self):
        d2h_vals = [r.d2h(self) for r in self.rows]
        return[[self.stats(), round(np.mean(d2h_vals),2)],[self.stats_div(), round(np.std(d2h_vals),2)]]

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols.names, [])
        max_val = 0
        out = 1

        for i, row in enumerate(dark, 1):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)

            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp

        return out, selected

    def best_rest(self, rows, want):
        rows.sort(key=lambda a: a.d2h(self))
        best = DATA(self.cols.names)
        rest = DATA(self.cols.names)
        for i, row in enumerate(rows):
            if i < want:
                best.add(row)
            else:
                rest.add(row)
        return best, rest
    
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
        if current_distance <= target_distance:
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

    def clone(self, rows=None):
        new = DATA()
        for row in rows or []:
            new.add(row)
        return new

    def clone(self, rows=None, newData=None):
        newData = DATA([self.cols.names])
        for row in rows or []:
            newData.add(row)
        return newData

    def any50(self, random_seed):
        random.seed(random_seed)
        rows = random.sample(self.rows, 50)
        return [rows[0].cells, round(rows[0].d2h(self),2)]

    def best_100(self, random_seed):
        random.seed(random_seed)
        rows = random.sample(self.rows, len(self.rows))
        rows.sort(key=lambda row: row.d2h(self))
        return [rows[0].cells, round(rows[0].d2h(self),2)]