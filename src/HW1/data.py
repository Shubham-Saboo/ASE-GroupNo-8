from row import ROW
from cols import COLS
from utils import *;

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
            for _, x in enumerate(src):
                self.add(x, fun)

    def add(self, t, fun=None):
        row = ROW(t) if type(t) == list else t
        # row = t if t.get('cells') else ROW.new(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW.new(u)