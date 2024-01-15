'''
Lua Code:
    local ROW=is"ROW"
    function ROW.new(t) return isa(ROW, { cells = t }) end

'''

class ROW:
    def __init__(self, t):
        self.cells = t