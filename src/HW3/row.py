'''
Lua Code:
    local ROW=is"ROW"
    function ROW.new(t) return isa(ROW, { cells = t }) end

'''

class ROW:
    def __init__(self, t):
        self.cells = t

    def like(self, data, n, n_hypotheses, prior):
        prior = (len(data.rows) + the.k) / (n + the.k * n_hypotheses)
        out = math.log(prior)

        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                out += math.log(inc)

        return math.exp(1) ** out
    
    def likes(self, datas, n, n_hypotheses, most, tmp, out):
        n, n_hypotheses = 0, 0

        for k, data in enumerate(datas, start=1):
            print(data)
            n += len(data.rows)
            n_hypotheses += 1

        for k, data in enumerate(datas, start=1):
            tmp = self.like(data, n, n_hypotheses)
            if most is None or tmp > most:
                most, out = tmp, k

        return out, most