from row import ROW
from num import NUM
from sym import SYM
from cols import COLS
from utils import *;
from config import the
import math
import random
'''
Lua Code:
    local DATA=is"DATA"
    function DATA.new(src,  fun,     self)
        self = isa(DATA,{rows={}, cols=nil})
        if   type(src) == "string"
        then for _,x in l.csv(src)       do self:add(x, fun) end
        else for _,x in pairs(src or {}) do self:add(x, fun) end end
        return self end

    function DATA:add(t,  fun,row)
        row = t.cells and t or ROW.new(t)
        if   self.cols
        then if fun then fun(self,row) end
            self.rows[1 + #self.rows] = self.cols:add(row)
        else self.cols = COLS.new(row) end end

    function DATA:mid(cols,   u) 
        u = {}; for _, col in pairs(cols or self.cols.all) do u[1 + #u] = col:mid() end
        return ROW.new(u) end
'''

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
        u = [col.mid() for col in (cols or self.cols.all)]
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

    def gate(self, budget0, budget, some):
        random.seed(set_random_seed())
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
        return stats, bests

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