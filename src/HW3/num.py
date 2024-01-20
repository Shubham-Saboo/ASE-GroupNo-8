'''
Lua Code:
    local NUM=is"NUM"
    function NUM.new(s, n)
        return isa(NUM, {txt=s or " ", at=n or 0, n=0, mu=0, m2=0, hi=-1E30, lo=1E30,
                heaven = (s or ""):find"-$" and 0 or 1}) end

    function NUM:add(x,     d)
        if x ~="?" then
            self.n  = self.n+1
            d       = x - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(x - self.mu)
            self.lo = math.min(x, self.lo)
            self.hi = math.max(x, self.hi) end end

    function NUM:mid() return self.mu end
'''

class NUM:
    def __init__(self, s=" ", n=0):
        self.txt = s
        self.at = n
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = -1E30
        self.lo = 1E30
        self.heaven = 0 if (s or "").endswith("-") else 1

    def add(self, x):
        if x != "?" and isinstance(x, (int, float)):
            self.n += 1
            d = x - self.mu
            self.mu += d/self.n
            self.m2 += d*(x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1)) ** 0.5

    def like(self, x):
        mu, sd = self.mid(), (self.div() + 1E-30)
        nom = math.exp(-0.5 * ((x - mu) ** 2) / (sd ** 2))
        denom = (sd * 2.5 + 1E-30)
        return nom / denom