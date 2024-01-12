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