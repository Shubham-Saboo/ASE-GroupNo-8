'''
Lua Code:
    local SYM=is"SYM"
    function SYM.new(s,n)
        return isa(SYM,{txt=s or " ", at=n or 0, n=0, has={}, mode=nil, most=0}) end

    function SYM:add(x)
        if x ~= "?" then 
            self.n = self.n + 1
            self.has[x] = 1 + (self.has[x] or 0)
            if self.has[x] > self.most then 
                self.most,self.mode = self.has[x], x end end end

    function SYM:mid() return self.mode end
'''
import math
class SYM:
    def __init__(self, s=" ", n=0):
        self.txt = s
        self.at = n
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0

    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode
          
    def div(self, e=0):
        for v in self.has.values():
            e -= v / self.n * math.log(v / self.n, 2)
        return e

    def small(self):
        return 0
