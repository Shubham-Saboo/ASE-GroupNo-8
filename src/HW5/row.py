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