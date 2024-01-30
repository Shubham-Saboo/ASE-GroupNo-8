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
    list_1, list_2, list_3, list_4, list_5, list_6 = [[] for _ in range(6)]

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

    

    def gate(self, budget0, budget, some):
        random.seed(set_random_seed())
        rows = random.sample(self.rows, len(self.rows)) #shuffles the data 
        DATA.list_1.append(f"1. top6: {[r.cells[len(r.cells)-3:] for r in rows[:6]]}")
        DATA.list_2.append(f"2. top50:{[[r.cells[len(r.cells)-3:] for r in rows[:50]]]}")
        
        rows.sort(key=lambda row: row.d2h(self))
        DATA.list_3.append(f"3. most: {rows[0].cells[len(rows[0].cells)-3:]}")
        # print(random.seed)
        random.shuffle(rows)
        lite = rows[:budget0]
        dark = rows[budget0:]

        stats = []
        bests = []

        for i in range(budget):
            best, rest = self.best_rest(lite, int(round(len(lite) ** some,1)))
            todo, selected = self.split(best, rest, lite, dark)
            DATA.list_4.append(f"4: rand:{sum(list(map(coerce, random.sample(dark, budget0+i)[0].cells[-3:])))/3}")
            DATA.list_5.append(f"5: mid: {selected.mid().cells[len(selected.mid().cells)-3:]}")
            DATA.list_6.append(f"6: top: {best.rows[0].cells[len(best.rows[0].cells)-3:]}")
            stats.append(selected.mid())
            bests.append(best)
            lite.append(dark.pop(todo))
        return stats, bests

    # def gate(self, randomSeed, budget0, budget, some):
    #     random.seed(randomSeed)
    #     rows = random.sample(self.rows, len(self.rows)) #shuffles the data     
    #     DATA.list_1.append(f"1. top6: {[r.cells[len(r.cells)-3:] for r in rows[:6]]}")
    #     DATA.list_2.append(f"2. top50:{[[r.cells[len(r.cells)-3:] for r in rows[:50]]]}")
    #     rows.sort(key=lambda row: row.d2h(self))
    #     DATA.list_3.append(f"3. most: {rows[0].cells[len(rows[0].cells)-3:]}")
    #     rows = random.sample(self.rows, len(self.rows))
    #     lite = rows[:budget0]
    #     dark = rows[budget0:]       
    #     stats, bests = [], []
    #     for i in range(budget):
    #         best, rest = self.best_rest(lite, len(lite)**some)
    #         todo, selected = self.split(best, rest, lite, dark)
    #         DATA.list_4.append(f"4: rand:{sum(list(map(coerce, random.sample(dark, budget0+i)[0].cells[-3:])))/3}")
    #         DATA.list_5.append(f"5: mid: {selected.mid().cells[len(selected.mid().cells)-3:]}")
    #         DATA.list_6.append(f"6: top: {best.rows[0].cells[len(best.rows[0].cells)-3:]}")
    #         stats.append(selected.mid())
    #         bests.append(best.rows[0])
    #         lite.append(dark.pop(todo))
    #     return stats, bests

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols.names, [])
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
        rows.sort(key=lambda a: a.d2h(self))
        best = DATA(self.cols.names)
        rest = DATA(self.cols.names)
        for i, row in enumerate(rows):
            if i < want:
                best.add(row)
            else:
                rest.add(row)
        return best, rest