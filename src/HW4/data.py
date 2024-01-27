from row import ROW
from num import NUM
from sym import SYM
from cols import COLS
from utils import *;
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
            # for _, x in enumerate(src):
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
        return ROW.new(u)

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


    def gate(self, budget0, budget, some):
        rows = self.rows[:]
        random.shuffle(rows)
        lite = rows[:budget0]
        dark = rows[budget0:]

        stats = []
        bests = []

        for _ in range(budget):
            best, rest = self.best_rest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))

        return stats, bests

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols_names, [])
        max_val = 1E30
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
        rows.sort(key=lambda row: row.d2h())
        best = rows[:want]
        rest = rows[want:]
        return DATA(self.cols_names, best), DATA(self.cols_names, rest)