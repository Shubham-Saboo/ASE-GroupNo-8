from sym import SYM
from num import NUM

'''
Lua Code:
    local COLS=is"COLS"
    function COLS.new(row)
        local x,y,all = {},{},{}
        local klass,col
        for at,txt in pairs(row.cells) do
            col = (txt:find"^[A-Z]" and NUM or SYM).new(txt,at)
            all[1+#all] = col
            if not txt:find"X$" then
                if txt:find"!$" then klass=col end
                (txt:find"[!+-]$" and y or x)[at] = col end end
        return isa(COLS,{x=x, y=y, all=all, klass=klass, names=row.cells}) end

    function COLS:add(row)
        for _,cols in pairs{self.x, self.y} do
            for _,col in pairs(cols) do
                col:add(row.cells[col.at]) end end 
        return row end
'''

class COLS:
    def __init__(self, row):
        self.x, self.y, self.all = [], [], []
        self.klass, self.names = None, row.cells

        for at, txt in enumerate(row.cells, start=1):
            col = (NUM if txt[0].isalpha() and txt[0].isupper() else SYM)(txt, at)
            self.all.append(col)

            if not txt.endswith("X"):
                if txt.endswith("!"):
                    self.klass = col
                (self.y if txt.endswith(("!", "-", "+")) else self.x).append(col)

    def add(self, row):
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])
        return row