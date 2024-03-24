from config import the
from utils import keysort
import math

class ROW:
    def __init__(self, t):
        self.cells = t

    def d2h(self, data):
        d, n, p = 0, 0, 2
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** p
        return math.sqrt(d) / math.sqrt(n)

    def dist(self, other, data):
        d, n, p = 0, 0, 2
        for col in data.cols.x:
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
        return (d / n) ** (1 / p)

    def neighbors(self, data, rows=None):
        return keysort(rows or data.rows, lambda row: self.dist(row, data))

    def like(self, data, n, n_hypotheses):
        prior = (len(data.rows) + the['k']) / (n + the['k'] * n_hypotheses)
        out = math.log(prior)

        for col in data.cols.x:
           v = self.cells[col.at]
           if v != "?":
               inc = col.like(v, prior)
               if inc<=0:
                   return 0
               out += math.log(inc)

        return math.exp(1) ** out
    
    def likes(self, datas):
        n, n_hypotheses = 0, 0

        for k, data in datas.items():
            n += len(data.rows)
            n_hypotheses += 1
        
        most, out = None, None

        for k, data in datas.items():
            tmp = self.like(data, n, n_hypotheses)
            if most is None or tmp > most:
                most, out = tmp, k

        return out, most